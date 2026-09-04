# Critical Infrastructure Integration

Expanding ORION beyond smartphones and emergency vehicles.

## The SCADA Bridge
National infrastructure (power grids, water dams, air traffic control radar) runs on legacy SCADA (Supervisory Control and Data Acquisition) systems.
ASCEND dictates that these systems must be integrated into the ORION mesh to allow **SENTIENCE** (AI) to predict cascading failures.

*   We do not replace the SCADA systems.
*   We deploy an ORION Edge Node next to the SCADA controller.
*   The Edge Node runs a lightweight adapter that translates legacy Modbus/DNP3 protocols into standardized ORION CloudEvent JSON.
*   If a dam's water pressure exceeds a threshold, the SCADA system alerts the Edge Node, which publishes `telemetry.infrastructure.dam.critical` to the global mesh, instantly notifying operators and triggering simulation updates in MIRROR.
