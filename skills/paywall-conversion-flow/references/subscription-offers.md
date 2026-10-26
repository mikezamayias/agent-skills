# Subscription offers

Apple and Google offer types for each user state, read on the vendor pages on 2026-10-22.
Item 7 in `SKILL.md` says which state gets which offer.

## Apple offer types

| Offer        | Who can get it                                                                     | Where Apple shows it                                                                                                              | Notes                                                                                                        |
| ------------ | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Introductory | New and returning customers, one introductory offer per subscription group         | Applied at purchase                                                                                                               | Check eligibility before showing a trial CTA                                                                 |
| Promotional  | Anyone with an existing or expired subscription in the app, plus your own criteria | Your app, you decide who sees it                                                                                                  | Needs a server-signed request, works on iOS 12.2 and later                                                   |
| Offer code   | New and existing subscribers                                                       | Redeemed by code or link                                                                                                          | Fits a downsell to someone who never subscribed                                                              |
| Win-back     | Churned subscribers who match your eligibility rules                               | Manage Subscriptions on iOS 14.3 and later, the in-app win-back sheet on iOS 18 and later, and the product page if you promote it | The direct link `https://apps.apple.com/win-back/<win-back offer Apple ID>` can go in your own email or site |

An introductory offer is one of three types: free trial, pay up front or pay as you go (Apple help page, read 2026-10-24).

| Standard duration | Pay as you go | Pay up front                   | Free trial                                           |
| ----------------- | ------------- | ------------------------------ | ---------------------------------------------------- |
| 1 week            | 1 to 12 weeks | 1, 2, 3 or 6 months, or 1 year | 3 days, 1 or 2 weeks, 1, 2, 3 or 6 months, or 1 year |
| 1 year            | 1 year        | 1, 2, 3 or 6 months, or 1 year | Same as above                                        |

A "$0.99 first week" on a weekly product is therefore a pay as you go offer, and a "$0.99 first month" on a yearly product is a pay up front offer.

Apple groups the four as Acquire, Retain and Re-acquire.

## Win-back offer rules

- A churned subscription has an `expirationDate` in the past and `willAutoRenew` false.
- Win-back offers are set per subscription product, not per group.
  A customer is eligible only for the most recently lapsed product in each group.
- Eligibility has three controls.
  Minimum Paid Duration is 1 to 24 months, or 3, 4 or 5 years.
  Time Since Last Subscribed is 1 to 24 months and needs both a minimum and a maximum.
  Wait Between Offers is optional and 2 to 24 months.
- A subscription allows 350 win-back offers, with at most 5 running at once per storefront.
- An offer runs at least 3 days and starts one day after creation at the earliest.
- App Review must approve the subscription before you can create the offer.
- Priority is Normal or High, and it ranks the offer in the win-back sheet, Manage Subscriptions and the App Store.
- Streamlined Purchasing is on by default, so the app receives a completed transaction when someone redeems outside the app.

## Retention on iOS

- Cancellation happens in Apple's Settings, so the app cannot intercept the cancel tap.
- The server notification `DID_CHANGE_RENEWAL_STATUS` fires when a subscriber turns off auto-renew in Manage Subscriptions or cancels through AppleCare.
  The subscription stays active until it expires, so the server can decide eligibility and tell the app to show a promotional offer.
- Apple retries a failed renewal for 60 days, and Billing Grace Period is a separate setting in App Store Connect.
- The Apple pages read describe no user-facing pause for an App Store subscription.
- Apple's Retention Messaging API changes that for the cancel screen.
  It is a server-to-server service, and it shows the retention message you chose after the subscriber taps Cancel Subscription, on a Confirm Cancellation page where the subscriber can still cancel, keep the subscription or redeem an offer (Apple Retention Messaging API page, read 2026-10-25).
  There are four message types: text with bullet points, text with an image, a switch-plan message with a suggested subscription, and a promotional-offer message that carries a promotional offer.
  A message that carries an offer needs the real-time flow, where Apple calls your server when a subscriber views a subscription details page that has a Cancel button.
  Configure a default message for every product in each locale, because the system shows no retention message for a product in a locale that has no default, and it uses the default if your real-time call fails.
  Apple labels the API a pre-release and asks developers to express interest, so check access before planning on it.
  Messages show only on iOS 15.1 or later, iPadOS 15.1 or later, visionOS 1 or later and macOS 14 or later.
- One founder says the API cuts churn by 20 percent (X article, 2026-10-25, no source named, unverified).
  Apple gives no figure, so plan on none and measure retained subscribers against a holdout.

## Google Play

- Play detects a cancellation before expiry in real time, so the app can ask the user to resubscribe by push or in-app message.
- Play has winback offers in the app and in the Play Store after expiry, plus grace period and account hold for failed payments.
- Its manage-subscription page lists cancellation, resubscription and pause as user actions.

## Checklist

- [ ] Each offer has its own `placement` value and its own line in the funnel report.
- [ ] Every offer screen states the price after the offer ends, the billing period and the renewal date (`paywall-transparency`).
- [ ] No offer is named in What's New (`asc-whats-new-writer`).
- [ ] Email offers have consent and a working unsubscribe link in the EU (`launch-watch`).
- [ ] The win-back eligibility window chosen is written in the test notes.

## Sources

- <https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-introductory-offers-for-auto-renewable-subscriptions>
- <https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-win-back-offers>
- <https://developer.apple.com/documentation/storekit/supporting-win-back-offers-in-your-app>
- <https://developer.apple.com/documentation/storekit/implementing-promotional-offers-in-your-app>
- <https://developer.apple.com/app-store/subscriptions/>
- <https://developer.android.com/google/play/billing/subscriptions>
- <https://www.revenuecat.com/docs/subscription-guidance/subscription-offers/ios-subscription-offers>
