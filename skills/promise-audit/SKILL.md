---
name: promise-audit
description: >-
  Trace every promise in a privacy policy, terms, store privacy label or marketing claim to the mechanism behind it. Use when writing, signing off or publishing such a text, or when a decision changes data handling or processors. Also use when asked to document the mechanism behind each promise, or to audit drift in a published policy.
metadata:
  provenance: local
---

# Promise audit

A policy is a list of promises.
Under the GDPR (the EU's data protection law) and store review rules, a promise with nothing behind it is a liability, and so is a behaviour the policy does not mention.
Both drift over time, because product decisions change behaviour after the text was signed.

This skill traces each sentence to its mechanism in both directions and keeps a sign-off state per sentence.

## Inputs

- The texts: privacy policy, terms, deletion page, store privacy labels (the App Store "nutrition label" and the Google Play Data safety form), consent screens, and marketing claims.
- The spec: schema, jobs and retention rules, integrations and processors, screens and copy, analytics events, and moderation or automated-decision rules.
- The decision log (see `decision-sweep`).

## Step 1: Trace every sentence to a mechanism

Split each text into sentences, and quote each one verbatim.
For each promise, fill one row:

| Sentence | Mechanism | Where it is specified | Test or check that proves it | Build task | Status |
| -------- | --------- | --------------------- | ---------------------------- | ---------- | ------ |

- **Mechanism:** what makes it true, for example a database cascade, a scheduled purge job, a setting, a vendor setting, or a screen.
- **Where it is specified:** a link to the owner document.
- **Test or check:** a test that fails if the promise breaks.
  Critical promises such as deletion, retention, and visibility need one.
- **Status:** `backed`, `gap`, or `contradicted`.

Typical gaps:

- deletion that removes the account but not analytics profiles, crash reports, backups, or files in storage
- retention that is stated but not enforced by any job
- vendor retention longer than the policy says, for example an analytics plan that keeps events for years
- "we never share X" while an integration sends X
- metadata the policy says is stripped but a code path keeps

## Step 2: Trace every behaviour back to a sentence

Walk the spec for anything that touches personal data or acts on a person, and check the texts cover it:

- every processor (vendor) and the country its data sits in
- every data category, including derived data such as scores, flags, and inferences
- every automated decision that acts on someone before a human reviews it, for example account suspension, content filtering, or automated holds
  The GDPR requires these to be disclosed, with a way to ask for a human review.
  A section that claims to be complete must list them all.
- every retention period and every place data is copied to, including backups
- special-category data, such as health or biometric data, and the consent that covers each use of it
  A new use of it is a new purpose, so it needs new consent text.

Anything missing is a `gap` in the other direction.

## Step 3: Close the gaps

For each gap, choose one of two fixes:

- add the mechanism (a spec change, a test, and a build task)
- change the sentence to match reality, with a proposed rewording

Put the choice to the decision-maker on an answer sheet (see `answer-sheet`), with the exact before and after text.
Verify vendor facts such as retention, region, or data processing agreement coverage on the vendor's live pages.
Never ask the decision-maker to check them.

## Step 4: Sign-off state per sentence

Keep the sign-off state inside the text file, as a comment block at the top or an HTML comment per section:

```html
<!-- sign-off: section N, sentences X-Y: signed YYYY-MM-DD by the decision-maker
     section N, sentence X: awaiting (changed YYYY-MM-DD: <what changed>) -->
```

- A sentence is signed only in the exact wording the decision-maker approved.
  A reworded sentence goes back to `awaiting`.
  Never treat an approval as covering different text.
- Publication waits until every sentence is signed and every placeholder, such as the legal name, the contact address, or the domain, is filled.

## Step 5: Re-open on change

Every ruling recorded afterwards runs through a check: does it make any signed sentence untrue, or add behaviour no sentence covers?
If so, set the sentence to `awaiting` and add it to the next sign-off sheet, showing exactly what changed.
The `decision-sweep` loop calls this step.

## Output

- the trace table, with counts of backed, gap, and contradicted sentences
- the behaviours with no covering sentence
- the proposed fixes, as an answer sheet
- the sign-off state per sentence
- what blocks publication

## Legal limits

This is an engineering consistency check, not legal advice.
When a question needs a lawyer, for example whether a vendor without a data processing agreement is acceptable, say so in plain words and name the exact question to ask.
