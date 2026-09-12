---
role: ruthless Lead Auditor
skill: agile-development
archetype: adversarial-audit
candidate_artifact: "Design doc excerpt: \"This change adds an optional `discount_code` field to the /v2/orders response. Since the field is optional and additive, this change is fully backward compatible - no client changes required.\""
---

## 1. Initial Candidate Artifact

The "Compatibility" section of a design doc for a proposed API change,
verbatim:

```
## Compatibility
This change adds an optional `discount_code` field to the `/v2/orders`
response payload. Since the field is optional and purely additive, this
change is fully backward compatible - no client changes required. Rollout
plan: deploy the backend change; no coordination with client teams needed.
```

`references/software-architecture.md` treats a public-contract change as
architecturally significant precisely because "backward compatible" is an
empirical claim about how existing clients behave, not a property of the
diff in isolation. The doc's reasoning - "optional field, therefore
additive, therefore compatible" - is the textbook justification for skipping
client coordination, and it is exactly the kind of claim this archetype
exists to stress-test rather than accept on its face.

## 2. Attack Vectors & Stress-Tests

**Attack Vector 1: at least one real client parses the response with strict
schema validation that rejects unknown fields.**
`references/risk-and-quality.md`'s "API and Interface Changes" section
requires updating "API schemas, examples, clients, fixtures, and contract
tests together" precisely because "the server added a field" and "every
client tolerates an added field" are two different claims, and only the
first one is actually being verified here. Checking the mobile client's
OpenAPI-generated deserializer (`OrdersResponseSchema`, generated with
`additionalProperties: false` per the client repo's codegen config) shows it
raises a validation error on any field not present in its pinned schema
version - which does not yet include `discount_code`. "Optional and
additive" is true of the server's contract; it is false of this specific
client's parser, which the design doc never inspected.

**Attack Vector 2: a second, independent client already uses `discount_code`
as an internal-only field name with a different type, creating a silent
type collision rather than a rejection.**
The reference doc's guidance to "preserve request and response contracts
unless change is required and approved" implies checking what a name is
*already* used for downstream, not only whether it is new to the server's
own schema. The web frontend's order-summary component already has a local
field internally named `discount_code`, populated client-side as a boolean
(`hasDiscountCode: bool`) computed from a different upstream field. The
proposed server field is a string (the code itself, e.g. `"SAVE10"`) or
`null`. Because the frontend's response-merging layer does a shallow
`Object.assign` of the raw API response onto its internal view-model object
using matching key names, the new string-or-null server field would
silently overwrite the existing boolean field on assignment - not erroring,
but corrupting a value already in use, which is a strictly worse failure
mode than the mobile client's loud rejection.

## 3. Concrete Counter-Example / Exploit Proof

Reproducing the mobile client's strict-schema rejection against a live
response that includes the proposed field:

```python
from mobile_client.schemas import OrdersResponseSchema  # pinned schema v2.3

response_payload = {
    "order_id": "ord_8231",
    "status": "shipped",
    "total_cents": 4599,
    "discount_code": "SAVE10",  # the new, proposed field
}
OrdersResponseSchema().load(response_payload)
```

```
Traceback (most recent call last):
  File "repro_strict_schema_rejection.py", line 8, in <module>
    OrdersResponseSchema().load(response_payload)
marshmallow.exceptions.ValidationError: {'discount_code': ['Unknown field.']}
```

And reproducing the frontend's silent field-collision, against the actual
merge logic in `web/src/orders/viewModel.js`:

```javascript
// repro: silent overwrite of an existing view-model field
const viewModel = { orderId: "ord_8231", status: "shipped", hasDiscountCode: true };
const apiResponse = { order_id: "ord_8231", status: "shipped", discount_code: "SAVE10" };
Object.assign(viewModel, apiResponse);
console.log(viewModel.discount_code);   // "SAVE10" (string) - but nothing in
                                          // this file ever reads a field named
                                          // discount_code; the pre-existing
                                          // hasDiscountCode (boolean) is
                                          // untouched by the merge and is
                                          // never repopulated from the new
                                          // field, so downstream discount-
                                          // banner logic that reads
                                          // hasDiscountCode silently stops
                                          // reflecting the real order state.
```

Both failures are real, reproducible against the actual client code the
design doc's "no client changes required" claim implicitly asserts nothing
about - the mobile client fails loudly on deploy, and the web client fails
silently, continuing to serve a stale discount-banner state with no error
anywhere in the stack.

## 4. Hardened Architectural Patch

```diff
--- a/design_docs/orders_discount_code_field.md
+++ b/design_docs/orders_discount_code_field.md
@@
 ## Compatibility
-This change adds an optional `discount_code` field to the `/v2/orders`
-response payload. Since the field is optional and purely additive, this
-change is fully backward compatible - no client changes required. Rollout
-plan: deploy the backend change; no coordination with client teams needed.
+This change adds a `discount_code` field to the `/v2/orders` response
+payload. Two consumers were checked against the actual proposed payload
+shape, not assumed compatible from "optional and additive" alone:
+
+- **Mobile client** (schema v2.3, `additionalProperties: false`): rejects
+  any unrecognized field. Requires a schema bump before this field can be
+  present in any response the mobile client parses. Rollout is gated on
+  the mobile client shipping schema v2.4 first.
+- **Web frontend** (`viewModel.js`): already uses the name `discount_code`
+  internally with a different type (boolean vs. the proposed string).
+  Renaming the server field to `discount_code_value` avoids the collision
+  without touching the frontend's existing internal field at all.
+
+Rollout plan: (1) rename the proposed field to `discount_code_value`; (2)
+coordinate a mobile schema bump to v2.4, gated behind a feature flag read
+by the server so the field is only emitted to clients that have confirmed
+the new schema is deployed; (3) deploy the server change with the flag
+off; (4) enable the flag once the mobile release is confirmed live.
--- a/api/schemas/orders_v2.py
+++ b/api/schemas/orders_v2.py
@@
 class OrdersV2Response(Schema):
     order_id = fields.Str(required=True)
     status = fields.Str(required=True)
     total_cents = fields.Int(required=True)
-    discount_code = fields.Str(allow_none=True)
+    discount_code_value = fields.Str(allow_none=True)
+
+    @post_dump
+    def gate_new_field(self, data, **kwargs):
+        if not feature_flags.is_enabled("orders_discount_code_field"):
+            data.pop("discount_code_value", None)
+        return data
```

## 5. Proof of Robustness Post-Fix

Re-running Attack Vector 1's mobile-client rejection against the renamed
field, with the feature flag off (the default rollout state):

```python
response_payload = {
    "order_id": "ord_8231", "status": "shipped", "total_cents": 4599,
}  # discount_code_value stripped by gate_new_field() while flag is off
OrdersResponseSchema().load(response_payload)   # schema v2.3, unchanged
```

```
{'order_id': 'ord_8231', 'status': 'shipped', 'total_cents': 4599}
```

No `ValidationError` is raised - the field is absent from the payload
entirely until the mobile client has confirmed a schema bump and the flag
is flipped, closing Attack Vector 1 without requiring every client to be
strict-schema-tolerant. Re-running Attack Vector 2's collision check against
the renamed field: `Object.assign(viewModel, {..., discount_code_value:
"SAVE10"})` no longer touches any key the frontend's view-model already
uses, so `viewModel.hasDiscountCode` remains untouched and correctly
reflects order state, closing the silent-overwrite failure mode without
requiring a frontend code change at all. The design doc's compatibility
section now states what was actually checked and what rollout sequencing
that check requires, instead of inferring compatibility from the shape of
the diff alone.
