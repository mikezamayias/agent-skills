# Distribution channel notes

Read this before choosing paid social, creator, community or influencer channels in step 6.
Platform and vendor facts were checked on their official pages on 2026-10-17.
Founder numbers are single accounts, not benchmarks, and none is a target.
Prices and policies change, so re-check the linked page before relying on one.

## Paid social

- Two indie founders (October 2026) report that Meta converted better than TikTok for a paid app.
  One ranks Meta ads first "by far" for an app near $60K total revenue.
  The other gives higher intent, a better demographic and higher willingness to pay as reasons.
  Treat this as a reason to test Meta first, not as a ranking.
- Meta offers two optimization choices for app ads.
  Install optimization suits the goal of lowest cost per install.
  App event optimization still runs app install ads but delivers them to people likely to complete a specific in-app event, such as a purchase, and is billed per impression, like install optimization.
  Pick by goal and test the event choice against installs on a small budget.
- On iOS 14.5+, Meta app promotion campaigns run only in Advantage+ setup, with one ad set per campaign.
  Each campaign picks one attribution method, either Aggregated Event Measurement (AEM, Meta's own attribution) or SKAdNetwork (SKAN, Apple's privacy-preserving install attribution).
- AEM needs an eligibility check per app event in Events Manager (Datasets, Settings, Setup tasks for iOS app events, Check app events eligibility), so the app must already send events to Meta through its SDK or the Conversions API.
- SKAN results reach Meta at least 24 hours late, are dated by when Meta receives them, and are aggregated at campaign level.
  Ad set and ad results may be statistically modeled.
  Short test windows and per-creative reads on iOS are therefore unreliable, so judge a creative test on a longer window or on your own purchase data.
- A message test can instead send the ad to the app's own web page, not to the store, and read the result in the page's analytics, which has no SKAN delay or modeling.
  Give each ad variant its own `utm_campaign` or `utm_content`, and set `utm_medium` to a paid value such as `paid_social`, because Plausible counts a visit as Paid Social only when the medium matches a paid pattern (Plausible docs, "Top referrers", read 2026-11-03).
  Read the store-click rate per variant (see `app-landing-page`), and treat it as interest, since it does not measure installs or purchases (inference).
  That Meta accepts an external URL with UTM parameters on an app promotion ad was not read on Meta's pages, so confirm it in Meta's help first.
  One founder plans such a test, a few message angles on a first Meta ad, and reports no result yet (LinkedIn, 2026-11-03).
  The post does not say whether the ad goes to a page or to the store, so this route is a suggestion and not what that founder does.
- The Meta pages above partly date from 2021 to 2023, and Apple is moving from SKAdNetwork to AdAttributionKit, so re-check the setup steps.
- TikTok's own guidance is to add 3-5 new creatives about every 7 days or when fatigue appears, and to run 5-7 varied creatives with weekly refreshes.
  Its fatigue signals are click-through rate falling while frequency rises, impressions falling, and cost per acquisition rising or return on ad spend falling.
  Add creatives to the existing ad group, because TikTok says opening new accounts does not help when creative, targeting, bid and budget stay the same.
  TikTok states budgets as multiples of target cost per acquisition and says to raise budget by no more than 50% at a time.
  The fatigue figures are vendor data, and the Fatigue Index guide covers web campaigns more than app installs.
