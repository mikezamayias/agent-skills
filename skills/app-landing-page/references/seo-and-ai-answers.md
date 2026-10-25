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
- Google says there is no limit on meta description length, and truncates titles and snippets in results as needed, typically to fit the device width.
  Its title guidance asks only to avoid unnecessarily long or verbose text.
  Do not enforce 50-60 or 150-160 character rules.
  Third-party auditors still flag title and description lengths, and the common 60-character rule comes from SEO tools, not from Google.
  Drop those findings instead of rewriting a title to satisfy them.
  Put the query and the differentiator in the first words, then check the rendered result at 375px wide and on desktop.
- Google may rewrite a title from the `<h1>`, `og:title` or anchor text, so keep those consistent with `<title>`.
- Unique meta description, canonical, sitemap entry, OG tags and `SoftwareApplication` JSON-LD with the real store URL and price.
  For a native app on several platforms, give each platform its own `operatingSystem` value (for example `iOS`, `watchOS`, `macOS`, `Android`) and its own download URL, such as the App Store, Play, or the Mac direct download.
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
- The CDN line earlier in this list names four other agents, so check the CDN or bot-protection setting for `ClaudeBot`, `Claude-SearchBot` and `Claude-User` too.
  A site can allow them in `robots.txt` and still block them at the network edge (advice from a vendor study, not tested here).
- Do not submit a site to Brave Search as a way to appear in Claude.
  An X post (2026-10-24) says a site needs to be indexed in Brave for Claude and gives no source.
  Anthropic's web search tool page and Help Center page name no search provider (read 2026-10-25).
  One vendor study (Writesonic, 2026-10-20, one account) reports that Claude's default search mode shares 13.3% of cited domains with Brave's API and 38.4% in its extended mode, and dates a change to 2026-10-05 (single report, not reproduced, not confirmed by Anthropic).
  Treat the source behind Claude search as unknown and unstable.
- Brave Search has its own index and a crawler that sends no distinct user agent, so `robots.txt` cannot target it.
  Brave says its crawler does not crawl a page that Googlebot cannot crawl.
  Its form at `search.brave.com/submit-url` is described in Brave's help as a way to have a URL re-fetched, to apply a `noindex` or to delist a page that no longer exists.
  Use it for that and do not count on it to add a new page.
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
- Put a blog on the app's own domain or a subfolder of it, and not on a platform's domain.
  This is a vendor claim, not a verified rule, because Outrank's free blog page calls a subfolder "the best option for SEO" (read 2026-10-20).
  Google's SEO Starter Guide (read 2026-10-23) is neutral on subfolder versus subdomain, see the next bullet.
  Outrank's free blog tier (10,000 visits a month, a "Published with Outrank" badge, and blogs that break its content policy stay hidden from search engines on the free subdomain) is a data point for a vendor comparison only, not a recommendation.
- For a portfolio of apps, a subdomain or a subfolder per app on one domain is a valid structure.
  Google's SEO Starter Guide (read 2026-10-23) says: "From a business point of view, do whatever makes sense for your business."
  It adds that subdirectories can be easier to manage and that subdomains can make sense for separate topics or industries.
  It names no ranking difference and does not discuss buying a separate domain per app.
  One developer who runs per-app SEO sites reports that they started with a separate domain per app, moved to subdomains because separate domains were getting expensive, and saw "no difference whatsoever" (single report on X, October 2026, no data).
  Choose by maintenance and cost and measure each site in Search Console.
  Not buying a domain per app follows from that report and from Google's neutrality (inference), and is not a Google rule.

## Translated pages

