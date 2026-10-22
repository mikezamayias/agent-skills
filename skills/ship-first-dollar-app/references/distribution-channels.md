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
- The Meta pages above partly date from 2021 to 2023, and Apple is moving from SKAdNetwork to AdAttributionKit, so re-check the setup steps.
- TikTok's own guidance is to add 3-5 new creatives about every 7 days or when fatigue appears, and to run 5-7 varied creatives with weekly refreshes.
  Its fatigue signals are click-through rate falling while frequency rises, impressions falling, and cost per acquisition rising or return on ad spend falling.
  Add creatives to the existing ad group, because TikTok says opening new accounts does not help when creative, targeting, bid and budget stay the same.
  TikTok states budgets as multiples of target cost per acquisition and says to raise budget by no more than 50% at a time.
  The fatigue figures are vendor data, and the Fatigue Index guide covers web campaigns more than app installs.
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
- TikTok allows multiple accounts but classes automation that runs many accounts, and repetitive content, as spam.
  Penalties include account bans and limited reach.
- One founder (October 2026, one account, no measured effect) reports a seven-day warm-up before the first post, with two sessions a day at random times.
  Days 1 and 2 only scroll For You for 15 to 20 minutes.
  Days 3 and 4 search about 10 niche terms and watch each video 12 seconds to 1.5 minutes.
  Days 5 and 6 like about 8% of videos after long watches.
  Day 7 posts the first slideshow, then at most one post a day.
  This is unverified and the author promotes his own automation offer next to it.
  Do it by hand only.
  Automating account activity falls under the spam rule above and risks a ban of the account.
- The same founder creates one TikTok account per app before the store approves the app, so format testing starts before launch (author reply, one account).
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
  Apple App Review Guideline 2.3.1(a) (read 2026-10-21) says "marketing your app in a misleading way, such as by promoting content or services that it does not actually offer ... whether within or outside of the App Store, is grounds for removal of your app from the App Store".
  Apple Ads policies section 1.6 says "Ad content may not be misleading" (fetched as a summary only, so re-check the policy page).
  Meta's Advertising Standards page could not be read, so the Meta side is not verified.

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
