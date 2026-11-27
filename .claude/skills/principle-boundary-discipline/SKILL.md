---
name: principle-boundary-discipline
description: "Use only when a card or a person names this skill. Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions."
---
> Vendored from `github.com/backnotprop/pstack@c81f1bf680803f9e3f0cade6adb62593f43fb61f`, `skills/principle-boundary-discipline/`, MIT (see `LICENSE`).
> `CLAUDE.md` and `docs/design.md` win where this skill disagrees with them, and you never wait for a person: block the card instead.


# Boundary Discipline

Validate, narrow types, and handle errors where data crosses a system boundary (CLI args, config files, external APIs, network). Inside, trust the types: no re-validation and no redundant nil checks. Parse raw data into domain types at the boundary, and keep transport and framework types out of the public surface. Business logic lives in pure functions with no framework dependencies. The shell that calls them is thin.

Two tests. Is this data crossing a boundary right now? If not, the validation is redundant. Can this be a pure function the shell just calls? If yes, extract it.
