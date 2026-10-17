# Search and AI answers for an app site

Read this when a landing page ships, or when the human asks for SEO, AEO (answer engine optimization, being named in ChatGPT, Perplexity or Google AI answers) or a recurring site check.
Rules are checked against Google, OpenAI and Perplexity docs on 2026-10-14.
The crawler rules were rechecked against Anthropic, Apple, Google, OpenAI and Perplexity docs on 2026-10-17.
The loop is adapted from Illyism/seo-skills `seo-autopilot` (MIT per its README, af48ce5).
The AI answer counting rules are ours, adapted from the `ai-visibility-audit` skill in every-app/open-seo (MIT per its README, d7ea785).

## Ship checks per page

- One primary query per page, written into the `<title>`, the `<h1>` and the first paragraph.
  Two pages chasing one query is a bug: merge them and 301 the weaker one.
- A title that lists queries with different intent splits the page.
  Keep the queries one page can satisfy together (the head term, "buy X", "X online") in one title and give each different-intent modifier, such as "X for sleep", its own page.
  This is our own heuristic, not a Google rule, because Google's title guidance asks only for descriptive and concise titles.
  Check the live top results for each query before splitting.
- Google publishes no length limit for titles or meta descriptions and truncates to the device width.
  Do not enforce 50-60 or 150-160 character rules.
  Third-party auditors still flag title and description lengths, and the common 60-character rule comes from SEO tools, not from Google.
  Drop those findings instead of rewriting a title to satisfy them.
  Put the query and the differentiator in the first words, then check the rendered result at 375px wide and on desktop.
- Google may rewrite a title from the `<h1>`, `og:title` or anchor text, so keep those consistent with `<title>`.
- Unique meta description, canonical, sitemap entry, OG tags and `SoftwareApplication` JSON-LD with the real store URL and price.
- The main content is in the server HTML, not injected by JavaScript.
- The production page carries no `noindex`, in a robots meta tag or an `X-Robots-Tag` response header, and `robots.txt` does not disallow it.
  Google drops a page with `noindex` from Search results entirely once it recrawls the page, and a recrawl can take months.
  A `robots.txt` disallow only blocks crawling, so the URL can still be indexed and shown without a snippet, and Google never sees a `noindex` on a disallowed page.
  Draft and staging deploys often add `X-Robots-Tag: noindex`, so check the response headers of the production URL, not the source.
- `robots.txt` and the CDN allow `Googlebot`, `Bingbot`, `OAI-SearchBot` and `PerplexityBot`.
  Blocking `OAI-SearchBot` removes the site from ChatGPT search answers, though it can still appear as a navigational link, and OpenAI applies `robots.txt` changes in about 24 hours.
  Blocking `GPTBot` only opts out of training and does not affect citations.
  `Perplexity-User`, which fetches a page when a user asks, generally ignores `robots.txt`, so blocking `PerplexityBot` is not a full opt-out from Perplexity answers.
  `ChatGPT-User` fetches a page when a user asks ChatGPT, and OpenAI says `robots.txt` rules "may not apply" to it.
  It is not the setting for ChatGPT search inclusion, which `OAI-SearchBot` controls.
- Anthropic runs three agents, each blocked by its own `robots.txt` entry and set separately per subdomain.
  `ClaudeBot` collects content that may be used for training, and blocking it signals that future content should be excluded from training datasets.
  `Claude-SearchBot` indexes pages for Claude search and `Claude-User` fetches a page when a person asks Claude.
  Anthropic says blocking either of those two may reduce the site's visibility, so allow them.
- `Applebot-Extended` does not crawl and only decides how content crawled by `Applebot` may be used.
  Disallowing it opts the site out of training Apple's foundation models, and the pages can still appear in Apple search results.
  If `robots.txt` names `Googlebot` but not `Applebot`, `Applebot` follows the `Googlebot` rules.
  A `nosnippet` robots meta tag or `X-Robots-Tag: applebot: nosnippet` header stops Apple from generating a description or web answer and from using the page as extra context for AI-generated output.
  It does not stop crawling or training.
- `Google-Extended` has no user agent of its own and works only as a `robots.txt` control token.
  Blocking it opts the content out of training future Gemini models and out of grounding in Gemini Apps and Grounding with Google Search on Vertex AI.
  Google says it does not affect inclusion or ranking in Google Search.
- Check Search Console > Settings > Search generative AI shows Include for the property, which is the default.
  The other options are Exclude and Inherit.
  Google says Exclude means the site receives no traffic or impressions from these features, and takes effect within 1-2 days.
  This control is separate from `Google-Extended`, which does not affect Search inclusion.
