---
role: Staff Software Engineer
skill: agile-development
use_case: scoping a new "let admins export a CSV of active users" feature request
---

## Scenario

Product asks for an endpoint that "lets admins export a CSV of active users."
The user table has grown to several hundred thousand rows across three years of
signups, some of whom deactivated their accounts, some of whom haven't logged in
in years but never deleted their account either. There is no existing definition
of "active" anywhere in the codebase - it is a business term, not a column - and
no admin-facing async job infrastructure exists yet. The request is one sentence
long, and it is on the sprint board as a single ticket with no acceptance
criteria attached.

## Common Weak Approach

The engineer reads "active users" as self-evidently "not soft-deleted" - the only
existing boolean on the `User` model - and starts building. Because the ticket
also says "let admins export," they reason that admins will eventually want a
dashboard for this, so they build the dashboard page, a background job queue to
generate the file (reasoning that "some export might be slow one day"), and an
email notification for when the job completes, all in one PR:

```python
# admin/views.py
@admin_required
def export_users_page(request):
    """New admin dashboard page: lists past exports and lets you start a new one."""
    exports = ExportJob.objects.filter(requested_by=request.user).order_by("-created_at")
    return render(request, "admin/export_users.html", {"exports": exports})


@admin_required
def start_user_export(request):
    job = ExportJob.objects.create(requested_by=request.user, status="queued")
    export_users_task.delay(job.id)  # enqueued on a new Celery queue: "admin-exports"
    return redirect("admin_export_users_page")


# admin/tasks.py
@shared_task
def export_users_task(job_id: int) -> None:
    job = ExportJob.objects.get(id=job_id)
    job.status = "running"
    job.save(update_fields=["status"])

    users = User.objects.filter(deleted_at__isnull=True)  # "active" silently means this
    path = f"/tmp/exports/users-{job.id}.csv"
    with open(path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "email", "signup_date"])
        for user in users:  # loads the whole active-user table into memory at once
            writer.writerow([user.id, user.email, user.signup_date])

    job.status = "done"
    job.file_path = path
    job.save(update_fields=["status", "file_path"])
    send_export_ready_email.delay(job.requested_by.email, job.id)  # new notification feature


# admin/emails.py
@shared_task
def send_export_ready_email(to_email: str, job_id: int) -> None:
    send_mail(
        subject="Your user export is ready",
        message=f"Download it here: /admin/exports/{job_id}/download",
        from_email="noreply@example.com",
        recipient_list=[to_email],
    )
```

The PR touches a new dashboard template, a new Celery queue and worker
configuration, a new `ExportJob` model and migration, a new email template, and
the CSV generation itself - roughly 600 lines across nine files. There is no
test for any of it, because the reviewer can't tell from the diff which parts
are load-bearing for "export a CSV" and which are speculative infrastructure for
features nobody asked for yet. The definition of "active" was never written down
anywhere; a reviewer who disagrees with "not soft-deleted" (say, they expected
"logged in within 30 days") would have to reverse-engineer it from the query
inside a Celery task three files deep. Review stalls for a week because nobody
can hold the whole PR in their head at once, and the actual CSV export - the one
thing that was asked for - ships no faster than if none of the extra
infrastructure had been built.

## Expert-Level Best Practice

The engineer starts by writing acceptance criteria before writing any code,
using given/when/then, and states the ambiguous business term as a visible
assumption rather than resolving it silently inside a query:

```markdown
## Acceptance Criteria

- Given an authenticated admin, when they request `GET /admin/users/export.csv`,
  then the response is a `text/csv` download listing every active user's id,
  email, and signup date, ordered by signup date ascending.
- Given a non-admin authenticated user, when they request the same endpoint,
  then the request fails with the repository's standard 403 forbidden response
  and no file is generated.
- Given zero active users exist, when the endpoint is requested, then the
  response is a CSV containing only the header row, not an error.

## Assumption (flagged for product sign-off, not guessed silently)

"Active" is read as **not soft-deleted** (`deleted_at IS NULL`), matching the
only existing status field on `User`. The alternative reading - "logged in
within the last 30 days" - would need a new query against `last_login_at` and
would return a materially different, much smaller list. This PR implements the
"not soft-deleted" definition and calls it out by name in the endpoint's
docstring and in the PR description; a 30-day-activity definition is a
one-line follow-up ticket if that's what was actually meant, not a silent
guess baked into a query nobody reviewed for that intent.
```

Given that, they pick the smallest vertical slice that satisfies the stated
criteria end-to-end - a synchronous CSV download for the common case - and
explicitly defers the two things the weak approach built speculatively:

```python
# admin/views.py
import csv

from django.http import StreamingHttpResponse
from django.contrib.admin.views.decorators import staff_member_required


class _EchoBuffer:
    """A file-like object whose .write() just returns what was written, so
    csv.writer can drive a StreamingHttpResponse row by row instead of
    building the whole file in memory first."""

    def write(self, value: str) -> str:
        return value


@staff_member_required
def export_active_users_csv(request):
    buffer = _EchoBuffer()
    writer = csv.writer(buffer)

    def rows():
        yield writer.writerow(["id", "email", "signup_date"])
        # .iterator() streams from the DB in chunks instead of loading the
        # whole active-user table into memory at once - this is the one piece
        # of the "will this scale" question that is actually in scope now,
        # because it changes behavior at today's row count, not just at some
        # future one.
        queryset = (
            User.objects.filter(deleted_at__isnull=True)
            .order_by("signup_date")
            .values_list("id", "email", "signup_date")
            .iterator(chunk_size=2000)
        )
        for user_id, email, signup_date in queryset:
            yield writer.writerow([user_id, email, signup_date.isoformat()])

    response = StreamingHttpResponse(rows(), content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="active_users.csv"'
    return response
```

