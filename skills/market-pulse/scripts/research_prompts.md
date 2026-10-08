# Research Agent Prompt Templates

## Agent 1 — App Store Intelligence

```text
Research the App Store/Play Store landscape for {CATEGORY} apps.

Use `web_fetch` to gather data. Search these URLs:
- https://apps.apple.com/us/charts/iphone/{category-slug}
- Google "top {category} apps 2025 2026 site:sensortower.com OR site:data.ai OR site:appfigures.com"
- Google "best {category} apps iOS" for editorial lists

For the top 20 apps, collect:
- App name, developer, App Store rating, review count
- Pricing model (free/freemium/paid/subscription)
- Price points (if paid/subscription)
- Last updated date
- Estimated downloads (from review count × 100-200 multiplier, or public data)

Write results as JSON to {OUTPUT_PATH}/app-store-data.json

Also note:
- Category saturation (how many total apps?)
- Average rating in category
- How many are actively maintained (updated in last 6 months)?
```

## Agent 2 — Competitor Deep Dive

```text
Deep-dive the top 10 competitors for {APP_NAME} in the {CATEGORY} space.

For each competitor:
1. Fetch their App Store page via web_fetch
2. Extract: full feature list, pricing tiers, review highlights (positive + negative)
3. Check Product Hunt (web_fetch "site:producthunt.com {competitor name}")
4. Check Reddit sentiment (web_fetch "site:reddit.com {competitor name} app review")
5. Note their key differentiator and biggest weakness

Also analyze:
- Feature gap matrix: what does {APP_NAME} have that others don't?
- What are the most common user complaints across all competitors?
- What features do users consistently request?

Write results to {OUTPUT_PATH}/competitors.md
```

## Agent 3 — Market Sizing

```text
Research the market size for {CATEGORY} apps/software.

Search for:
- "{CATEGORY} app market size 2025 2026" — look for Statista, Grand View Research, Mordor Intelligence public summaries
- "{CATEGORY} software market growth rate"
- Google Trends data for key category search terms

Determine:
- Global TAM (total addressable market) for the category
- Growth rate (CAGR)
- Geographic breakdown (US, EU, APAC)
- Platform split (iOS vs Android market share in this category)
- User demographics (age, income, behavior patterns)
- Seasonal trends (when do downloads spike?)

Write results to {OUTPUT_PATH}/market-sizing.md with sources cited.
```

## Agent 4 — Monetization Research

```text
Research monetization benchmarks for {CATEGORY} apps.

Search for:
- "app subscription benchmarks {CATEGORY} 2025" site:revenuecat.com OR site:adapty.io OR site:superwall.com
- "{CATEGORY} app ARPU conversion rate"
- "indie app revenue {CATEGORY}"

Determine:
- % of apps that are free / freemium / paid / subscription
- Average subscription price (monthly and annual)
- Typical free-to-paid conversion rate
- Average ARPU (average revenue per user)
- D1/D7/D30 retention benchmarks for the category
- Churn rate for subscription apps in this category
- Common paywall strategies (when/where in the user journey)
- Average LTV (lifetime value) if available

Write results to {OUTPUT_PATH}/monetization.md with sources cited.
```
