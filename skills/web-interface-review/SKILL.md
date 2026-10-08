---
name: web-interface-review
description: >-
  Review web UI code (HTML/CSS, Vue/Nuxt, Svelte) for interface correctness against live Vercel rules and mobile fixes. Use when asked to review a page, component or diff for accessibility, focus, forms, keyboard, dark mode or i18n issues. Also use when a web app or PWA feels wrong on a phone, or before shipping a Nuxt, Svelte or landing-page UI change.
license: MIT
metadata:
  fork-status: adapted
  upstream: https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines
---

# Web Interface Review

Review web UI source for interface correctness and report terse `file:line` findings with the fix for each.
The rule set is the Vercel Web Interface Guidelines, fetched live at the start of every review so it stays current.
Phone and PWA targets also get the mobile-web checks in [references/mobile-web.md](references/mobile-web.md).
The review is analysis-only.
Edit files only when the user asks to apply fixes.

## Scope and handoffs

In scope: accessibility, focus, forms, keyboard, content handling, images, performance that is visible in code, navigation state, touch, safe areas, dark mode, i18n, hydration, and mobile-web behavior.
Targets are plain HTML/CSS, Vue and Nuxt, and Svelte and SvelteKit.
The targets are not React, so translate the upstream React vocabulary with [references/framework-translation.md](references/framework-translation.md).

Hand off instead of duplicating:

| Need                                                                                               | Skill                                                   |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Aesthetic quality, anti-slop design audit, or building the design                                  | `tastemaker`                                            |
| Animation timing, easing, and motion review beyond the reduced-motion and `transition: all` checks | `tastemaker` (its `references/animation-guidelines.md`) |
| Measured Core Web Vitals (LCP, INP, CLS), traces, network waterfalls                               | `web-perf`                                              |
| Worst-case data stress test (long strings, empty, huge lists, slow network)                        | `break-ui`                                              |
| Rewriting UI copy or prose                                                                         | `humanizer`                                             |
| Flutter UI accessibility                                                                           | `vgv-accessibility`                                     |

## Workflow

1. Resolve the target.
   Use the files or glob the user names.
   With no target, use the uncommitted diff (`git diff --name-only HEAD`) filtered to `.vue`, `.svelte`, `.html`, `.css`, `.scss`, `.ts`, and `.js` UI files.
   With no diff either, ask once which files or routes to review.
2. Detect the stack from `package.json`, `nuxt.config.*`, `svelte.config.*`, and `tailwind.config.*` or a Tailwind v4 `@import "tailwindcss"`.
   Note where the global head, viewport meta, and base CSS live, because many rules are satisfied or broken there and not in the component.
3. Decide whether mobile-web applies.
   It applies when the project is a PWA (`@vite-pwa/nuxt`, `@vite-pwa/sveltekit`, a `manifest.webmanifest`, or a `pwa` key in `nuxt.config`), when the user says it is used on phones, or when the target is a landing page.
4. Fetch the live rules with the full text, not a summary.

   ```bash
   curl -fsSL --max-time 20 https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
   ```

   Prefer `curl` over a summarizing fetch tool, because summaries drop rules.
   Do not save the fetched rules into this skill or the project.
   If the fetch fails, print this message verbatim and then continue in degraded mode:
   `Live Web Interface Guidelines unreachable (<curl error>). Coverage is partial: reviewing from model knowledge plus references/mobile-web.md only. Rerun when online for the full rule set.`
   Label every finding in degraded mode as `[unverified rule]`.

5. Read each target file in full and its global context from step 2.
   Check every rule category in the fetched document, translated per [references/framework-translation.md](references/framework-translation.md).
   When step 3 applies, also check every item in [references/mobile-web.md](references/mobile-web.md).
   Where the live rules and mobile-web disagree, follow the resolution table in that file.
6. Verify each candidate before reporting it.
   Confirm the line number, confirm no global style, layout, component wrapper, or config already satisfies the rule, and confirm the element is really interactive or really content.
   Drop anything you cannot point to on a line.
7. Report using the output contract.
8. Only when the user asks to apply fixes, make the smallest edit per finding, put shared fixes in the global owner (base CSS, `app.head`, `app.html`) once, add no dependencies, and run the project's documented lint, type check, and build.
   Report which commands passed against the final state.

## Guardrails

- Never vendor or paraphrase the fetched rule set into this skill.
  The live document is the source of truth, and its rules change.
- Apply copy rules (Title Case, curly quotes, ellipsis) only to English UI strings.
  For Greek or other locales, check the locale's own punctuation and skip Title Case.
- Do not flag React-only rules literally.
  Translate them, or skip them when the framework has no equivalent, and say which were skipped.
- Never recommend `user-scalable=no` or `maximum-scale=1`.
  Fix the 16px input font size instead.
- Gate hover by capability media queries, never by user agent or screen width.
- Mobile-web behavior does not reproduce in desktop device emulation.
  Mark which findings are code-verified and which need a real phone.
- Do not report measured performance numbers.
  Code-visible problems such as missing image dimensions are in scope, while timing belongs to `web-perf`.
- Report a pattern repeated across many files once with all locations, not as separate findings.
- Do not commit, push, or deploy.

## Output contract

No preamble.
Deliver, in order:

1. Rules source: `Rules: live command.md fetched <YYYY-MM-DD>` or the degraded-mode message from step 4, plus `Mobile-web: applied` or `Mobile-web: not applied (<reason>)`.
2. Findings grouped by file under a `## path` heading, one per line as `path:line - issue -> fix`.
   Add a short reason only when the fix is not obvious.
   A clean file gets one line, `pass`.
3. Global fixes: issues whose fix belongs in base CSS, `nuxt.config`, `app.html`, or the manifest, listed once with the owning file.
4. Needs a phone: mobile-web findings that only real hardware can confirm.
5. Skipped: rule categories not applicable to this stack or target, with a one-line reason each.
6. Handoffs: which sibling skill should take what, only when something was out of scope.

Example finding lines:

```text
## components/ItemCard.vue

components/ItemCard.vue:14 - icon-only button has no accessible name -> add aria-label="Delete item"
components/ItemCard.vue:31 - div with @click acts as a button -> use <button type="button">
components/ItemCard.vue:58 - :hover not gated, sticks after tap -> wrap in @media (hover: hover) and (pointer: fine)
```

## Credits

Rule set and review format: Vercel `web-design-guidelines` skill and the live `web-interface-guidelines` command document (MIT, Vercel).
Mobile-web checks: condensed and paraphrased from Emil Kowalski's `mobile-native` skill (MIT, Copyright (c) 2026 Emil Kowalski).
