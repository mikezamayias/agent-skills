---
name: market-pulse
description: >-
  Run a market analysis for an app or product: competitor audit, market sizing, pricing benchmarks and MAU forecasts. Also produces revenue projections, ROI estimates and go-to-market recommendations. Use for market research, competitive or landscape analysis, revenue projections or app launch strategy.
---

# Market Pulse — App Market Analysis

Run a structured, parallelized market analysis that produces actionable intelligence.

## Output

A single markdown report per app at the user-specified path (default: `market-pulse/{app-name}.md`) containing:

1. **Executive Summary** — One-paragraph verdict
2. **Market Sizing** — TAM, SAM, SOM with sources and methodology
3. **Competitor Landscape** — Top 10 competitors with feature matrix
4. **Pricing Benchmark** — Category pricing norms, recommended strategy
5. **Projected Metrics** — MAU, DAU, retention, revenue (Month 1/3/6/12)
6. **ROI Analysis** — Dev cost estimate vs projected revenue, break-even timeline
7. **Channel Strategy** — Launch channels ranked by expected ROI
8. **Price Localization Strategy** — Top 10 markets, PPP-adjusted pricing, psychological thresholds, recommended custom price tiers per storefront
9. **Risk Matrix** — Top 5 risks with mitigation strategies
10. **Recommendations** — Prioritized next steps

## Workflow

### Phase 1: Gather Intelligence (parallel sub-agents)

Spawn 4 research agents simultaneously:

**Agent 1 — App Store Intelligence:**

- Search App Store/Play Store for top 20 apps in the category
- For each: name, rating, review count, price, IAP model, last updated, estimated downloads
- Use `web_fetch` on App Store search URLs and competitor pages
- Check sites: sensortower.com/blog, appfigures.com/resources, data.ai for public reports

**Agent 2 — Competitor Deep Dive:**

- For top 10 competitors: feature list, pricing tiers, review sentiment, App Store description
- Check Product Hunt launches, TechCrunch/press coverage
- Check Reddit/community sentiment (search subreddits relevant to the category)
- Note key differentiators and weaknesses

**Agent 3 — Market Sizing & Trends:**

- Research category market size (reports from Statista, Grand View Research, IBISWorld — use public summaries)
- Search for "[category] app market size 2025 2026"
- Check Google Trends for category keywords
- Identify growth rate and trajectory

**Agent 4 — Monetization & Pricing Research:**

- Research category pricing norms (% free, freemium, paid, subscription)
- Average subscription price in category
- Conversion rates (free→paid) benchmarks for the category
- ARPU benchmarks from public reports
- Check RevenueCat blog, Adapty blog for category benchmarks
- **Price Localization Analysis:**
  - Identify top 10 revenue markets for the category
  - For each market: local purchasing power (Big Mac Index or PPP ratio), psychological price thresholds (e.g. $X.99 vs round numbers), and cultural pricing norms
  - Compare auto-converted App Store prices vs locally-optimized prices for top 3 competitors
  - Note which competitors actively localize pricing (custom price tiers per storefront) vs rely on Apple/Google auto-conversion
  - Flag markets where auto-conversion creates awkward prices (e.g. ₺299.99 instead of ₺299 in Turkey)

### Phase 2: Synthesize (main agent)

After all 4 agents return, compile into the report structure:

**Market Sizing Formula:**

```text
TAM = Total addressable users in category × average annual spend
SAM = TAM × % reachable via target platforms (iOS/macOS/Android)
SOM = SAM × realistic capture rate (use 0.01-0.1% for Year 1 indie app)
```

**MAU Projection Model:**

```text
Month 1:  Launch spike × retention rate
Month 3:  Organic growth + channel acquisition
Month 6:  Steady state (organic + word-of-mouth)
Month 12: Mature state with seasonal adjustments

Assumptions:
- Launch spike: 500-2000 downloads (indie with no paid marketing)
- D30 retention: 15-25% (category benchmark)
- Monthly organic growth: 5-15% (if ASO is good)
- Conversion to paid: 2-5% (category benchmark)
```

**Revenue Projection:**

```text
Monthly Revenue = MAU × conversion_rate × ARPU
Annual Recurring = Monthly Revenue × 12 × (1 - monthly_churn)
```

**ROI Calculation:**

```text
Development Cost = estimated hours × <hourly opportunity cost>
Break-even = Development Cost / Monthly Net Revenue
ROI (12mo) = (Total Revenue - Total Cost) / Total Cost × 100%
```

### Phase 3: Deliver

Write the report, present key findings to user. Include:

- Confidence levels (High/Medium/Low) on each projection
- Data sources cited
- Clear assumptions stated
- Actionable recommendations with priority

## Conversion Optimization Playbook

Apply these proven conversion tactics when making recommendations:

1. **Rating before paywall** — Prompt for App Store rating BEFORE showing the paywall. Users 1-star when they hit a paywall cold. Get the 5-star review first, then show pricing.
2. **Killer onboarding** — Show value in under 30 seconds. Don't explain features, show outcomes. Make them feel success before asking for anything.
3. **Free trial with card required** — Removes freeloaders, pre-qualifies serious users. Increases conversion ~3x vs no-card trials.
4. **Weekly pricing tier** — Monthly and yearly isn't enough. Weekly lowers commitment fear and converts users who want to "test" before going long-term. Always recommend a weekly option alongside monthly/yearly.

Include a **Conversion Strategy** section in every report evaluating how the app can apply each of these, with specific UX recommendations.

## Tips

- For niche apps, the TAM is small — adjust SOM expectations
- Health/fitness apps have high competition but also high willingness-to-pay
- Finance apps have highest ARPU but strictest regulation
- Always benchmark against BOTH direct competitors and adjacent apps
- If no public data exists, estimate from App Store review counts (reviews ≈ 0.5-1% of downloads)
- Use conservative estimates — better to exceed projections than miss them
- **Currency conversion ≠ price localization.** Auto-converted prices often miss psychological thresholds and local purchasing power. Always recommend custom price tiers for top 5-10 markets. A $4.99/mo sub auto-converts to ~₺179.99 in Turkey, but ₺149.99 may convert 2-3x better.
- Use Apple's App Store pricing reference tables and Google's sub-country pricing to identify optimal tiers

## Multi-App Mode

When analyzing multiple apps at once, spawn all Phase 1 agents for all apps simultaneously (up to 16 agents). Group results by app in Phase 2.

Present a comparison table at the end:

```text
| Metric          | App A    | App B    | App C    |
|-----------------|----------|----------|----------|
| TAM             | $X.XB    | $X.XB    | $X.XM    |
| SOM (Y1)        | $XXK     | $XXK     | $XXK     |
| Projected MAU   | X,XXX    | X,XXX    | XXX      |
| Monthly Revenue | $X,XXX   | $X,XXX   | $XXX     |
| Break-even      | X months | X months | X months |
| Risk Level      | Med      | High     | Low      |
| Recommendation  | Launch   | Iterate  | Launch   |
```
