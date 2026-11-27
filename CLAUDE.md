# Make Apertus Great: project guide

Our entry for the ti&m challenge at Hack Apertus: the TrustRoom, an AI space inside e-banking.
`challenge_description.md` is the brief, `starter/README.md` explains the mock e-banking we plug into.
Five people and their agents work in parallel, so the conventions below matter more than any clever solution.

## Rules of the challenge

- Our code lives in `src/`. Never rename or move the template files (`README.md`, `technical_report.md`,
  `challenge_description.md`, `LICENSE`, `starter/`).
- The model is Apertus v1.5 through the Keera gateway, configured only by `LLM_NAME`, `LLM_BASE_URL`
  and `LLM_API_KEY`. No closed model and no proprietary AI API at runtime.
- Customer data stays inside: nothing the customer types, uploads or owns goes to a service outside
  the stack in `starter/docker-compose.yml`, except the model gateway.
- Figures are never invented. The server computes every sum, date and comparison from the banking API;
  the model only chooses what to compute and words the result. Every figure can name its bookings.
- Identity comes from the token the e-banking hands us. We build no login of our own.

## Branches

- `main` is development. Every card lands here.
- `prod` holds stable versions. It only moves by promoting a commit of `main` that a human picked.
  Agents never push to `prod`.

## Board

The [board](https://github.com/users/gusevm1/projects/4) is the single source of truth for what gets
built, who is on it and how far it is. Every change belongs to a card.

- **Before any work, use the `scrum-board` skill:** take the next Ready card, claim it, build it, open
  a PR with `Closes #<n>`.
- **Humans decide what gets built** (Backlog to Ready, priority, owner) at the sprint boundary. Agents
  add cards to Backlog and never promote them.
- **Stuck or need a decision:** block the card with the exact question and take the next one. Never
  wait, never guess a product decision.
- **Building a card:** `build-card` takes it from claim to merged in its own worktree with its own
  banking API and ports, and `land-card` lands it on `main` after checking what others landed.
- **One card at a time changes prompts or tool descriptions.** Such an edit changes answers to
  unrelated questions, so those cards run in sequence and small prompt wishes go into one card.
- **Unattended runs:** one orchestrator follows the `night-run` skill. It hands cards to implementers
  and keeps the run log; it never builds or merges.
- Humans run `sprint-boundary` every few hours and `refine-issue` on new ideas.

## Writing

Before prose goes to a person (a card, a PR body, a commit message, docs, the report), apply the
`unslop` skill to it.

## Scope

One concern per PR: one capability or one fix, end to end. If you notice something else worth fixing,
add a card for it.

## Tests

Never weaken, skip or delete a failing test to make it pass. If you think the test is wrong, stop and
explain why.

## Commands

- Whole stack (from `starter/`): `docker compose up -d`. E-banking on 8090, banking API on 8000,
  MCP server on 8001, OCR on 8002. Demo logins are in `starter/README.md`.
- Their example TrustRoom: `TRUSTROOM_URL=http://localhost:3000 docker compose --profile example up -d`.
- Model settings for local work: `.env` in the repo root with the three `LLM_*` variables.
- Board: `python3 .claude/skills/scrum-board/board.py list`.
- Checks before landing: `.claude/skills/land-card/gates.sh`.
