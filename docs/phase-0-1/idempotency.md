# Idempotency

HTTP idempotency and event-consumer idempotency are separate requirements.

## API Idempotency
Prevent duplicate SOS incidents if a client retries the same request.
`Request + Idempotency Key -> First request (create) -> Retry (return existing result)`

## Event-Consumer Idempotency
Prevent duplicate processing if an event is delivered again.
`Event -> Worker -> Already processed? (Yes -> skip, No -> process and record)`
