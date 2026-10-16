# Search and AI answers for an app site

Read this when a landing page ships, or when the human asks for SEO, AEO (answer engine optimization, being named in ChatGPT, Perplexity or Google AI answers) or a recurring site check.
Rules are checked against Google, OpenAI and Perplexity docs on 2026-10-14.
The loop is adapted from Illyism/seo-skills `seo-autopilot` (MIT per its README, af48ce5).

## Ship checks per page

- One primary query per page, written into the `<title>`, the `<h1>` and the first paragraph.
  Two pages chasing one query is a bug: merge them and 301 the weaker one.
- Google publishes no length limit for titles or meta descriptions and truncates to the device width.
  Do not enforce 50-60 or 150-160 character rules.
  Put the query and the differentiator in the first words, then check the rendered result at 375px wide and on desktop.
- Google may rewrite a title from the `<h1>`, `og:title` or anchor text, so keep those consistent with `<title>`.
- Unique meta description, canonical, sitemap entry, OG tags and `SoftwareApplication` JSON-LD with the real store URL and price.
- The main content is in the server HTML, not injected by JavaScript.
- `robots.txt` and the CDN allow `Googlebot`, `Bingbot`, `OAI-SearchBot` and `PerplexityBot`.
  Blocking `OAI-SearchBot` removes the site from ChatGPT search answers, though it can still appear as a navigational link, and OpenAI applies `robots.txt` changes in about 24 hours.
  Blocking `GPTBot` only opts out of training and does not affect citations.
  `Perplexity-User`, which fetches a page when a user asks, generally ignores `robots.txt`, so blocking `PerplexityBot` is not a full opt-out from Perplexity answers.
- Google says AI Overviews and AI Mode need no special markup or optimization beyond normal indexing, so do not add "AEO schema".
- Answer the page's question in the first two sentences, then give detail.
  This is a writing rule for both readers and quoting engines, not a documented ranking factor.

## Recurring loop

Keep all state in `seo/` in the site repo, because the agent has no memory between runs.

- `seo/context.md`: product, buyer, prices, limits and competitors, each fact with the file or URL it came from.
- `seo/keyword-map.csv`: query, intent, target URL, status (live, planned, gap), position, last checked.
- `seo/ai-prompts.md`: 15-25 buyer questions and each assistant's answer per check.
- `seo/log.md`: one dated line per shipped change with its URL.
- `seo/reports/YYYY-MM-DD.md`: read the previous report first so the run spends tokens on what regressed, not on re-finding fixed issues.

Each run:

1. Health: request every sitemap URL and flag non-200s, redirect chains, wrong canonicals, stray `noindex`, orphan pages and duplicate titles.
2. Fact check: read commits since the last run.
   When a price, plan, limit or feature changed, fix every page stating the old fact the same day.
   If a page and the product disagree, the product is right.
3. Page 2 to page 1: for queries at positions 8-20 with real impressions, read the top 3 results, add what they have and the page lacks, and link to the page from strong related pages.
   Good position with a low click rate means rewrite the title and description instead.
4. AI answers: ask each assistant every question in `ai-prompts.md` at least 3 times, because answers vary run to run.
   The repeat count is our sampling rule, not vendor guidance.
   Count a source or a mention only when it recurs, and report the mention rate, not one answer.
   A wrong fact about the app means the owning page states it unclearly.
   Cited sources that omit the app are the outreach and directory list.
5. Competitors: diff each competitor's sitemap against the last snapshot and add a backlog item only where the app can make a better page.

Comparison pages ("X alternatives", "app vs X") must say where the competitor is better and source every competitor claim with an "as of" date.

## Never

- Buy links, paid guest posts or product-for-review placements with followed links.
  Google's spam policies treat paid links that pass ranking credit as link spam unless marked `rel="sponsored"` or `rel="nofollow"`.
- Re-request indexing for the same URL every day.
  Google says repeated requests do not crawl it faster, and the tool has a quota.
- Publish many generated pages with no added value, which Google's scaled content abuse policy targets.
- Invent a statistic, quote, review, price or benchmark.
- Send email, submit a directory listing, create an account or post socially.
  Draft it in `seo/outreach/` and list it in the report for the human.
- Remove or redirect a page that gets traffic or has inbound links without flagging it first.

## Sources

- <https://developers.google.com/search/docs/appearance/title-link>
- <https://developers.google.com/search/docs/appearance/snippet>
- <https://developers.google.com/search/docs/appearance/ai-features>
- <https://developers.google.com/search/docs/essentials/spam-policies>
- <https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl>
- <https://developers.openai.com/api/docs/bots>
- <https://docs.perplexity.ai/guides/bots>
- <https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/>
- <https://github.com/Illyism/seo-skills>
