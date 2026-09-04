# Telemetry & Sensor Ingestion

The firehose of the physical world.

## Standardization (CloudEvents)
ORION ingests data from thousands of disparate sources: LoRaWAN flood sensors, DJI drones, Android phones, and power grid SCADA systems. 

OMNIS normalizes this chaos by forcing all telemetry into the **CloudEvents** JSON specification at the very edge (via Leaf Nodes). The core routing engine only speaks CloudEvents.

## Edge Downsampling
If a bridge stress sensor fires 1,000 times a second, beaming that over satellite is suicide.
The local Edge Node acts as a buffer. It calculates the moving average over 60 seconds and transmits a single summary packet. If the sensor detects a catastrophic anomaly, it bypasses the buffer and triggers an immediate P0 (Priority 0) alert.
