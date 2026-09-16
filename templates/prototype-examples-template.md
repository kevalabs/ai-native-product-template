# Prototype examples

These cases are synthetic illustrations, not confirmed product behavior.
Replace them with your named cases before presenting the prototype.
Keep one JSON block. Each case has a unique `id` and a `form`.
Use every applicable form; add domain fields before confirmation.

```json
[
  {
    "id": "screen-empty-list",
    "form": "screen walkthrough",
    "scenario": "Open the list with no items",
    "sample_data": {"items": []},
    "expected": "The empty state is visible"
  },
  {
    "id": "rule-total-count",
    "form": "worked example",
    "inputs": {"counts": [2, 3]},
    "expected_outputs": {"total": 5}
  },
  {
    "id": "service-success",
    "form": "integration trial",
    "scenario": "The sample provider accepts the request",
    "inputs": {"sample_id": "demo-1"},
    "expected": {"outcome": "success"}
  },
  {
    "id": "service-failure",
    "form": "integration trial",
    "scenario": "The sample provider is unavailable",
    "inputs": {"sample_id": "demo-1", "provider": "unavailable"},
    "expected": {"outcome": "failure", "message": "Try again later"}
  }
]
```

The prototype demonstration reads this file. After confirmation, preserve
the entire file byte for byte as the phase's `design/prototype-examples.md`.
Build tests read its JSON block directly and assert the product's results.
Do not copy cases into a second fixture or rewrite confirmed inputs.
Changed examples need renewed confirmation or an accepted Spec revision.
