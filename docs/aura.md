# AURA — ORION’s visual system presence

AURA is the presentation layer that makes ORION’s system condition visible. It is not a service, an AI agent, a policy authority, or a dispatch control. AURA receives a display state from the interface and never authorizes, recommends, or executes an operational action.

## Design language

The original AURA mark is a **signal lattice**: a six-sided field for resilient infrastructure, a split diamond core for observation/understanding, and two navigators for incoming and returning system signals. It scales to a small monochrome icon because its silhouette and interior split remain legible without color. The linework is geometric, open, and intentionally non-anthropomorphic.

Motion is deterministic CSS/SVG: drift means listening, core compression means analysis, fast synchronized navigation means coordination, and interruption means degraded/offline. No animation uses randomness. `frozen` and reduced-motion preferences disable all movement.

| State | Meaning | Visual behavior | Accessibility label |
|---|---|---|---|
| IDLE | Healthy and waiting | Calm lattice drift | ORION is healthy and waiting. |
| LISTENING | Receiving data | Directional lateral drift | ORION is receiving information. |
| ANALYZING | Processing | Compressed rotating core | ORION is processing incoming information. |
| COORDINATING | Systems interacting | Fast synchronized navigators | ORION subsystems are coordinating. |
| ALERT | Critical incident | Strong bounded pulse, heavier frame | ORION has detected a critical incident requiring attention. |
| DEGRADED | Reduced capability | Interrupted frame and asymmetric movement | ORION is operating with reduced capability. |
| RECOVERING | Restoring normal operation | Settling expansion | ORION is restoring normal operation. |
| SAFE | Stable/resolved | Slow stable breathing | ORION is stable and the active incident is resolved. |
| HUMAN_REVIEW | Authorized action needed | Explicit vertical review glyph | ORION requires authorized human review. |
| OFFLINE | Relevant subsystem unreachable | Broken linework and diagonal disconnect mark | ORION cannot reach the relevant subsystem. |

## Integration

`Aura` is an isolated React client component in `apps/dashboard/src/components/aura`. It accepts `state`, `size`, `theme` (`dark`, `light`, `mono`), `intensity`, `animated`, and `frozen`. It has a semantic SVG title and `role="img"`; do not use color as the only status indicator—always pair it with text, as the dashboard does.

```tsx
<Aura state="HUMAN_REVIEW" size={64} theme="dark" frozen={false} />
```

The dashboard’s current mapping is deliberately display-only: connection errors map to `OFFLINE`, critical incidents to `ALERT`, high-severity incidents to `HUMAN_REVIEW`, untriaged incidents to `ANALYZING`, active assets to `COORDINATING`, and no incidents to `SAFE`. A future state aggregator may replace this mapper, but must remain outside AURA and preserve the human approval boundary.

SVG and CSS animations avoid canvas/WebGL and external assets, keeping AURA lightweight across dashboards, mobile status indicators, screenshots, PDFs, and documentation. The geometry supports dark/light/monochrome contexts without locking the ORION identity to one color.
