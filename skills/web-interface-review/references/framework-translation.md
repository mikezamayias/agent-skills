# Translating the live rules to Vue, Nuxt, and Svelte

The live rule set is written in React and Tailwind vocabulary.
Read each rule for its intent, then check the equivalent below.
Plain-CSS projects take the CSS column wherever a rule names a Tailwind class.

## Markup and events

| Live rule term                     | Vue and Nuxt                               | Svelte and SvelteKit                                                                    |
| ---------------------------------- | ------------------------------------------ | --------------------------------------------------------------------------------------- |
| `onClick`, `onKeyDown`, `onKeyUp`  | `@click`, `@keydown`, `@keyup`             | `onclick`, `onkeydown` (Svelte 5) or `on:click` (Svelte 4)                              |
| `<div onClick>` should be a button | `<div @click>`                             | `<div onclick>`, also flagged by the Svelte `a11y_click_events_have_key_events` warning |
| `htmlFor`                          | `for`                                      | `for`                                                                                   |
| `<Link>`                           | `<NuxtLink>` or `<a href>`                 | `<a href>`                                                                              |
| `spellCheck={false}`               | `spellcheck="false"`                       | `spellcheck="false"`                                                                    |
| `autoFocus`                        | `autofocus` attribute or a focus directive | `autofocus` attribute or a `use:` action                                                |
| `.map()` over a large array        | `v-for`                                    | `{#each}`                                                                               |

## State, forms, and hydration

| Live rule term                               | Vue and Nuxt                                                                            | Svelte and SvelteKit                                                                                     |
| -------------------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `useState`                                   | `ref`, `reactive`, Nuxt `useState`                                                      | `$state` (Svelte 5), stores (Svelte 4)                                                                   |
| Input with `value` needs `onChange`          | `:value` with no `@input` and no `v-model` is read-only                                 | `value=` with no `bind:value` and no `oninput` is read-only                                              |
| Controlled input must be cheap per keystroke | Heavy `watch` or `computed` on a `v-model` value, fix with `v-model.lazy` or a debounce | Heavy `$derived` or `$effect` on a bound value, fix with a debounce                                      |
| URL reflects state, nuqs                     | `useRoute().query` read, `router.replace({ query })` write                              | `page.url.searchParams` read, `goto(url, { replaceState: true, keepFocus: true, noScroll: true })` write |
| Unsaved-changes guard                        | `onBeforeRouteLeave` plus `beforeunload`                                                | `beforeNavigate` plus `beforeunload`                                                                     |
| Date or time hydration mismatch              | `<ClientOnly>` or a fixed time zone on server and client                                | `browser` from `$app/environment`, or render in `onMount`                                                |
| `suppressHydrationWarning`                   | `data-allow-mismatch` (Vue 3.5 and later)                                               | No equivalent, skip the rule                                                                             |

Hydration rules apply only to server-rendered code.
A Nuxt app with `ssr: false` or a SvelteKit route with `ssr = false` skips them.

## Head, images, and fonts

| Live rule term                          | Nuxt                                                | SvelteKit                               | Plain HTML             |
| --------------------------------------- | --------------------------------------------------- | --------------------------------------- | ---------------------- |
| `<link rel="preconnect">`, font preload | `app.head.link` in `nuxt.config.ts` or `useHead`    | `src/app.html` or `<svelte:head>`       | `<head>`               |
| Image `priority`                        | `fetchpriority="high"`, or `preload` on `<NuxtImg>` | `fetchpriority="high"`                  | `fetchpriority="high"` |
| Image `width` and `height`              | Also required on `<NuxtImg>` and `<NuxtPicture>`    | `<img>` or the `enhanced:img` component | `<img>`                |

## Tailwind classes to CSS

| Tailwind               | CSS                                                                            |
| ---------------------- | ------------------------------------------------------------------------------ |
| `focus-visible:ring-*` | A visible `outline` or `box-shadow` under `:focus-visible`                     |
| `outline-none`         | `outline: none`                                                                |
| `truncate`             | `overflow: hidden`, `text-overflow: ellipsis`, `white-space: nowrap`           |
| `line-clamp-*`         | `line-clamp` with the `-webkit-line-clamp` and `display: -webkit-box` fallback |
| `break-words`          | `overflow-wrap: break-word`                                                    |
| `min-w-0`              | `min-width: 0`                                                                 |
| `h-screen`             | `100vh`, see M3 in [mobile-web.md](mobile-web.md)                              |
