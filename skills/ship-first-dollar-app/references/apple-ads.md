# Apple Ads first test

Read this before the first paid test of an iOS app.
Apple facts were checked on ads.apple.com and RevenueCat docs on 2026-10-14, and on Apple Ads, Apple developer and Singular pages on 2026-10-17.
The playbook is adapted from @frederickjames (post and video, October 2026, who reports $2.5k a month gross in about 30 days) and @xburak (October 2026, DevRel at Adapty, a subscription tooling vendor).

## Before spending

- Attribution works first.
  With RevenueCat, call `enableAdServicesAttributionTokenCollection()` after `configure` (iOS 14.3+), and match the RevenueCat setting to Basic or Advanced.
  Without App Tracking Transparency consent the token gives Standard data only.
- From September 2026, installs from ad groups with age or gender targeting return `attribution: false`, so leave audience age and gender unset.
- Onboarding and paywall funnel events are tracked, because the first $100 buys funnel data as much as installs.
- The product page converts.
  Paid taps land on it, so fix the first screenshots before raising bids.
- Attribution and funnel events ship in the launch build, so the first test can start in launch week.
  Apple lists downloads among its App Store search ranking factors, next to text relevance and ratings, and publishes no weights.
  One founder claims launch-week paid installs help ranking afterwards, which is unconfirmed.

## Credit and products

- Apple gives a one-time $100 (US) credit to a new account linked to App Store Connect with at least one app on sale.
  Non-USD accounts get the equivalent at Apple's daily exchange rate.
  Link the top-level account, because linking a campaign group does not apply the credit.
  Unused credit can expire under Apple's promo terms, which do not promise a notice.
- Apple shows no remaining credit balance.
  Open Account Settings, then the Billing tab, then Invoices, and open an invoice to see how much credit it used.
  Subtract the amounts applied from the initial credit to get what remains.
- The credit eligibility page (effective 2026-10-12) now covers Apple Maps ads only.
  It describes a one-time $150 Ads on Maps sign-up credit and a Grand Opening Promo, both for Maps ad spend with no cash value, and it no longer lists the App Store $100 credit.
  Do not read $150 as the App Store credit.
- A second $100 for Basic after using Advanced is reported by one developer and is not confirmed by Apple.
- Advanced charges per tap (CPT) and has keywords, audiences, custom product pages and the API.
  Basic charges per install (CPI), has no keywords, and caps at $10,000 per app per month.
  Use Advanced for a keyword test and Basic when a fixed CPI matters more than learning which keywords convert.

## Advanced setup for a first test

1. Campaign type search results, bid strategy Manage Bids.
2. One competitor campaign per territory group: the US alone, then tier 2 such as UK, Canada, Australia and Japan, then the rest of the world.
   Bid higher where the market pays more.
3. Keywords are the competitor's name and its spellings, all exact match.
   Apple's own structure is Brand, Category, Competitor and Discovery, with exact match everywhere except Discovery, which uses broad match and Search Match.
4. Turn Search Match off in exact-match campaigns, because it is on by default for Manage Bids.
5. Add the app's own name as a negative keyword in competitor and category campaigns, so the test does not pay for taps it would get free.
6. Audience: iPhone only for an iPhone app, customer type New users, no age or gender.
7. Start the max CPT at Apple's suggested bid, which Apple calls a reference point, and about $25 a day.
8. Use the default product page first, then a custom product page per campaign whose first screenshot says why this app over the competitor.
   Stay within App Review rules, so never imitate the competitor's page.

Apple says it does not investigate trademark claims about keywords, so bidding on a competitor's name is allowed on Apple Ads.

To read what a competitor's Apple ads say, try Apple's Ad Repository at <https://adrepository.apple.com/> (read 2026-10-20).
Apple publishes it under Article 39 of the Digital Services Act (DSA, the EU law on online platforms) and covers Apple-delivered App Store ads in EU countries and regions only.
Absence there is unknown, not proof of no ads, and it says nothing about the US or other regions.
Only a third-party blog lists the fields shown (creatives, keywords, placements, regions, impression dates), and retention is unknown.
Open one entry and check what it shows before relying on it.

Advanced runs in four placements: the Today tab, the Search tab, search results and product pages.
Custom product pages can be used in Apple Ads campaigns.
This first test uses the search results campaign type, and the checked pages do not say how a Search tab placement is bought.

## Reading the first week

- After 2 days with no spend, either nobody searches the term or competitors bid more.
  Raise the CPT in steps, or drop the term.
- Compare like with like.
  Cost per install goes against net proceeds per new user, and cost per paying user goes against net proceeds per paying user.
  Never pair a cost per paying user with proceeds per new user, because that overstates the loss.
- Keep a keyword while its cost per paying user stays below net proceeds per paying user within a payback window and spend cap set in advance, as in the keep-or-kill rule in the main skill.
- Do not judge by CPT, tap-through rate or installs.
  CPT is a direction signal only.
- Export the keyword report (taps, installs, average CPT, conversion rate, spend) and join it with paid conversions per keyword before scaling any keyword.
- Third-party keyword popularity tools are directional, because only Apple has the search data.
- Use a third-party popularity and difficulty score to choose which keywords to test, and the Apple Ads keyword report to decide, because the third-party score is not conversion data.
  One account (X post, October 2026) proposes choosing low-difficulty keywords this way and then testing them with a small campaign, with no test reported.

## When it will not work

- Saturated niches, such as calorie trackers, where many advertisers already bid.
  One developer reported about $10 per install with no trials from the free $100.
- Categories where large companies bid far above indie budgets, such as finance.
- One founder who reports $12,698 of revenue over 28 days for one app (October 2026) credits TikTok and Meta ads behind an attribution partner for the scaling, and treats Apple Ads as a floor of about $1k a month in the right niche.
  That is one account, not a benchmark.
- The best case is a niche with one large competitor growing on organic social, so people search its name in the App Store and see this app's ad first.

## Sources

- <https://ads.apple.com/app-store/help/billing/0032-apple-ads-promo-credit>
- <https://ads.apple.com/promo-terms>
- <https://ads.apple.com/app-store/help/campaigns/0056-structure-campaigns>
- <https://ads.apple.com/app-store/help/campaigns/0006-understand-search-match>
- <https://ads.apple.com/app-store/help/bids-and-budget/0062-set-and-adjust-bids>
- <https://ads.apple.com/app-store/help/apple-ads-basic/0001-compare-apple-ads-solutions>
- <https://ads.apple.com/app-store/help/ad-placements/0082-search-results>
- <https://www.apple.com/legal/intellectual-property/dispute-forms/app-store/>
- <https://ads.apple.com/credit-eligibility-criteria-and-limitations>
- <https://developer.apple.com/app-store/promote/>
- <https://ads.apple.com/en/app-store/advanced>
- <https://developer.apple.com/app-store/search/>
- <https://www.apple.com/legal/dsa/>
- <https://adrepository.apple.com/>
- <https://www.rplg.io/blog/apple-search-ads-ad-repository>
- <https://www.revenuecat.com/docs/integrations/attribution/apple-search-ads>
- <https://x.com/frederickjames/status/2110007318221885827>
- <https://x.com/david_attisaas/status/2109917304217604303>
