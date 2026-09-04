# Distributed Computing

In ORION, compute is shifted to where the data is, not the other way around.

## The Edge AI Paradigm
Consider a drone recording 4K video of a collapsed bridge.
*   **Legacy Model:** The drone beams 4K video over a satellite link to the cloud. The cloud AI analyzes it. (Fails because satellite bandwidth is capped at 2Mbps).
*   **ORION Model:** The computer vision AI model (packaged as a container) is pushed *down* to the drone or the nearby Edge Node. The AI analyzes the 4K video locally. It finds a survivor, generates a 2-kilobyte JSON `incident.created` event, and sends *only* the JSON over the satellite link.

By treating the entire planetary mesh as a single distributed computer, ORION solves bandwidth constraints mathematically.
