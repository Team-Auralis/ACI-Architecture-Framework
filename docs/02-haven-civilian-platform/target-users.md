# Target Users

HAVEN serves three distinct user profiles:

## 1. The Stranded Civilian (Victim)
*   **Goal:** Request immediate assistance (Medical, Fire, Evacuation).
*   **Technical Constraint:** Highly likely to have zero cellular connectivity and low battery.
*   **UX:** Large, unambiguous SOS button. Zero configuration required during the emergency.

## 2. The Volunteer Civilian (Relay)
*   **Goal:** Provide assistance or act as a network bridge.
*   **Technical Constraint:** Needs the app running in the background to relay BLE packets.
*   **UX:** Opt-in mesh relay capabilities. Can view localized, anonymized requests for help if authorized.

## 3. The Dispatch Operator (Triage)
*   **Goal:** Coordinate the response effort across a region.
*   **Technical Constraint:** Must handle overwhelming data volume without UI lag.
*   **UX:** Operates the Next.js Command Dashboard. Requires AI-assisted clustering of SOS signals (e.g., grouping 50 SOS signals from the same collapsed building).
