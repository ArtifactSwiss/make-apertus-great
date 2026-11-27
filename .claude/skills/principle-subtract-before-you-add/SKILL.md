---
name: principle-subtract-before-you-add
description: "Use only when a card or a person names this skill. Remove dead code, redundant validators, and stub references first, then build on the simpler base."
---
> Vendored from `github.com/backnotprop/pstack@c81f1bf680803f9e3f0cade6adb62593f43fb61f`, `skills/principle-subtract-before-you-add/`, MIT (see `LICENSE`).
> `CLAUDE.md` and `docs/design.md` win where this skill disagrees with them, and you never wait for a person: block the card instead.


# Subtract Before You Add

When evolving a system, remove complexity first, then build. Default to subtraction.

Make simplification a continual investment. Leave the design slightly simpler and more capable behind the same or smaller surface than you found it.

- Sequence removal before construction
- Cut before you polish (get to the minimum before investing in quality)
- Design for observed usage, not speculative edge cases
- No speculative validators, parsers, or guards beyond what the spec demands
- Simplify prompts (remove redundant instructions, excessive templates)
- When a reference has no novel content, delete it rather than leaving a stub