Add a language only when a human who reads it has reviewed the page, because Google's scaled content abuse policy covers many pages made mainly to manipulate rankings, whatever the production method.
Give every language its own URL, and have every version list itself and every other version with `hreflang`, in the HTML, the HTTP headers or the sitemap, but not in several at once, because Google says combining methods gives no benefit in Search.
Annotations must be reciprocal, because Google ignores the tags when two pages do not point to each other.
Use fully qualified absolute URLs, and add an `x-default` for the language selector page.
Google does not use `hreflang` or the HTML `lang` attribute to detect a page's language, so the translated main content is what separates versions from duplicates.
Translating only the navigation and footer leaves the versions duplicates, so translate the main content.
Pick languages by where Search Console already shows impressions or where the store listing is localized, not by a round number such as 10.
Check each translated page's hreflang set, canonical and sitemap entry in the same change that publishes it.
The hreflang rules were read on Google's localized versions page on 2026-10-21.
The post behind this section (minosdevs, 2026-10-19) says to translate into 10 more languages, which is its own claim and is not adopted, and its author sells a EUR 349 course that teaches the method.

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
   3b. New pages from impressions: for a query with impressions in Search Console and no page that targets it, add it to `seo/keyword-map.csv` with status `planned`.
   Write a page only when it can answer the query with something the top 3 results and the app's own listing do not already give.
   Cap new pages at a few per run, and review each as if it were hand-written.
   Skip a query when a page already covers its intent, and merge instead of publishing two pages for one query.
   The idea comes from the minosdevs post (2026-10-19, a method with no result figure) and the guardrails are ours, from the rules in this file.
   3c. Several app sites: read every property at once instead of opening each one.
   The Search Console API method `searchanalytics.query` takes `startDate`, `endDate`, `dimensions` (use `date` for a trend line) and `rowLimit` from 1 to 25,000, and returns clicks, impressions, ctr and position, with the read-only scope `https://www.googleapis.com/auth/webmasters.readonly` (Google, read 2026-10-23).
   Google's quota is 1,200 queries per minute per site and per user, which a dozen daily queries never approach.
   The Google pages read do not say whether a service-account email can be added as a property user, so confirm that in Search Console before relying on it.
   The API returns only finalized data when `dataState` is omitted, and `dataState` "all" returns fresh data that can still change, so compare complete days only.
   Give any status flag a minimum click count, and add a "flat for N weeks" status, because a percentage rule flags a site with 4 clicks as rising and a week-over-week rule misses a site that went to zero long ago (inference).
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
   Classify every cited source by type: listicle, blog article or guide, comparison or review, Wikipedia or research, product or landing page, docs or help center, forum or social, video, review platform or news.
   A reference base rate exists, and it is a vendor study (Outrank sells blog content), one benchmark run on 2026-10-20, 48 generic questions, 1,329 cited sources, API answers with web search on, with types assigned by a Claude model.
   Its blog content share (listicles, blog articles and guides, comparisons) was 73% pooled, 18% for ChatGPT, 84% for Perplexity, 71% for Gemini and 93% for Claude.
   Compare the app's own sample against it only as a direction, under the fewer-than-10-questions rule above.
   A pooled share hides large differences between assistants, so never state it as the behavior of one assistant, and report the assistant that actually sends the traffic.
   The 73% is also not "what AI looks at", because the chart counts sources cited in an answer.
   The pooled-share reading is ours, derived from the chart (high confidence as a reading of the data, low confidence as a fact about the world).
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
6. Links: keep `seo/links.csv` with site, type (directory, founder story, article platform, launch site), URL, status (candidate, drafted, submitted by human, live), live URL and date.
   Each run, add at most 5 candidates and draft the submission text in `seo/outreach/`.
   Pick candidates by topical fit to the app, not by DR.
   The human submits.
   The source types come from one author's promotional list that was not verified, so check each site before listing it.
   To find listicle candidates, ask an assistant "best [category] tools" and note the competitors it recommends.
   Then open each competitor in a backlink tool and list the "Best X" listicles that link to it.
   This recipe is from a post by @illyism (2026-10-20), who sells link-building tools.
   It has no response rate or result data, and replies to the quoting post say listicle owners seldom answer and often ask for payment (single accounts, unverified).
   The recipe needs a paid backlink tool, and a free backlink checker was not tested for the same filter.
   Selection stays by topical fit under the rule above.
   The human sends every email, and an agent never pays for a placement.
   Do not buy or join a network of links to rank, such as a plan advertising "Backlinks from real sites in the Outrank network" (Outrank pricing page, read 2026-10-20).
   Google's spam policies, read 2026-10-21, define link spam as "creating links to or from a site primarily for the purpose of manipulating search rankings".
   They list "Buying or selling links for ranking purposes" and "Using automated programs or services to create links to your site".
   They allow paid links only when qualified with `rel="nofollow"` or `rel="sponsored"`.