```python
# tests/admin/test_export_active_users_csv.py
import csv
import io
from datetime import date, timedelta

import pytest
from django.urls import reverse

from accounts.models import User


@pytest.fixture
def admin_client(client, django_user_model):
    admin = django_user_model.objects.create_user(
        "admin@example.com", is_staff=True, is_superuser=True
    )
    client.force_login(admin)
    return client


def _make_user(email, deleted=False, days_ago=10):
    return User.objects.create(
        email=email,
        signup_date=date.today() - timedelta(days=days_ago),
        deleted_at=None if not deleted else date.today(),
    )


@pytest.mark.django_db
def test_export_lists_only_non_deleted_users_ordered_by_signup_date(admin_client):
    _make_user("newer@example.com", days_ago=5)
    _make_user("older@example.com", days_ago=50)
    _make_user("gone@example.com", deleted=True)

    response = admin_client.get(reverse("export_active_users_csv"))

    assert response["Content-Type"] == "text/csv"
    rows = list(csv.reader(io.StringIO(b"".join(response.streaming_content).decode())))
    emails_in_order = [row[1] for row in rows[1:]]
    assert emails_in_order == ["older@example.com", "newer@example.com"]


@pytest.mark.django_db
def test_export_forbidden_for_non_admin(client, django_user_model):
    user = django_user_model.objects.create_user("shopper@example.com")
    client.force_login(user)

    response = client.get(reverse("export_active_users_csv"))

    assert response.status_code == 403


@pytest.mark.django_db
def test_export_returns_header_only_when_no_active_users(admin_client):
    _make_user("gone@example.com", deleted=True)

    response = admin_client.get(reverse("export_active_users_csv"))

    rows = list(csv.reader(io.StringIO(b"".join(response.streaming_content).decode())))
    assert rows == [["id", "email", "signup_date"]]


@pytest.mark.django_db
def test_export_streams_a_large_table_without_loading_it_all_at_once(admin_client, settings):
    # Proportional to the risk actually introduced by this slice: a table this
    # size is realistic in production and would previously have been loaded
    # into memory in one queryset evaluation. This does not test Celery or
    # async generation, because this slice deliberately doesn't add either.
    User.objects.bulk_create(
        [User(email=f"user{i}@example.com", signup_date=date.today()) for i in range(5000)]
    )
    from django.test.utils import CaptureQueriesContext
    from django.db import connection

    with CaptureQueriesContext(connection) as ctx:
        response = admin_client.get(reverse("export_active_users_csv"))
        list(response.streaming_content)  # force the generator to run to completion

    select_queries = [q for q in ctx.captured_queries if "SELECT" in q["sql"]]
    # .iterator(chunk_size=2000) against 5000 rows issues multiple bounded
    # SELECTs rather than one unbounded one - this is the observable proxy for
    # "does not load the whole table into memory at once."
    assert len(select_queries) >= 3
```

The PR description states the deferred scope explicitly, as follow-up tickets
rather than unstated gaps:

```markdown
## Out of scope for this PR (filed as follow-ups, not silently dropped)

- FOLLOWUP-142: background/async generation for exports large enough that a
  synchronous request would risk a request-timeout (no current admin has hit
  this; revisit if/when one does).
- FOLLOWUP-143: email notification on export completion - only meaningful once
  generation is async; premature while the download is synchronous.
- FOLLOWUP-144: an admin dashboard page listing past exports - no product ask
  for export history yet; this PR ships a single endpoint an admin can already
  reach from the existing admin nav.
```

## Key Takeaways

- State ambiguous business terms as a visible, written assumption instead of
  resolving them silently inside a query. The weak approach's choice of
  "active = not soft-deleted" may even have been the right call, but because it
  was never written down, a reviewer had no way to check it against what
  product actually meant, and the cost of being wrong was discovered only after
  the feature shipped rather than during a five-second read of the PR
  description.
- Slice by the smallest end-to-end observable behavior, not by every layer the
  feature might eventually need. The weak approach built a dashboard page, a
  job queue, and an email notifier because they seemed like natural neighbors
  of "export a CSV" - but none of them were asked for, none of them were
  reviewable independently of the others, and all three added surface area
  that had to be maintained before it delivered any value. The expert approach
  shipped one given/when/then-verified endpoint and named the rest as follow-up
  tickets, which is a scoping decision, not a corner cut.
- Distinguish speculative scale-proofing from proportional scale-handling. The
  expert approach did not defer *everything* about scale - it used
  `.iterator(chunk_size=...)` and a `StreamingHttpResponse` because the table's
  actual current size (hundreds of thousands of rows) would otherwise load
  entirely into memory on every request, a real defect today. It deferred
  *async job infrastructure* because no admin has hit a timeout yet. The
  difference is evidence: build for the scale you have, defer the scale you
  are guessing at.
- Acceptance criteria are a scoping tool, not paperwork after the fact. Writing
  given/when/then before code forced three decisions into the open before any
  line of implementation existed: what "active" means, what happens on zero
  results, and what happens for a non-admin caller. The weak approach's PR
  reviewer had to reconstruct all three from finished code instead of
  confirming them against a half-page spec - which is why the review stalled
  and the acceptance criteria approach did not.