- Submit the sitemap in Google Search Console and Bing Webmaster Tools.
  DuckDuckGo says it largely sources its traditional links from Bing.
- IndexNow (a protocol that tells participating engines a URL was added, updated or deleted) takes up to 10,000 URLs per POST request.
  One submission is shared with all participating engines, and Google is not listed among them.
  Publish only URLs that changed, because the IndexNow FAQ says not to resubmit unchanged URLs.
  Bing says IndexNow does not guarantee a page is crawled or indexed.
  Bing's guide lists enabling Crawler Hints in a Cloudflare account as the no-code route, and a deploy step that POSTs only the changed URLs otherwise.
- When the site sells or has sign-in, check GA4 (Google Analytics 4) unwanted referrals before launch.
  Google names third-party payment processors as the standard use, so returning shoppers are not credited to the payment domain.
  The list holds at most 50 domains per data stream and needs the Editor role.
  Add any sign-in domain that shows up as a referral in the same list.
- Google says AI Overviews and AI Mode need no special markup or optimization beyond normal indexing, so do not add "AEO schema".
- Google says a page must be indexed and eligible to be shown in Search with a snippet to appear in AI features, so check the page carries no `noindex` or `nosnippet`.
  Google does not guarantee indexing or serving.
- Answer the page's question in the first two sentences, then give detail.
  This is a writing rule for both readers and quoting engines, not a documented ranking factor.
- Keep each answer section short enough to stand alone under its heading.
  Some retrieval pipelines split pages into chunks, and Google's Vertex AI Search sets a configurable `chunkSize` that defaults to 500 tokens, with supported values of 100-500, and an `includeAncestorHeadings` option that defaults to false.
  Google does not say Search or AI Overviews use that setting.
  Google's generative AI guide says "There's no requirement to break your content into tiny pieces for AI to better understand it", so never split a page for AI.
  Keep this as our reader-first writing rule, not a ranking factor.

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
   Update the same fact in the page's JSON-LD (`offers.price`, `priceCurrency`) and in the App Store and Play listings in the same change.
   Microsoft's AEO and GEO guide for retailers asks to "Maintain consistent values across feed, on-site schema, and user-facing displays" (page 12).
   That guide speaks for Copilot and Bing, not for Google.
   If a page and the product disagree, the product is right.
3. Page 2 to page 1: for queries at positions 8-20 with real impressions, read the top 3 results, add what they have and the page lacks, and link to the page from strong related pages.
   Good position with a low click rate means rewrite the title and description instead.
4. AI answers: ask each assistant every question in `ai-prompts.md` at least 3 times, because answers vary run to run.
   The repeat count is our sampling rule, not vendor guidance.
   Count a source or a mention only when it recurs, and report the mention rate, not one answer.
   A wrong fact about the app means the owning page states it unclearly.
   Cited sources that omit the app are the outreach and directory list.
   Also report the share of answers that name the app first, and which competitor is named first in the rest.
   This first-named split is our own reporting rule, not vendor guidance on ranking.
   Keep questions that name the app out of the mention rate, and report how many were left out.
   Count rates over answered runs only, and report failed or empty answers separately, because they are not absence.
   Record for every run whether the assistant searched the web, because an answer that did not search cites nothing and is not a lost citation.
   Report each assistant on its own line, not as one blended rate.
   With fewer than about 10 neutral questions, call the result a direction to check, not a finding.
   These counting rules are ours too.
   Next to the sampled rate, record GA4 sessions in the AI Assistant channel (medium `ai-assistant`).
   Google says that channel covers sources like ChatGPT, Gemini, Deepseek, Copilot and Grok, and excludes Google's AI Overviews and AI Mode.
   For those two surfaces, open Search Console > Performance > Search results > Generative AI.
   The report launched on 2026-06-03 and Google says it reached all websites worldwide by 2026-08-31.
   Impressions are the only metric it defines, so it has no clicks, position or query data.
   A missing report can mean too few AI impressions or a site excluded from Search generative AI features.
   Before crediting installs or revenue to AI answers, separate first-time visitors from returning or branded ones, because an assistant can route an existing customer back to the site.
   Never credit revenue from a post-purchase survey alone.
   This attribution rule is ours.
5. Competitors: diff each competitor's sitemap against the last snapshot and add a backlog item only where the app can make a better page.

Rank evidence rules, ours, adapted from OpenSEO's public skills (MIT per its README, d7ea785):

