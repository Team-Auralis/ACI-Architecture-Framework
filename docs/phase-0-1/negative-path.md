# Negative Path

This is mandatory.

```text
Unauthorized request
        ↓
Identity established
        ↓
OPA
        ↓
DENY
        ↓
HTTP 403
        ↓
No unauthorized database mutation
        ↓
No unauthorized event
```

This proves OPA is an actual enforcement firewall rather than a decorative component.
