---
name: principle-minimize-reader-load
description: "Use only when a card or a person names this skill. Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope."
---
> Vendored from `github.com/backnotprop/pstack@c81f1bf680803f9e3f0cade6adb62593f43fb61f`, `skills/principle-minimize-reader-load/`, MIT (see `LICENSE`).
> `CLAUDE.md` and `docs/design.md` win where this skill disagrees with them, and you never wait for a person: block the card instead.


# Minimize Reader Load

Reader load is the work a reader must do to understand code. It has two independent axes: layers to trace between the question and the answer, and hidden or mutable state to hold in their head. Guard both.

- Collapse layers that only forward: wrappers with one caller, adapters with no second implementation, pass-through methods. Inline them.
- Shrink state scope: returns over mutations, locals over fields, fields over module state, module state over globals. Derive instead of sync.
- Name an invariant once at the boundary, not in every consumer.

The test: can a new reader answer "where does X come from?" and "what can change X?" in under 30 seconds? If not, cut layers or cut state.
