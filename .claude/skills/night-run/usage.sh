#!/usr/bin/env bash
# Prints how much of the weekly Claude usage is spent, as a number from 0 to 1 (0.14 means 14% used).
# ponytail: costs one tiny headless call; read it at check-ins, not in a loop.
claude -p "Reply with ok" --model claude-haiku-5-5 --output-format stream-json --verbose 2>/dev/null |
  python3 -c '
import json, sys
for line in sys.stdin:
    try:
        event = json.loads(line)
    except ValueError:
        continue
    if event.get("type") == "rate_limit_event":
        print(event["rate_limit_info"]["unifiedWindows"]["seven_day"]["utilization"])
        break
else:
    sys.exit("No usage figure in the reply.")
'
