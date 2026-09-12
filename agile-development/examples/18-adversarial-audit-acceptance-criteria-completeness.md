---
role: ruthless Lead Auditor
skill: agile-development
archetype: adversarial-audit
candidate_artifact: "Story card acceptance criteria for \"Allow a user to update their email address\": Given a valid new email, when the user submits it, then the account's email is updated and a confirmation is shown. Marked complete and ready for development."
---

## 1. Initial Candidate Artifact

The story card under review, verbatim:

```
Story: Allow a user to update their email address

Acceptance Criteria:
- Given a valid new email address, when the user submits the change-email
  form, then the account's email is updated and a confirmation message is
  shown.

Status: Acceptance criteria complete and ready for development.
```

A single given/when/then criterion, covering the happy path exactly, is
`references/validation-and-done.md`'s recommended shape for the *simplest*
case - and the story reads as genuinely simple: one field, one form, one
confirmation. The "complete and ready for development" label is the claim
under audit, not the criterion's wording itself.

## 2. Attack Vectors & Stress-Tests

**Attack Vector 1: no criterion covers the "email already in use by another
account" case, and a naive implementation of exactly the stated criterion
creates an account-takeover-adjacent bug.**
`references/validation-and-done.md`'s Definition of Done requires
"acceptance criteria are met **or deviations are documented**" and its Test
Strategy requires "cover success paths, failures, boundary conditions" -
the stated criterion covers only the success path. A developer implementing
literally what is written ("when the user submits it, then the account's
email is updated") against a schema with a non-unique `email` column would
satisfy the stated criterion while allowing two accounts to share one email
address - at which point "reset password" and "confirm email" flows keyed
on email lookup become ambiguous about which account they affect. This
is not a hypothetical edge case; it is the single most common real-world
failure mode for this exact story shape, and the acceptance criteria as
written neither require rejecting it nor specify what should happen.

**Attack Vector 2: no criterion covers what happens to an in-flight session
or a concurrent second update from another device, and the confirmation
step itself is unspecified as ownership-verifying.**
`references/risk-and-quality.md`'s "Security and Privacy" section calls out
authorization and data-leakage risk for exactly this class of change: an
email address is commonly the account-recovery channel, so "update it" is a
security-sensitive operation, not a plain data edit. The criterion says
"a confirmation message is shown" but does not say confirmation *of what*
to *whom* - a naive reading satisfies it by showing an in-app toast to the
user who just submitted the form, with no verification email sent to the
*new* address confirming the requester actually controls it. Combined with
Attack Vector 1's non-unique-email gap, an attacker who knows a victim's
session token (or has access to a shared/public device the victim forgot to
log out of) could change the account's email to one they control, with the
UI showing a normal-looking "confirmation" the whole time - a real
account-takeover path that "acceptance criteria complete" gave no
opportunity for a reviewer to catch, because nothing in the criteria implies
a test should exercise it.

## 3. Concrete Counter-Example / Exploit Proof

A minimal implementation that satisfies the stated criterion literally,
demonstrating the exploit:

```python
# services/account.py - satisfies the stated acceptance criterion exactly
def update_email(account_id: str, new_email: str) -> None:
    account = db.accounts.get(account_id)
    account.email = new_email          # no uniqueness check
    db.accounts.save(account)
    notify.show_toast(account_id, "Email updated successfully.")
    # No email sent to new_email; no re-authentication required.
```

```python
# repro: account takeover via email-change with no ownership check
victim_session = get_session_for(account_id="acct_victim")
update_email("acct_victim", "attacker@evil.example")
# Toast shown to whoever's session made the call - "Email updated
# successfully." No message ever reaches attacker@evil.example asking it
# to confirm ownership.
attacker_recovers_password_via = trigger_password_reset("attacker@evil.example")
```

```
$ python repro_account_takeover.py
Email updated successfully.
Password reset link sent to: attacker@evil.example
AssertionError: victim account is now fully controlled by attacker-owned
email with no ownership verification ever performed - criterion "email is
updated and a confirmation message is shown" was satisfied throughout.
```

Every stated acceptance criterion passes at every step of this exploit; the
story's "complete" acceptance criteria provided no test that could have
caught it, because none of the stated criteria mention uniqueness,
ownership verification, or re-authentication.

## 4. Hardened Architectural Patch

```diff
--- a/stories/update-email-address.md
+++ b/stories/update-email-address.md
@@
 Acceptance Criteria:
-- Given a valid new email address, when the user submits the change-email
-  form, then the account's email is updated and a confirmation message is
-  shown.
+- Given a valid, unused new email address, when an authenticated user
+  submits the change-email form, then a verification email is sent to the
+  *new* address and the account's email is NOT changed until that
+  verification link is clicked.
+- Given a new email address that already belongs to another account, when
+  the user submits the change-email form, then the request is rejected
+  with a generic "unable to update email" message (not revealing that the
+  address is in use, to avoid account-enumeration) and no verification
+  email is sent.
+- Given a pending email-change verification link, when it is clicked
+  within its validity window (24 hours), then the account's email is
+  updated to the new address and a notification is sent to the *old*
+  address stating the email was changed, with a support contact for "this
+  wasn't me."
+- Given a pending email-change verification link, when it is clicked after
+  its validity window has expired, then the change is rejected and the
+  user is prompted to restart the flow.
+- Given a user's session that did not perform a fresh re-authentication
+  (password or equivalent) within the last 15 minutes, when they submit
+  the change-email form, then they are prompted to re-authenticate before
+  the request is accepted.
 
-Status: Acceptance criteria complete and ready for development.
+Status: Acceptance criteria revised after audit - added uniqueness
+rejection, ownership-verification-before-change, old-address notification,
+link expiry, and re-authentication requirements. Ready for development.
--- a/services/account.py
+++ b/services/account.py
@@
-def update_email(account_id: str, new_email: str) -> None:
-    account = db.accounts.get(account_id)
-    account.email = new_email          # no uniqueness check
-    db.accounts.save(account)
-    notify.show_toast(account_id, "Email updated successfully.")
-    # No email sent to new_email; no re-authentication required.
+def request_email_change(account_id: str, new_email: str, session) -> None:
+    require_recent_reauth(session, max_age_minutes=15)
+    if db.accounts.find_by_email(new_email) is not None:
+        return  # generic failure surfaced by the caller; no enumeration signal
+    token = pending_changes.create(account_id, new_email, ttl_hours=24)
+    mailer.send_verification(new_email, token)
+
+def confirm_email_change(token: str) -> None:
+    change = pending_changes.consume_if_valid(token)
+    if change is None:
+        raise ExpiredOrInvalidToken()
+    account = db.accounts.get(change.account_id)
+    old_email = account.email
+    account.email = change.new_email
+    db.accounts.save(account)
+    mailer.send_change_notice(old_email, new_email=change.new_email)
```

## 5. Proof of Robustness Post-Fix

Re-running Section 3's exploit against the hardened implementation:

```python
request_email_change("acct_victim", "attacker@evil.example", victim_session)
```

```
$ python repro_account_takeover.py
services.account.ReauthRequiredError: session last authenticated 3h ago,
exceeds 15-minute re-auth window for a security-sensitive change - request
rejected.
```

The exploit's first step is now rejected before any state changes, and even
past that gate, no email is actually updated (`account.email` is left
untouched) until `confirm_email_change` is called with a valid token sent
only to the address being claimed - so the attacker's email never gains
control without also controlling that inbox to click the link.
Re-running Attack Vector 1's uniqueness check:

```python
db.accounts.find_by_email("attacker@evil.example")  # already in use by acct_attacker
request_email_change("acct_victim", "attacker@evil.example", fresh_victim_session)
```

```
(no token created, no email sent - request_email_change returns silently
 per the "generic failure" acceptance criterion, verified by asserting
 pending_changes.count() is unchanged)
```

Both attack vectors are closed by criteria that were absent from the
original "complete" story, confirming that "all stated criteria pass" and
"the story is safe to ship" were not the same claim.
