# Rule: Spam and Template Apps

- **Guideline**: 4.3(a), 4.3(b), 4.2.6
- **Severity**: REJECTION
- **Category**: design

## What to Check

Guideline 4.3(a) says not to create multiple Bundle IDs of the same app, for example a separate map app for every city instead of one map app that searches any city.
For apps with versions for specific locations, sports teams or universities, Apple advises "consider submitting a single app and providing the variations using in-app purchase".
That is advice, not the only accepted fix.

Guideline 4.3(b) says not to submit apps that are indistinguishable from what is already widely available, or opportunistic variants of existing app categories or popular apps.
It adds that "Repeated submissions of this kind may lead to removal from the Apple Developer Program".
That sentence refers to the mediocre and low-effort apps 4.3(b) lists, not to every 4.3 rejection, and no Apple text sets a rejection count that triggers termination.

Guideline 4.2.6 rejects apps created from a commercialized template or app generation service unless the provider of the app's content submits them.
Apple offers template providers another option, a single binary that hosts all client content in an aggregated or "picker" model.

Apple's App Review page warns that submitting several apps that are essentially the same ties up App Review and risks the apps not passing review, and suggests combining them into one.

Check:

- Other apps in the same developer account that share this app's template, flows and features and differ only in content, language, audience or color.
- Whether those variations could live inside one app as in-app purchase content or as selectable content.
- Whether the app was built from a purchased template or an app generation service, and who submits it.
- Whether several of these apps or their updates are about to go to review on the same day.

## How to Detect

```bash
# List every app in the account and look for siblings with the same template
asc apps list --output table

# Compare the description of each sibling against this app
asc metadata pull --app "<APP_ID>" --version "<VERSION>" --dir ./metadata
jq -r '.description // empty' ./metadata/version/<VERSION>/<LOCALE>.json
```

Apple has not said how it detects similar apps.
Its May 2026 Newsroom post says App Review uses machine learning to analyze app similarity and flag problematic changes in app updates.

## Resolution

1. Do not resubmit the same build after a 4.3 or 4.2.6 rejection.
   Reply in App Review messages, or make the significant changes the rejection asks for.
2. Explain in the review notes what this app does that the account's other apps do not.
3. Consider merging same-template apps into one app with in-app purchase or selectable content, as 4.3(a) advises.
4. If the account receives a termination notice, follow the appeal steps in `asc-submission-health`.

One developer reported that a day of 4.3 rejections on updates to his whole portfolio was followed by a pending termination of his account, which Apple's App Review Board reversed after he deleted his same-template apps.
Another developer advised uploading a demo video to the review attachments, and a third reported that submitting one app at a time did not clear 4.3.
These are individual accounts, not Apple guidance.
Source: <https://x.com/DanKulkov/status/2109888553622949898> and its replies.

## Example Rejection

Developer-posted copy of an Apple rejection, not an Apple-authored page:

```text
Guidelines 4.3 - Spam and 4.2.6 - App Generation Services
Issue Description

The app does not appear to meet App Store requirements to prevent the
distribution of spam submissions.

Specifically, the app appears to match one or more of the following kinds of
spam, which make it harder for users to find the apps they want:

- Apps that duplicate content or functionality already on the App Store. See
  guideline 4.3(a).
- Apps that are indistinguishable from what's already widely available or is an
  opportunistic variant of an existing category or popular app. See guideline
  4.3(b).
- Apps that are created from a commercialized template or app generation
  service but are not submitted directly by the provider of the app's content.
  See guideline 4.2.6.

Next Steps

If any of the above descriptions apply to this submission, do not resubmit for
review until significant changes have been made to resolve this issue.
```

## Sources

- App Store Review Guidelines 4.2.6 and 4.3: <https://developer.apple.com/app-store/review/guidelines/>
- App Review, repeated submission of similar apps: <https://developer.apple.com/distribute/app-review/>
- Apple Newsroom, May 2026: <https://www.apple.com/newsroom/2026/05/the-app-store-stopped-over-2-point-2-billion-usd-in-fraudulent-transactions-in-2025/>