Seed plan for a new app site, from a video by Dan Kulkov endorsed by pfernan95dev (2026-10-19, narration only, no results shown, the "working for a month" claim is self-reported and unverified):
choose 10 to 20 keywords, record a volume figure and its source for each in `seo/keyword-map.csv`, and publish them in a bounded batch over about two weeks.
Drop any keyword with no measured volume.
Draft two formats first: `best <niche> apps` and `<big competitor> alternatives`.
The alternatives page follows the comparison rule below, with competitor strengths and "as of" dates.
Each page needs its own primary query and real content, under the scaled content rule in Never.
The two-week batch is larger than the few-pages-per-run cap in step 3b, so keep the cap and treat the batch as a plan, not a pace.

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
- Run a keyword difficulty check before building a page.
  The video above says Google is stricter with new sites, so expect AI-assistant referrals before Google ones (source claim, no data).
  One reply to the source (@mankaff\_) says the tactic does not work in a red ocean, which is a single unverified comment.
- Treat a "#1 in N months" claim from a source as unproven until it names the site, the starting position and whether the domain was already strong.
  A tool's "x to 1" with "New" only means the page was not ranking in the compared period.
  Ahrefs traffic is an estimate, so do not size a plan on it.
- Treat a "N backlinks built" claim the same way.
  Ask for the site, the report (the example is one page's row in the Search Console Links report, while Ahrefs counts referring domains), whether the links are followed, and whether the count includes links the site would have received anyway.
  The example behind this rule is one author's screenshot with the URL redacted, so the figure is unverified.
- Treat a "N clicks in 28 days" screenshot as unproven until it names the property, the date range, the query mix and whether the pages were already ranking.
  Search Console's congratulation email does not show which site earned the clicks.
  Clicks to an app site are not installs, so size a plan on the click-to-store-tap rate and the store conversion of the same app, not on clicks alone.
  The example behind this rule is one author's screenshot (450 clicks, Sep 30, 2026) with the property hidden, so the figure is unverified.
- Treat a vendor's citation study as marketing until it names who sells what, the sample size, the question set, whether answers came from an API or the consumer app, who classified each source and whether the run was single.
  The example is Outrank's benchmark (2026-10-20): 48 questions, one same-day run, a Claude model as the classifier, and a vendor that sells blog content at $99 a month.
- DR (Domain Rating) is an Ahrefs metric that shows the relative strength of a website's backlink profile.
  Google states that third-party authority scores do not come from Google, so do not make a DR threshold a requirement.
- Do not select link sources by DR or by a source's claimed monthly traffic.
  A source list sorted by DR or claimed traffic is a promotion list, not evidence that a link helps rankings, and one such list mixed DR 14 and DR 88 sites with no stated criterion.
  Record any DR or traffic number with its tool and date, because an Ahrefs traffic number is an estimate.

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
  A pattern an engagement post promoted (2026-10-21, income figure unverified) is one new page a night in a thin directory niche with affiliate links, run by an agent.
  Google's spam policies (read 2026-10-21) list "Using generative AI tools or other similar tools to generate many pages without adding value for users" and "Creating multiple sites with the intent of hiding the scaled nature of the content" as scaled content abuse.
  They add that not every affiliate site is thin, and that good ones add original reviews, testing and comparisons.
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
- <https://x.com/hridoyreh/status/2112072682854556143> (link source list, promotional and unverified, used only for the DR and backlink-claim cautions and the bounded sourcing step)
- <https://developers.google.com/search/docs/specialty/international/localized-versions> (hreflang rules, read 2026-10-21)
- <https://outrank.so/ai-citations> (vendor citation study, single run on 2026-10-20, read 2026-10-20)
- <https://outrank.so/free-blog> and <https://outrank.so/pricing> (vendor pages, read 2026-10-20)
- <https://x.com/tibo_maker/status/2112481939563438091> and <https://x.com/illyism> quoted post 2112377329284730977 (listicle recipe, unverified outcome)
- <https://x.com/DanKulkov/status/2112178737785819183> (video transcript source for the seed plan, unverified)
- <https://x.com/minosdevs/status/2112189288314020303> (six-step loop, author sells a course, unverified)