- Count organic listings only, not ads, maps or other result blocks, and write the spot as "#11 (page 2)".
- Check 20 deep and write "not in the first 20 results" for a page not found.
  A failed lookup is unknown, not absent.
- Record the query, country, language and date with every position.
  A tool's retrieval date is not the date the ranking was observed.
- When two checks on one day disagree, keep both, because that is same-day variation and not a trend.
  One snapshot is not a baseline.
- Search volume is not visits.
  A page that already ranks already gets part of the volume, so size a gain on the extra clicks, not on the total.
- Treat a "#1 in N months" claim from a source as unproven until it names the site, the starting position and whether the domain was already strong.
  A tool's "x to 1" with "New" only means the page was not ranking in the compared period.
  Ahrefs traffic is an estimate, so do not size a plan on it.
- DR (Domain Rating) is an Ahrefs metric that shows the relative strength of a website's backlink profile.
  Google states that third-party authority scores do not come from Google, so do not make a DR threshold a requirement.

Comparison pages ("X alternatives", "app vs X") must say where the competitor is better and source every competitor claim with an "as of" date.

## Never

- Buy links, paid guest posts or product-for-review placements with followed links.
  Google's spam policies treat paid links that pass ranking credit as link spam unless marked `rel="sponsored"` or `rel="nofollow"`.
- Build links with keyword-rich anchor text in guest posts, articles or press releases placed on other sites, or with automated link tools.
  Google's link spam policy lists "links with optimized anchor text in articles, guest posts, or press releases distributed on other sites" and "using automated programs or services to create links to your site".
- Build `llms.txt` files, AI-only copies of pages, or campaigns for inauthentic mentions as a Google AI tactic.
  Google says new machine-readable files, AI text files, markup or Markdown neither help nor harm visibility in Google Search, because Google Search ignores them, and keeping `llms.txt` for other services is fine.
  Its guide also lists rewriting content just for AI systems and seeking inauthentic mentions as myths.
- Publish pages per fan-out query variant mainly to manipulate rankings or AI responses.
  Google's scaled content abuse policy covers many pages made mainly to manipulate rankings, whatever the production method.
  Applying it to fan-out pages is our inference, because the spam policy page does not use the term.
- Re-request indexing for the same URL every day.
  Google says repeated requests do not crawl it faster, and the tool has a quota.
- Use the Google Indexing API, or tools built on it, for app or marketing pages.
  Google says it "can only be used to crawl pages with either JobPosting or BroadcastEvent embedded in a VideoObject".
- Resubmit unchanged URLs through IndexNow.
- Publish many generated pages with no added value, which Google's scaled content abuse policy targets.
- Invent a statistic, quote, review, price or benchmark.
- Send email, submit a directory listing, create an account or post socially.
  Draft it in `seo/outreach/` and list it in the report for the human.
- Remove or redirect a page that gets traffic or has inbound links without flagging it first.

## Sources

- <https://developers.google.com/search/docs/appearance/title-link>
- <https://developers.google.com/search/docs/appearance/snippet>
- <https://developers.google.com/search/docs/appearance/ai-features>
- <https://developers.google.com/search/docs/fundamentals/ai-optimization-guide>
- <https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports>
- <https://support.google.com/webmasters/answer/16984139>
- <https://support.google.com/webmasters/answer/16908024>
- <https://ahrefs.com/blog/domain-rating/>
- <https://developers.google.com/search/docs/essentials/spam-policies>
- <https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl>
- <https://developers.google.com/search/docs/crawling-indexing/block-indexing>
- <https://developers.google.com/search/docs/crawling-indexing/robots/intro>
- <https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers>
- <https://developers.google.com/search/apis/indexing-api/v3/quickstart>
- <https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler>
- <https://support.apple.com/en-us/119829>
- <https://www.indexnow.org/faq>
- <https://www.bing.com/indexnow/getstarted>
- <https://duckduckgo.com/duckduckgo-help-pages/results/sources>
- <https://support.google.com/analytics/answer/9756891>
- <https://support.google.com/analytics/answer/10327750>
- <https://docs.cloud.google.com/generative-ai-app-builder/docs/parse-chunk-documents>
- <https://about.ads.microsoft.com/content/dam/sites/msa-about/global/common/content-lib/pdf/from-discovery-to-influence-a-guide-to-aeo-and-geo.pdf>
- <https://developers.openai.com/api/docs/bots>
- <https://docs.perplexity.ai/guides/bots>
- <https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/>
- <https://github.com/Illyism/seo-skills>
