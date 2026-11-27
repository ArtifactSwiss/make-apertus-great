#!/usr/bin/env python3
"""Wait for a PR's checks or a card's status. Exit 0 when reached, 1 when a check failed or the PR conflicts, 2 on timeout."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scrum-board"))
import board  # noqa: E402

INTERVAL_SECONDS = 15
CONFLICT_POLLS = 2


def mergeable_state(pr: str) -> str:
    """MERGEABLE, CONFLICTING, or UNKNOWN while GitHub still computes."""
    result = subprocess.run(
        ["gh", "pr", "view", pr, "--json", "mergeable", "--jq", ".mergeable"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def checks_state(pr: str) -> str:
    """'pending' until a check exists and all have finished, then 'pass' or 'fail'."""
    result = subprocess.run(
        ["gh", "pr", "checks", pr, "--json", "name,bucket"],
        check=False,
        capture_output=True,
        text=True,
    )
    # gh exits 8 while checks run and 1 with "no checks reported" before CI starts
    if result.stdout.strip() == "" and "no checks reported" not in result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
        sys.exit(1)
    checks = json.loads(result.stdout) if result.stdout.strip() else []
    buckets = {check["bucket"] for check in checks}
    if not checks or "pending" in buckets:
        return "pending"
    for check in checks:
        print(f"{check['bucket']:8} {check['name']}")
    return "fail" if buckets & {"fail", "cancel"} else "pass"


def plain(value: str) -> str:
    return value.lower().replace("-", " ").replace("_", " ")


def card_status(number: int) -> str | None:
    return board.find_card(number=number)["status"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    checks = commands.add_parser(
        "checks", help="until every check of the PR has finished"
    )
    checks.add_argument("pr")
    checks.add_argument(
        "--timeout", type=int, default=540, help="seconds (default 540)"
    )
    status = commands.add_parser("status", help="until the card has reached the status")
    status.add_argument("number", type=int)
    status.add_argument("status", help="e.g. 'In review' or Done")
    status.add_argument(
        "--timeout", type=int, default=180, help="seconds (default 180)"
    )
    args = parser.parse_args()

    deadline = time.monotonic() + args.timeout
    conflicting_polls = 0
    while True:
        if args.command == "checks":
            # a conflicting PR gets no pull_request run, so its checks never start
            is_conflicting = mergeable_state(pr=args.pr) == "CONFLICTING"
            conflicting_polls = conflicting_polls + 1 if is_conflicting else 0
            # right after a push GitHub can still answer for the old head, so one poll is not enough
            if conflicting_polls == CONFLICT_POLLS:
                print(
                    f"PR {args.pr} conflicts with its base: "
                    "rebase onto origin/main and push.",
                    file=sys.stderr,
                )
                sys.exit(1)
            state = checks_state(pr=args.pr)
            if state != "pending":
                sys.exit(0 if state == "pass" else 1)
        else:
            current = card_status(number=args.number)
            if current is not None and plain(value=current) == plain(value=args.status):
                print(f"#{args.number} is {current}.")
                return
        if time.monotonic() > deadline:
            what = (
                "checks still running"
                if args.command == "checks"
                else f"status is {current}"
            )
            print(f"Timed out after {args.timeout}s: {what}.", file=sys.stderr)
            sys.exit(2)
        time.sleep(INTERVAL_SECONDS)


def demo() -> None:
    """Self-check against canned gh output: python3 wait.py --demo"""
    import contextlib
    import io
    from unittest import mock

    no_checks = (1, "", "no checks reported on the 'x' branch")
    pending = (8, '[{"name":"sync","bucket":"pending"}]', "")
    passed = (0, '[{"name":"sync","bucket":"pass"}]', "")

    def run(
        mergeables: list[str], checks: list[tuple[int, str, str]], timeout: int = 540
    ) -> tuple[int, str]:
        def fake_run(
            command: list[str], **_: object
        ) -> subprocess.CompletedProcess[str]:
            if command[2] == "view":
                return subprocess.CompletedProcess(
                    command, 0, mergeables.pop(0) + "\n", ""
                )
            returncode, stdout, stderr = checks.pop(0)
            return subprocess.CompletedProcess(command, returncode, stdout, stderr)

        stderr = io.StringIO()
        argv = ["wait.py", "checks", "1", "--timeout", str(timeout)]
        with (
            mock.patch.object(subprocess, "run", fake_run),
            mock.patch.object(time, "sleep"),
            mock.patch.object(sys, "argv", argv),
            contextlib.redirect_stderr(stderr),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            try:
                main()
            except SystemExit as stopped:
                code = 0 if stopped.code is None else int(stopped.code)
                return code, stderr.getvalue()
        return 0, stderr.getvalue()

    code, err = run(mergeables=["MERGEABLE"], checks=[passed])
    assert (code, "conflict" in err) == (0, False), (code, err)

    code, err = run(
        mergeables=["UNKNOWN", "UNKNOWN", "MERGEABLE"],
        checks=[no_checks, pending, passed],
    )
    assert (code, "conflict" in err) == (0, False), (code, err)

    code, err = run(mergeables=["UNKNOWN"], checks=[no_checks], timeout=0)
    assert (code, "conflict" in err) == (2, False), (code, err)

    code, err = run(mergeables=["CONFLICTING", "MERGEABLE"], checks=[no_checks, passed])
    assert (code, "conflict" in err) == (0, False), (code, err)

    code, err = run(
        mergeables=["UNKNOWN", "CONFLICTING", "CONFLICTING"],
        checks=[no_checks, no_checks],
    )
    assert (code, "conflicts with its base" in err) == (1, True), (code, err)
    print("wait.py demo: all checks pass")


if __name__ == "__main__":
    if sys.argv[1:] == ["--demo"]:
        demo()
    else:
        main()
