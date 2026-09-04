# API Contract Concept
*Note: Conceptual contracts subject to versioned finalization. No implementation code.*

Request:
```json
{
  "type": "SOS",
  "location": {
    "latitude": 17.6868,
    "longitude": 83.2185
  },
  "message": "Emergency assistance required",
  "source": "mobile"
}
```

Response:
```json
{
  "incident_id": "INC-01J...",
  "status": "CREATED",
  "created_at": "2026-08-17T12:30:00Z"
}
```