- Before raising a budget, write down what you will do if CPA holds, if it passes your line and if it keeps improving.
  Keep the next creatives in a test campaign before the current winners fade, and move only proven ones into the scaling campaign.
  One founder's article (October 2026, single report, no data) says the account lost its winners at about $20K a month with ten creatives in one ad set.
  On iOS, Meta app campaigns allow one ad set per campaign (see the Meta bullet above, from Meta's help pages, not re-read on 2026-10-25), so a test and scale split means two campaigns (inference).
- Install a mobile measurement partner (MMP, a third-party attribution provider) before TikTok or Meta spend.
  Singular's Free plan costs $0 per conversion with no card, covers up to 15,000 paid conversions, and includes paid-campaign attribution and SKAN.
  AppsFlyer's free Zero plan measures clicks and impressions only and does not measure attribution, so attribution starts on its paid Growth plan, billed per conversion.
  New AppsFlyer accounts begin on a Welcome plan with 12,000 free measured conversions or one year of access, whichever ends first.
- Before spending, read the competitor's ads in the Meta Ad Library (read 2026-10-20).
  Meta's pages returned 403 to fetch, so the scope below comes from search snippets of Meta's help page and library page, so re-check it there.
  Search covers ads that are currently active.
  Inactive ads are searchable only for issue, election or politics ads, ads that ran in the EU in the past year, and ads that ran in the UK in the past year after 2025-07-01.
  The library therefore does not show every ad a competitor has run, and an empty result is unknown, not proof of no ads.
  An ad that keeps running suggests the advertiser keeps paying for it, which is a weak signal and not proof that it is profitable.
  Blogs call 45, 60 or 60-90 days a winner, a folk rule with no Meta or study source, so set no day threshold.
  Many new ads with several variants each suggests the advertiser is testing creative volume.
  Quote the hooks of the longest-running ads and test those angles in your own creative.
  Never copy their footage, copy or brand assets.
  One founder reports briefing a creator to remake a competitor's ad one for one with his own app.
  Do not do that.
  Copy the structure and angle, such as the hook order and the proof shown, and re-shoot with your own words, footage and claims.
  That legal point is an inference and was not checked against a source.
  A library read is a sample, so write unknown for any library you did not check.
- Treat an ad test as a message test first.
  Write down the angles before spending, such as an arithmetic hook, a proof of the app UI or a pain statement, and the one metric that decides, for example store-click rate or cost per install.
  A winner then goes to the store page by a screenshot caption, the first screenshot or a custom product page that the ad links to (`apple-ads.md` step 8 has the Apple Ads form).
  A product page optimization test cannot run on a custom product page (Apple, via `asc-aso-audit`), so test a message on the default page only after the ad has chosen it.
  One founder (LinkedIn, 2026-11-03, a plan with no result) wants to test a few angles on a first Meta ad and reuse a winner on the App Store page, the website and a second app.

## Founder-on-camera and creator video

- Post the creative angles yourself on TikTok, Reels and Shorts before paying creators.
  One founder reports that this converted poorly but showed which content worked.
  Another films 5 to 10 short videos a day, ranks the organic posts by hold rate and skip rate, and runs only the winners as paid ads.
  That founder's definitions of those two rates were not checked against TikTok or Meta.
- Hire creators after a format has won.
  The same founder reports early paid creator videos at about $100 for about one download.
- One founder (October 2026, an app about a month old, no attribution tool shown) posts three videos a day on one Instagram account and says an old two-week-old video resurfaced and brought about 190 downloads in a day.
  His tiles show +191 new customers that day, and the cause is unverified.
  His screenshot lists three Reels at 141K, 921K and 117K views.
  Check an old post's installs one to two weeks after posting before you retire its angle, and log installs by post date so a late spike can be traced.
- Instagram's published ranking explainer (2023-05-31, read 2026-10-24) lists reshare, watch to the end, like and audio page visits as Reels signals, and says muted or majority-text Reels are shown less.
  It does not list replays, so check that a Reel is not mostly text and has audio, and treat a claim that rewatches push a video as unverified.
  The same page also lists reels that have already been posted on Instagram and reels with borders among those it makes less visible, so a re-post of an unchanged video may be shown less (read 2026-11-05, inference).
  One founder (November 2026, one Instagram account, no numbers shown) says re-posting their best video with a new first line gave it 10x the views and calls it their favourite trick.
  That claim is unverified and the page's wording is three years old, so test it once: re-post one winner with a different first line, delete or archive nothing, and compare views and installs by post date before repeating it.
- A different founder claims 1.5 million downloads in about three days for under $5,000 (October 2026).
  The claim is unverified, with no store data, spend breakdown or cost per install shown, and it comes from a video that promotes the founder's own paid creator-research tool.
  The account that amplified it also sells a research tool, so read it as one founder's account and never as a benchmark.
  He says he started with three to five creators, texted each daily with replies inside an hour, and would not start with 30 to 50 until a format works.
  His reason is that a small group keeps quality control and experiment results readable.
- No study checked compares founder-on-camera video with paid creator video.
- Mass faceless slideshow accounts are reported as cheap but low converting.
  One founder calls them "insanely cheap" with low converting views, and a reply reports decent views with almost no installs.
  Another uses them for organic and international reach and says offshore slideshow creators delivered bot views and the wrong countries, so check each creator's audience country and view quality before paying.
  For how to write a slideshow, see [tiktok-slideshow-format.md](tiktok-slideshow-format.md).
- One X growth account (2026-10-25, consulting seller, no result shown) advises 3 to 5 "clippers" posting 3 to 5 times a day as the fastest route to $1,000 or more a week.
  The author defines clippers as people who post content on their own accounts promoting your app.
  The same word also means people who cut podcasts into short clips, so search for the first meaning with "paid posters" or "slideshow creators".
  The post names no pay, no count of posts per clipper, no app, no installs and no revenue, so it is an unsourced income claim and not a result (single report).
  Run any version of it as a test with a fixed budget, track installs and revenue per clipper account, and apply the disclosure and spam rules in this file.
- Posting your own AI or cartoon slides through a scheduler tool is a separate cost from paying creators, and the tools sell themselves with account-level view claims.
  One scheduler's page quotes "2.2M views from 90 posts in 60 days" from a single user, with no install data (vendor claim, unverified, vendor page read 2026-10-23).
  Its pitch of hundreds of automated slideshows runs into the spam rule on the next line, so read that rule before scheduling volume.
- TikTok allows multiple accounts but classes automation that runs many accounts, and repetitive content, as spam.
  Penalties include account bans and limited reach.
- An agent-run set of AI creator personas, one per buyer segment with its own accounts, is promoted in an X article by the maker of the tools it uses (2026-10-23, single report, no follower, view, install or sale result shown).
  Before building one, check each point against the rules in this file.
  1. Several accounts that post agent-made videos daily meet the TikTok spam rule above.
     The article's safeguards (an "AI creator" bio line, scheduling at least 24 hours out, a daily human review of the queue) are the author's choices, and no platform text read accepts them.
  2. Realistic AI people likely need the AI label (see the TikTok slideshow notes), and the label belongs on every post, not only in the bio.
  3. A persona that says it uses a product describes an experience that did not happen.
     16 CFR 465.2(a) bars a business from creating a consumer testimonial that "materially misrepresents, expressly or by implication" that the testimonialist exists or "used or otherwise had experience with the product" (Cornell LII, read 2026-10-25).
     The rule text does not mention AI, so whether a persona's passing mention counts is an inference, and a bio disclosure does not obviously cure an experience claim.
     Keep scripts to what the app does and never to what the persona felt or achieved.
  4. The article itself says to avoid regulated and trust-dependent categories (medical, legal, financial) and bans health, income and before and after claims.

  Our own rule, not the article's: test one persona with a human review of every post before adding a second.

- One founder (October 2026, one account, no measured effect) reports a seven-day warm-up before the first post, with two sessions a day at random times.
  Days 1 and 2 only scroll For You for 15 to 20 minutes.
  Days 3 and 4 search about 10 niche terms and watch each video 12 seconds to 1.5 minutes.
  Days 5 and 6 like about 8% of videos after long watches.
  Day 7 posts the first slideshow, then at most one post a day.
  This is unverified and the author promotes his own automation offer next to it.
  Do it by hand only.
  Automating account activity falls under the spam rule above and risks a ban of the account.
- Running the automation on real phones does not change the spam rule above.
  A popular open-source phone farm drives real iPhones through WebDriverAgent to schedule TikTok sessions and posts, and its README gives no warning about TikTok's rules.
  Two users in its thread report fresh accounts warmed for days that stayed at zero views (single reports, no method), and no source shows a positive result.
- Posting through a scheduler API has its own limit that TikTok publishes.
  An API client that TikTok has not audited can only post as private (`SELF_ONLY`), for at most 5 users in a 24 hour window, and TikTok lists "a utility tool to help upload contents to the account(s) you or your team manages" as not acceptable for an audit (TikTok content sharing guidelines, <https://developers.tiktok.com/doc/content-sharing-guidelines>, read 2026-11-02, verified).
  A client can leave at most 5 pending shares per user per 24 hours, and a photo post takes up to 35 photos (TikTok photo post reference, <https://developers.tiktok.com/doc/content-posting-api-reference-photo-post>, read 2026-11-02, verified).
  So a self-built poster cannot publish publicly, and a scheduler that does is posting through its own audited app (inference).
- The same founder creates one TikTok account per app before the store approves the app, so format testing starts before launch (author reply, one account).
- Organic videos that say "search the app name" give store downloads that no tool ties to a video (inference).
  Compare weekly first-time downloads before and after each post, so a view count is never read as installs.
  Apple gives each custom product page its own URL, and App Analytics shows product page impressions, downloads, redownloads and conversion rates for each custom product page (<https://developer.apple.com/app-store/custom-product-pages/>, read 2026-11-01).
  So one custom product page per video or creator, linked where the platform allows a link, gives downloads per page.
  That Apple page describes no breakdown by source for one page's URL, so one shared page URL does not separate the places it was posted.
  Whether a given platform allows the link was not checked, and no promo code route was checked.
- YouTube announced on 2026-10-01 that Shorts recommendations will give less reach to channels that mainly re-upload other creators' clips without significant changes.
  No effective date was given.
  Clips stay eligible when the uploader adds original commentary, unique edits or storytelling.
  A voiceover that only describes the screen, minor edits and template-based bulk changes do not count.
- YouTube's separate reused-content rule for monetization still applies to Shorts compiled from other social sites, even with the original creator's permission.

## Link in bio and in-app browsers

One founder's claim (2026-10-20) with one screenshot, no loss rate.
Nothing here is tested.

- TikTok and Instagram open bio links in their own in-app browser.
  A store link opened there can fail with "Action can't be completed", shown in one screenshot on a TikTok in-app browser.
- Point the bio link at a page you control.
  Detect the in-app browser and show an overlay with an arrow to the ••• menu and the text "Tap ••• → Open in browser".
  Once the page runs in Safari or Chrome, redirect by device to the App Store or Google Play, keep a visible Download button as a backup, and show a simple web page on desktop.
- The source calls this a guaranteed redirect.
  A link-routing vendor's page (read 2026-10-21) says TikTok cannot be redirected automatically and needs a guide to TikTok's own "Open in browser" option, so the overlay is required there and "guaranteed" is not supported.
  That vendor sells the same service, so its page is a secondary source.
- Example brief from the source, output untested and the Android auto-open step unverified:
  "Build a mobile link-in-bio page that detects TikTok/Instagram's in-app browser and shows a full-screen overlay with an arrow pointing to the ••• menu and the steps 'Tap ••• → Open in browser' (on Android, try auto-opening Chrome first). When opened in Safari or Chrome, redirect straight to my App Store or Play Store link (detect the device), with a big Download button as a backup."

## Games

Every item here is an unverified single account.
Apply the TikTok automation and spam warning above to any plan that automates posting.

- A game ad is gameplay video of the shipped game, with the single most satisfying 3 seconds first (@RobbyFrank, reply to a post by @alexcooldev, 2026-10-19).
- A common structure is fail-then-hook: a caption such as "THIS LOOKS EASY...", then a visible mistake, then a store card with the app name and a search prompt (a sample video in a reply by @solotechdev, watched by us).
- Produce many variants and let installs pick the winner. The "20 versions" figure has no source.
- An agent can record gameplay and cut clips for organic channels, but the account that says so had not started.
- A portfolio of games can advertise each other, and some studios historically split ownership with rising games to cross-promote (@dayonefoundry, names Ketchapp). Check Apple's rules on cross-promotion inside apps before adopting it.
- Never show gameplay, levels or features in an ad that the shipped game does not have.
  Apple App Review Guidelines 2.3.1 (`developer.apple.com/app-store/review/guidelines/`, read 2026-10-23) say "marketing your app in a misleading way, such as by promoting content or services that it does not actually offer ... whether within or outside of the App Store, is grounds for removal of your app from the App Store or a block from installing via alternative distribution and termination of your developer account".
  Guideline 2.3.4 says app previews "may only use video screen captures of the app itself".
  Apple Advertising Policies (`searchads.apple.com/policies/`, last updated February 26, 2025, read 2026-10-23) say in 1.5 "All claims made in ad content must be adequately substantiated" and in 1.6 "Ad content may not be misleading".
  The Meta side is unverified.
  `transparency.meta.com/policies/ad-standards/` loads only a JavaScript shell without the policy text, and the misleading-content subpages we tried returned 404 (read 2026-10-23), so no Meta quote is made here.

## Creator marketplaces

- The same founder says to find the first creators among untapped niche creators and college students under 2,000 followers, then walk their following networks.
  He gave no rate when asked, and he gave the tip after saying he uses his own tool for this search.
- LightReel (read October 2026), a creator-research tool, lists one Pro plan at $199 a month.
  Its pricing page offers a 3-day free trial with $0 due today and a 7-day money-back guarantee with no stated conditions.
  The page does not say what happens when the trial ends or when the 7 days start.
- SideShift (read 2026-10-17):
  - The Starter plan is $299 a month month to month or $210 a month billed annually.
    Growth is $349 billed annually or $499 monthly.
    Scale is $699 billed annually or $999 monthly.
  - The subscription covers the software only, and creator spend sits in a separate wallet.
  - Fees are non-refundable and cancelling gives no prorated refund.
    Unspent wallet funds belong to the client.
  - The default creator license is worldwide and perpetual, becomes irrevocable after payment, and covers paid social ads, whitelisting, TikTok Spark Ads and Meta partnership ads.
    A campaign agreement can narrow it, and the terms give a 90-day term as an example.
    Set the usage period and paid-ads rights in the campaign agreement before the first brief.
- Noise (read 2026-10-17):
  - The Standard plan is $0 a month, and the brand pays per view at a price per 1,000 views that it sets.
  - Noise keeps a percentage of that price as a platform fee and does not publish the percentage.
  - The Unlimited plan is $99 a month, credited toward campaign spend, and also acts as a minimum spend.

## Organic search

- Organic search via an app landing page, blog and Search Console is a slow, free-to-start channel with no spend to refresh.
  Treat any "simple marketing" claim for it as a method and not a result unless the author gives installs or revenue, and check whether the author sells a course that teaches the method.
  One source of this loop sells a EUR 349 course (the author's site, read 2026-10-20) and gave only a click count with the site hidden.

## App Store editorial featuring

Evidence is Apple's "Getting featured on the App Store" and "Nominate your app for featuring" pages, read 2026-10-24.

- Apple lets any developer nominate an app, an update or new content for editorial consideration, free, in App Store Connect under the app's Featuring, Nominations.
  The roles that can submit are Account Holder, Admin, App Manager and Marketing.
  Apple says there is "no checklist of requirements", so a nomination is a request and not a channel to plan revenue on.
- Types are App Launch (a new app or a pre-order), App Enhancements (new features or major updates) and New Content (new content, offers or events).
  Use one nomination per real change and do not file one for something that has not shipped (inference, not an Apple rule).
- Lead time: Apple's nomination help recommends at least 3 weeks, and its Getting featured page says at least 2 weeks and up to 3 months ahead for wider consideration.
  Use 3 weeks as the floor.
- Describe the specific change, its purpose and its priority, since Apple asks for specifics.
  Use Helpful Details for facts about the app or team, such as accessibility, inclusivity and priority.
  One founder advises writing the story of who built it and why (single report, not Apple's guidance).
- Attach an In-App Event only when one is approved or published, because Apple's help only allows that.
- Apple's featuring factors are user experience, UI design, innovation, uniqueness, accessibility, localization and product page quality, so check the product page and localizations before nominating.
- Log each nomination's outcome (date submitted, type, publish date, featured or not, installs in the week after) so the channel is judged on results.
  The one public how-to found reports no result.

## In-App Events

Source: Apple's In-App Events page, developer.apple.com/app-store/in-app-events/, read 2026-10-25.

- An In-App Event is a card for a time-limited happening in the app.
  Apple says people find events on the product page, in search results, by searching for the event itself, and in editorial selections.
- In search, the event card appears next to the app for people who have downloaded the app, and people who have not downloaded it see screenshots.
  So an event re-engages current and past users in search.
  It reaches new users only when they search for the event or find it elsewhere on the App Store (inference from Apple's wording).
- An event can last up to 31 days and be promoted up to 14 days before it starts.
  Up to 15 approved events can sit in App Store Connect at once and up to 10 can be published.
  Events can be submitted for review without a new app version.
- App Analytics in App Store Connect shows downloads per event and acquisition sources.
  Log event name, dates, source and installs for each event, so the channel is judged on results.
- Apple says good events are challenges, competitions and special content launches (Apple's In-App Events page, read 2026-10-30).
  It says repetitive activities such as daily tasks or rewards, price promotions that add nothing new, and general awareness promotions are not good candidates.
  So a plain "now on iPhone Duo" layout fix may not suit an event, and the "Major Update" badge is for significant new features, content or experiences and not for UI adjustments or bug fixes.
- Limits: name up to 30 characters in title case, short description up to 50 and long description up to 120, both in sentence case.
  The name must be the event's actual name and not a call to action.
  No specific prices, no unverifiable claims such as "the best" or "#1", and no all capitals or repeated punctuation.
  Apple says to avoid text and logos in the media and not to add borders or gradients, because Apple applies crops and gradients.
- Apple says event videos autoplay and repeat, so build a seamless loop.
- David Barnard, a RevenueCat advocate, reports building a "Major Update" event for iPhone Duo support in about 10 minutes with an AI agent and a mockup tool, partly to improve the app's chances of being featured (single report, 2026-10-29).
  Barnard says the agent's copy was poor and needed rewriting, so a person writes the event text.
  Barnard also says Apple could reject something other apps got approved, which is why other apps' events are not a rule.
- Judge the effort by search presence and featuring odds.
  The same person says an app with no search presence that will never be featured may find it a waste (single report).

## AI assistant directories (ChatGPT plugins)

Evidence is OpenAI developer docs read 2026-10-21 for the requirements and replies on X for the review waits.
Revenue and uplift claims are unverified.

- ChatGPT apps are now submitted as plugins backed by a public MCP (Model Context Protocol) server.
- Treat a listing as availability and not distribution, the same as a store listing.
  OpenAI's review page says developers cannot request enhanced distribution.
  Replies to one founder's launch ask how users discover the plugin and none is answered.
- One post (2026-10-20) claims "~900M weekly users for free".
  That figure matches an aggregator report for February 2026 and is stale or unverified, and no OpenAI page was read for a current number.
- A founder reports "500K in ARR this week" after a plugin launch, shown on a chart with no axes (October 2026).
  The same founder says he is selling the platform, so the plugin may not be the product.
  Read it as unverified until the author shows installs, sources or revenue by channel.
- The same post claims "+50-200%" income for agency clients, with no base number, client or period.
  This is unverified.
- A revenue chart with no axes, dates or source, or an uplift range with no base number, is not evidence.
  Ask which customers, over what period and from what base before counting it.
- Review is the schedule risk.
  OpenAI's review page gives no time and asks developers not to contact support for expedited review.
  Several replies report waits of 4 days, 2 weeks, 3 weeks and over a month, so plan for weeks and never promise a client a date.
- Requirements read on OpenAI's submission and review pages are a verified publisher identity for the publish name, a public HTTPS MCP server, website, support, privacy policy and terms URLs, a demo account that needs no MFA, a domain token at `/.well-known/openai-apps-challenge` returned as plain text, exactly 5 positive and 3 negative test cases, and a demo recording URL.
- Common rejections are connection or login failure, failed test cases, data not disclosed in the privacy policy and annotation mismatch.
- A plugin must not exist primarily as an advertising vehicle and trial or demo plugins are not accepted, so a lead-gen shell is a rejection risk.
- Commerce inside a plugin is limited to physical goods, with no subscriptions, plans or direct checkout links, though signing in to an existing paid account is allowed.

## AI assistant directories (Google Connected Apps)

Evidence is Google's blog post of 2026-10-28 and the Connected Apps Platform developer pages, read 2026-11-01.
Claims about reach and revenue in X posts are unverified.

- Google launched a preview of the Connected Apps Platform for the Gemini app and Search.
  Developers register a cloud-hosted MCP (Model Context Protocol) server, or an Android app through the Jetpack AppFunctions SDK, in the Google Connected Console and submit it for review.
  Access is by interest form and opens in phases, so a client cannot count on a listing date.
- Treat a listing as availability and not distribution, as with ChatGPT plugins.
  Google's pages state no user count and no ranking rule.
  One post's "4.3 billion users" has no Google source, and the blog says Search surfacing starts "in the coming weeks" after the Gemini launch, which contradicts the same post's "Gemini will be live imminently".
  An app can be called by name or with an @ mention and then stays in context for the session.
  How an app is chosen without a mention is not documented, so do not promise organic discovery.
- A mobile app does not get listed by being a mobile app (inference).
  The default path for iOS, Web and cross-platform (so also Flutter) is a public HTTPS MCP server backed by an API the developer owns.
  AppFunctions is Android only, runs on the device, and needs a native Jetpack integration.
- Requirements read on the developer pages: OAuth 2.1 with PKCE, authorization server metadata at a `.well-known` URL, dynamic client registration or a manual client id and secret, Google's redirect URLs allowlisted, server instructions that describe the domain, `readOnlyHint` and `destructiveHint` tool annotations, typed schemas, a privacy policy and help pages that explain data deletion.
- Policy bars that matter for a client: no third-party advertising or promotion in tool output, no wrapping or repackaging third-party APIs the developer does not own, no similar duplicate apps, no data sale, no tool descriptions that steer the model to pick the app over another, no tool that references other tools, and no app that consistently errors, times out or fails authentication.
  So a lead-gen shell, an ad vehicle or a thin wrapper around someone else's API is a rejection and suspension risk.
- Review is the schedule risk and Google gives no review time.
  Plan for a deployed, monitored server (Google shows traffic, latency and error rates in the console), because failing calls are a policy violation and not only a quality issue.
- A tool that changes state needs the confirmation flag in the console and a `destructiveHint`.
  One operator (single report) keeps sending an email as a separate permission that stays with the human.
- Do not run `npx @modelcontextprotocol/inspector` (the guide's validation step) outside the code-gate remote-code rule.

## AI assistant directories (Claude Connectors directory)

Evidence is Anthropic's Claude documentation pages and Software Directory Policy, read 2026-11-08.
Revenue and customer claims in X posts are unverified.

- Anthropic's directory lists plugins and MCP (Model Context Protocol) connectors for claude.ai, Claude Desktop, mobile, Claude Code and Cowork.
  Anyone on a paid Claude plan (Pro, Max, Ultra, Team or Enterprise) can submit at the developer portal, there is no partner program, and a free account cannot.
- A connector is a remote MCP server reachable over HTTPS.
  A local server cannot be listed on its own, and a skill is not a submission type, so put skills in a plugin bundle from a public GitHub repository.
  For your own product Anthropic advises two submissions, the server as a connector and a plugin bundle whose skills teach Claude to use it.
- By default a connector is scanned automatically and listed as Community, which Anthropic describes as screened and not reviewed in depth.
  Anthropic may escalate one to Verified review, where a reviewer tests each tool, and there is no application for the Verified label or for placement.
- Review time is not fixed.
  One founder reports approval in half an hour and says the queue is now longer (single report, X, 2026-11-07), so never promise a client a date.
- Only a directory listing makes a connector discoverable inside Claude, and every listing is eligible for in-chat Suggested Connectors, where Claude can recommend it when relevant.
  Anthropic does not say how often or on what ranking.
  Listing in the open MCP Registry does not surface a server in Claude.
- Review rejects a single tool that takes both safe and unsafe HTTP methods, a tool without a `title` and a `readOnlyHint` or `destructiveHint`, and tool descriptions that promote products and services or tell Claude how to behave.
  A listing is therefore not a place for sales copy in tool text, and the same lead-gen shell warning as for ChatGPT plugins and Google apps applies.
- A published connector's dashboard shows health and usage by tool, measured only on traffic from Claude surfaces, computed daily with up to 24 hours of lag.
  Rows with fewer than 5 calls are omitted.
  Use it to see whether Claude calls the server, and use the product's own signup data to see whether that turns into customers.
- One founder who runs three listed connectors reports "multiple customers a day" from Claude (X post, 2026-11-07).
  The evidence is three $19 trial-start alerts in one day with a free-text "heard about us" answer of "Claude", and two of the three show "Direct" as the traffic source.
  The founder's portal shows 297 accounts used one connector in 30 days, 15 another and 0 the third.
  Read it as one self-reported day with trials and not paid conversions, from a seller of the products shown (single report, survivorship).
  Do not use it as a rate, and do not treat a listing as distribution (inference from the policy pages above).

### Siri AI watch item

Evidence is Apple's news post of 2026-11-03 (<https://developer.apple.com/news/?id=gdk2umrf>) and the Siri AI Developer Preview page (<https://developer.apple.com/documentation/appintents/siri-ai-developer-preview>), read 2026-11-08.
Claims about reach and a new channel in LinkedIn and X posts are unverified.

- Apple opened a Siri AI Developer Preview in the iOS, iPadOS, macOS and visionOS 27.3 betas.
  An app takes part by exposing App Intents as tools, optionally with app skills that guide Siri through several actions, and by showing results as its own card snippet.
  There is no directory, listing or review for this yet, so treat it as engineering work and not as a listing to apply for.
- It cannot reach customers yet.
  Apple says the preview is not available to external TestFlight testers or to versions published on the App Store, that App Store submission opens in the spring, and that terms and usage policies will follow.
  So do not put Siri AI in a launch plan or a client forecast, and log it as a watch item.
- Do not promise organic discovery.
  A request made while the app is in the background must name the app, and the app can be left out of the request only in the foreground, while a Live Activity is active, or in a Siri conversation that already names it.
  A LinkedIn post that shows "order me a pad thai" with no app name leaves this out, and its own diagram names the app.
  How Siri chooses among several apps that can fulfil the same request is not documented on the pages read (a commenter asked and nobody answered).
- Availability is narrow.
  Siri AI needs an Apple Intelligence device, lists English, French, Japanese, Korean, Portuguese and Spanish, is unavailable in the EU on iOS and iPadOS, and Apple says some server-model features will carry daily limits and later a fee.
- Brand and measurement are open questions and not findings.
  Apple's card snippet carries the app's own branding, but the claim that it is the only brand surface is the post author's inference.
  One commenter says the app loses its usage signal when Siri runs the action, and Apple's pages read do not say what analytics an app gets from a Siri-run action (inference), so check this before counting Siri as a channel.
- Pair this with the ChatGPT, Google and Claude sections as one decision: expose a small, well-described set of actions once, and compare the channels by approval time, attributed sign-ups and revenue per sign-up as the other channels are.

## Channel choice by time horizon and business type

One operator's opinion with no data (Chris Raroque, video 2026-10-21).
He gives no performance numbers and says his own UGC (user-generated content, here paid creator videos) experiments lost far more money than they made.
Read it as a list to test, never as a ranking.

- Slow compounding at low effort: SEO, ASO (App Store optimization) and Reddit, about an hour a day.
  This is his own mix.
- Faster return for a consumer (B2C) app: UGC, SEO and Reddit.
  He says to post the content yourself first to learn what works before hiring creators, and credits this to unnamed UGC experts.
- Business (B2B) app: Reddit, SEO, LinkedIn and targeted email for some products.

## Communities

- Reddit does not ban self-promotion or multiple accounts.
  It bans spam, including mass-posting repetitive content for exposure or financial gain, and it asks accounts that mainly link to their own business to limit frequency or use ads.
  It sets no numeric ratio, and moderators set stricter limits per subreddit.
- Voting on the same post from several of your accounts is vote manipulation, and Reddit's rules also ban deceptively impersonating a person or entity.
  Never use a fake persona.
- One founder reports that answering "rate my face" posts with the app's own result converted well but got him banned often, and several replies report bans.
  Use the idea only where the subreddit's rules allow it.
- Discord's platform rules do not mention self-promotion.
  They ban unsolicited bulk messages and multiple unsolicited messages to other users, so repeated cold DMs are restricted.
  Each server sets its own promotion rules, so read them first.
  One founder reports low conversion but rare bans, and a reply says it suits tight-knit niches.
- LinkedIn's User Agreement bans using "bots or other unauthorized automated methods to access the Services, add or download contacts, send or redirect messages", so send first-contact messages by hand and not through a script or an automation tool (<https://www.linkedin.com/legal/user-agreement>, read 2026-11-01).

## X posts

### X link posts

One founder reports that a five-word X post with a bare link and no media reached 1.36 million views, 5,184 likes and 18,218 bookmarks (1.3 percent of views), from an account of about 3,500 followers (X post, 2026-11-01, counts read 2026-11-03).
Their analytics panel for the next 28 hours shows 113,452 visitors and 263,460 page views, 91 percent of visitors on the home page, 2.9 percent on the installation page, 5.6 percent on the components page and a 68 percent bounce rate.
The panel shows no referrer breakdown, so the 105,000 link clicks they claim and the share from X are not visible, and they withheld revenue.
It is one self-reported success, so do not read it as a conversion rate or as proof that X beats other channels (single report, survivorship, the author sells the product).
What carries over is the measurement plan, so before a link post goes out, set up page analytics with a referrer split and track one deeper step (an install, a signup or a purchase page) next to visits.
A spike gives most visitors only a home page view, so decide beforehand what the home page asks them to do.

### X launch posts

Evidence is X's open-source ranking repository (<https://github.com/xai-org/x-algorithm>, Apache-2.0, `README.md` and `home-mixer/params/param.rs` read 2026-11-03).
The repository is X's own publication and the code changes often, so recheck a number before relying on it.

- The For You feed takes candidates from followed accounts (Thunder), from an interest match on the viewer's history (Phoenix retrieval) and from accounts whose followers engage alike (SimClusters).
  It adds a shared list of popular recent posts, then ranks everything with one model.
- The score is the sum of a weight times the predicted chance that this viewer takes each action.
  The code lists reply 5, quote 5, share by DM 5, follow the author 4, share by copying the link 20, repost 1, like 0.66, not interested -52.3, mute -58.8, report -234 and profile click 0, and a mutual follow adds a reply boost of 15.
  X's own comment says these are multiples of predicted probability and not of raw counts, so one report does not cancel a fixed number of likes.
- Each post after an author's first is multiplied by a decaying factor, down to a floor, so posting five launch posts in a row lowers the later ones.
  Posts from accounts the viewer does not follow are multiplied by a factor below 1, and so are replies and reposts from followed accounts.
- A feed keeps the best-scoring post of one conversation, which means replies and branches of one thread, so a thread competes with itself.
  One agency article claims five separate posts lose four of them to this rule, but separate posts are separate conversations, so the cause is the author-diversity decay (inference from the filter code).
- Treat weights as a reason to design for the actions that carry weight, such as a post worth sending to a friend by DM or by copying the link, and not as a formula that counts likes.
- One agency article advises asking connections with an audience (investors, advisors, customers, beta testers, portfolio founders) to quote the launch before it goes out, ranked by reach into your customer and tiered so that the top 25 get a personal message with an example quote (single report, one agency, October 2026).
  A quote is a new post by another account, and the ranking code gives a quote weight 5, so it can reach that person's followers (weight verified, reach is inference).
  The article's "600 demos" and "1000x leverage" figures for one founder's launch have no evidence behind them.
- Do not coordinate engagement outside the feed.
  X's own code comment says actions on a post that the viewer was not served in the Home timeline, such as through a group chat, have no ranking impact (`home-mixer/params/param.rs` comment, read 2026-11-03).
  That comment is about mass blocking and reporting, so its scope as a limit on coordinated engagement is my reading (inference).

## Influencer deals

- A creator paid by revenue share or commission has a material connection.
  The FTC Endorsement Guides, which are enforcement guidance, treat pay per sale as compensation to disclose.
  The sources do not use the words revenue share, so applying it here is an inference.
- Put the disclosure inside the video, not only in the description or comments.
  Early in the video beats the end, repeating it is better, and saying it aloud while showing it on screen is best.
- An endorsement must reflect the endorser's honest experience, and advertisers should guide and monitor their endorsers.
  If the brand is obviously the influencer's own, no disclosure is needed.
  Having a creator present your app as theirs when it is not is a deceptive claim by inference from the Guides.
- One reply says large creators rarely take a profit-share deal without a prior scale result.
  Write the share, its term and the attribution method into the deal before the first post.

### Creator outreach

Reported method from one founder (George Lampropoulos, a podcast interview, self-reported, no data shared).
Treat it as a hypothesis.

- Ask the creator for their normal ad rate and pay it for a first post, then decide on any equity or share.
  If it fails, no ownership was given away.
- A cheaper first rate can be offered with a share only if the post works.
  Write the share, term and attribution into the deal first.
- Filter outreach to creators whose average views are at least 25,000 per post.
- Judge a creator by repeated high-view videos relative to follower count.
  The example is 8,000 followers with several 500,000-view videos over 300,000 followers with low engagement.
  Hand them proven hooks, competitor examples and screen recordings instead of asking them to invent a strategy.
  This is the opinion of one promotional article (2026-10-19), unverified.
- Write one brief per winning angle before paying a creator.
  A LinkedIn lead-magnet post (October 2026) lists these parts for such a brief: the app's value proposition, the audience, the use cases, a ranked list of content angles, opening hooks, a demo script, a story script, objection handling, a shot list, script variations and a production plan.
  This rests only on the contents page of a gated PDF that was not read, it has no performance data, and it is an inference from section titles.
  Take only the parts your logged posts back up, such as the winning hook and the objection that comments raised, and drop the rest.
- One founder's creator training note (a whiteboard photo in an X article, October 2026, single report, no results) asks creators to send the first post for review, keep a consistent style, show the app in 5 to 10 seconds, avoid making the whole post about the app, and film using the app on a second device instead of a screen recording.
  This conflicts with handing creators screen recordings above, so test both on a few posts and compare installs per post.
- Move to a call as soon as a creator replies, because rates and objections are easier to settle live.
- Target about 2 dollars per 1,000 views (CPM).
  One reported deal was 4 videos and 4 stories for 2,500 dollars with a creator averaging 400,000 to 1,000,000 views.
  Check any CPM against attributed installs and revenue, never views alone.
- A Cal AI co-founder says Cal AI bought fitness creator views at 50 cents to 3 dollars per 1,000 (October 2026, X post, no deal count or period).
  TechCrunch (2026-10-15) confirms the creator-heavy strategy and per-reach payout deals but gives no CPM.
  Treat the range as one operator's claim, and use it only as a sanity check for your own CPM.
- TechCrunch (2026-10-15, secondary report quoting the company, no contract seen) describes Cal AI deals as a payout for a stated scale of reach, with the creator posting until the reach threshold is met.
  Write the reach threshold and the end condition into the deal, and measure attributed installs against it.
- Founder-run outreach is cheaper to delegate once the script works.
  One reported hire is a virtual assistant at about 800 dollars a month following a written SOP.
- Do not buy followers, views or likes to make a brand page look established.
  One podcast guest advised it and the host noted it may break platform terms.
  16 CFR 465.8(b) makes it unfair or deceptive to "Purchase or procure fake indicators of social media influence that they knew or should have known to be fake and that materially misrepresent their influence or importance for a commercial purpose" (read 2026-10-21 on the Cornell LII copy, because the eCFR and FTC pages did not load).
  The FTC can seek civil penalties against knowing violators (FTC press release, August 2024).
  Build the page with real product demos and real creator collab posts instead.

## Sources

- <https://www.facebook.com/business/help/331612538028890?id=428636648170202>
- <https://www.facebook.com/business/help/651033805513936>
- <https://www.facebook.com/business/help/584603712214119>
- <https://developers.facebook.com/docs/app-ads/optimizing-your-app-ad>
- <https://www.facebook.com/help/259468828226154>
- <https://www.facebook.com/ads/library/>
- <https://www.law.cornell.edu/cfr/text/16/465.8>
- <https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials>
- <https://developer.apple.com/app-store/review/guidelines/>
- <https://ads.apple.com/app-store/policies>
- <https://www.askneedle.com/blog/meta-ads-library>
- <https://ads.tiktok.com/business/creativecenter/quicktok/online/tiktok_creative_accelerator/pc/en>
- <https://ads.tiktok.com/help/article/creative-best-practices?lang=en>
- <https://www.tiktok.com/community-guidelines/en/integrity-authenticity>
- <https://www.singular.net/pricing/>
- <https://support.appsflyer.com/hc/en-us/articles/115000136303-Account-management-plans-payments-and-billing>
- <https://support.google.com/youtube/thread/470890423/prioritizing-original-content-on-shorts>
- <https://support.google.com/youtube/answer/1311392?hl=en>
- <https://sideshift.app/pricing>
- <https://sideshift.app/terms-of-service>
- <https://sideshift.app/refund-and-cancellation-policy>
- <https://platform.getnoise.com/faq>
- <https://lightreel.ai/pricing>
- <https://x.com/Jibran_05/status/2111125040225735055>
- <https://x.com/GeorgeLampro20/status/2112452949561463082>
- <https://x.com/ericcosulea/status/2112214949736898809>
- <https://x.com/alexcooldev/status/2112218472709329038>
- <https://x.com/itsbongoo/status/2112401557946069175>
- <https://x.com/minosdevs/status/2112189288314020303>
- <https://x.com/MaxHirsch13/status/2112626598524465296>
- <https://x.com/devmelv/status/2112632240593158297>
- <https://x.com/chhddavid/status/2112113481495318700>
- <https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam>
- <https://support.reddithelp.com/hc/en-us/articles/204535759-Is-it-ok-to-create-multiple-accounts>
- <https://redditinc.com/policies/reddit-rules>
- <https://discord.com/guidelines>
- <https://www.youtube.com/watch?v=xt4GRXqVAAc>
- <https://developers.openai.com/plugins/deploy/submission>
- <https://developers.openai.com/plugins/deploy/app-review>
- <https://developers.openai.com/apps-sdk/app-submission-guidelines>
- <https://developers.openai.com/plugins/reference>
- <https://discord.com/safety/platform-manipulation-policy-explainer>
- <https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255>
- <https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers>
- <https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking>
- <https://www.linkedin.com/legal/user-agreement>
- <https://blog.google/innovation-and-ai/technology/developers-tools/connected-apps-one-place/>
- <https://developers.google.com/connected-apps>
- <https://developers.google.com/connected-apps/mcp>
- <https://developers.google.com/connected-apps/mcp/oauth>
- <https://developers.google.com/connected-apps/connected-apps-policy>
- <https://claude.com/docs/directory/publish.md>
- <https://claude.com/docs/connectors/building/submission.md>
- <https://claude.com/docs/connectors/building/review-criteria.md>
- <https://claude.com/docs/connectors/building/directory-vs-custom.md>
- <https://claude.com/docs/connectors/building/managing-your-listing.md>
- <https://claude.com/docs/connectors/verification.md>
- <https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy>
