# Authorization (AuthZ)

Proving *what* you are allowed to do.

AuthZ is strictly separated from AuthN. Just because you successfully authenticated with a valid JWT does not mean you have permission to act.

## The Negative Path Architecture
ORION defaults to `DENY`. 
If a user attempts an action and no specific policy explicitly allows it, the action fails.

**Example Flow:**
1.  *Identity established:* JWT verified. User is "Bob".
2.  *Intent:* Bob tries to POST `/v1/dispatch`.
3.  *AuthZ Check:* OPA evaluates. Bob is a "Civilian".
4.  *Result:* OPA returns `DENY`. FastAPI returns `403 Forbidden`. The database is untouched.

This absolute separation guarantees that a bug in the FastAPI routing logic cannot accidentally expose administrative endpoints.
