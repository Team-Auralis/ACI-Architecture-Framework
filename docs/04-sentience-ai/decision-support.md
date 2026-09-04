# Decision Support System

The interface between SENTIENCE and the human operator.

When SENTIENCE processes data, it does not act; it **proposes**.

## The Proposal Flow
1.  The Triage Agent identifies a critical medical emergency in a flooded zone.
2.  The Logistics Agent identifies that a swift-water rescue team is 2 miles away.
3.  The AI generates a `DispatchProposal` JSON payload.
4.  The Next.js Operator Dashboard receives this proposal.
5.  The UI highlights the map and presents a pre-drafted dispatch order.
6.  The human operator reviews the proposal.
7.  The human clicks **"Approve and Dispatch."**
8.  The system records the human's ID and executes the action.

This reduces the operator's workflow from 5 minutes of manual cross-referencing to a 5-second review-and-approve click.
