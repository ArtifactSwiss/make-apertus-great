---
name: frontend-mockups
description: Mockup-first workflow for building any new frontend page or significant UI change: produce 3 structurally different mockup variants, let the user pick or combine, refine one, then build the confirmed design end to end without further input. Use this whenever the user asks for a new screen, page, view or UI for a feature, or to redesign one, e.g. "build the search page", "we need a UI for the classification results", "show me some options for the chat", even if they don't say "mockup".
---

# Mockups → pick → build

Phase 1 (mockups and refinement) is interactive: show options and wait for the user. Phase 2 (build) runs without the user, and the confirmed mockup is the spec. The frontend rules in CLAUDE.md apply to phase 2 in full. In phase 1, only the mockup rules below apply.

## Phase 1: three variants

Create `src/_mockups/<feature>/VariantA.tsx`, `VariantB.tsx`, `VariantC.tsx`. They show up at `/_mockups/<feature>/<variant>`.

**Make them differ in structure, not style.** Each variant is a different idea of how the page works: layout and information hierarchy (side-by-side vs top-down vs conversational, sources first vs answer first). Colours, fonts and radii come from the theme tokens and stay identical. The user is choosing a concept, and three recolours of the same layout waste that choice.

**Keep them cheap.** One presentational file per variant:
- Use shadcn components, Tailwind and theme tokens only, the same as the real app, so porting is straightforward.
- Put sample data inline at the top of the file. Make it realistic: real-looking Swiss names, judgements, amounts; German/French text where the app would show it; one long item to show overflow.
- Allowed: trivial `useState` for click-through (tabs, expand).
- Not allowed: API calls, feature hooks, elaborate types, tests, review. They're throwaway.
- Include the provenance UI the real feature will need (sources, model, checks), because it's part of the product.

**Show them.** Run the mockup screenshot script (laptop 1440×900 and projector 1920×1080) and present:

```
A: <one sentence: the idea of this variant>   [screenshots]
B: ...
C: ...
```

Then stop and wait for the user's choice.

## Refinement

The user picks one or combines ("B, with A's source list"). Build **one** refined mockup from that, never three again, so the design converges. Show its screenshots and wait. Repeat until the user confirms. The confirmed screenshots are the acceptance criterion for phase 2.

## Phase 2: build (no further input needed)

1. **Port:** split the confirmed variant into components in `src/features/<name>/`, replace the sample data with feature hooks (`useX.ts` wrapping `$api`), use `useStream` for streamed text, add the route in `routes.tsx`, and delete `src/_mockups/<feature>/`.
2. **Backend:** if endpoints are missing, follow the `add-endpoint` / `add-llm-feature` skills. Regenerate API types (`npm run gen:api`).
3. **States the mockup didn't show:** loading, error (including the stream `error` event and 502 "model unavailable") and empty. A blank screen in the demo is the worst outcome.
4. **Playwright happy-path test** for the feature (role-based selectors).
5. **Bug hunt:** only on pages this change touched, these 5 checks in this order, then stop:
   1. Console errors and failed network requests during the happy-path run
   2. Double-click submit, and submitting again while a stream is running
   3. Reload or browser-back in the middle of a stream
   4. One edge input: empty, then one long text with umlauts and accents (ä, é, à)
   5. Lots of content (e.g. 50 results, a 2000-character answer) at 1920×1080

   For each bug found, fix it and add a regression test for exactly that case.
6. **Visual comparison:** screenshot the built page at the same sizes and compare it with the confirmed mockup. Layout and hierarchy should match. Differences need a reason (e.g. a real state the mockup didn't have).
7. **Run `hackathon-review`.**

## Report

```
Feature: <name>, built from variant <X> (+ refinements)
Mockup vs built: [screenshots side by side]; differences: <list or "none">
Bug hunt: 1 ✅  2 ✅  3 ❌ fixed (+ test)  4 ✅  5 ✅
Review: <summary from hackathon-review>
```
