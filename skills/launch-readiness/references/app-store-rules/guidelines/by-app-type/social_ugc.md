# Checklist: Social / User-Generated Content Apps

Guidelines specifically applying to social networking, messaging, community, and UGC platform apps.

## Critical (Will Reject)

- [ ] **1.2** — Content moderation: filter for objectionable material
- [ ] **1.2** — Report mechanism for offensive content with timely responses
- [ ] **1.2** — Ability to block abusive users
- [ ] **1.2** — Published contact information for user support
- [ ] **4.8** — If offering third-party login (Facebook, Google, etc.), must also offer Sign in with Apple or equivalent
- [ ] **4.0** — Sign in with Apple: don't re-ask name/email after SIWA auth
- [ ] **5.1.1(v)** — If account creation exists, must also offer account deletion
- [ ] **5.1.1(v)** — Must provide access without social login if core functionality isn't social-network-specific
- [ ] **5.1.1(i)** — Privacy policy required (in-app + App Store Connect)

## Important (Common Rejections)

- [ ] **1.2.1** — Creator content apps: age-restriction mechanism for content exceeding app rating
- [ ] **1.1.1** — No defamatory, discriminatory, or mean-spirited content
- [ ] **2.5.14** — Explicit consent for recording user activity (camera, microphone, screen)
- [ ] **5.1.1(ii)** — User consent for data collection; clear purpose strings
- [ ] **5.1.2** — ATT framework required for cross-app tracking
- [ ] **5.1.1(viii)** — No compiling personal info from non-user sources (public databases)
- [ ] **4.5.4** — Push notifications: not required to function; opt-in for marketing
- [ ] **5.1.1(iii)** — Data minimization: only request data relevant to core functionality

## UGC-Specific Rules

- [ ] NSFW content from web services: hidden by default, opt-in via website only
- [ ] No Chatroulette-style random chat, anonymous bullying, or "hot-or-not" voting
- [ ] No apps primarily used for pornographic content
- [ ] A third-party SDK that lets users type text that other users see, such as comments under a release or a review, makes the host app subject to Guideline 1.2 for that feature.
      Applying 1.2 to an SDK feature is an inference from the guideline text, not an Apple statement about SDKs.
      Check that the app itself offers a way to filter objectionable text, a report control, a block control and published contact information.
      Say which of them the SDK provides and which the app still has to add.
      Vendor documentation is not Apple's decision, so treat what the vendor provides as claimed until a build was reviewed or tested.
