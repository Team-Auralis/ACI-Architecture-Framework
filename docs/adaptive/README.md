# ORION Adaptive Intelligence & Capability Fabric

## 1. Core Vision
ORION is transitioning from a collection of manually orchestrated services into an **Intent-Driven, Capability-Aware, Self-Adaptive, Policy-Bounded, Observable, and Human-Governed** systems platform. 

The goal is to allow operators to declare *intent* (e.g., "Keep emergency communications operational") and allow the system to dynamically discover, sequence, and execute the optimal capabilities to achieve that intent, constantly adapting to failure—**without ever bypassing authorization, geofencing, or Human-in-the-Loop (HITL) safety policies.**

## 2. Adaptive Loop Architecture
The core cognitive loop of ORION is:
\HUMAN INTENT -> UNDERSTAND GOAL -> DISCOVER CAPABILITIES -> UNDERSTAND ENVIRONMENT -> GENERATE PLAN -> POLICY/SAFETY CHECK (VEIL) -> EXECUTE -> OBSERVE RESULT -> ADAPT -> REPLAN\

## 3. Capability Registry & Graph
Capabilities are discrete, bounded actions (e.g., \
etwork.switch\, \
otification.send\, \sset.locate\) registered in a central manifest. They are modeled as a dependency graph. The Planner traverses this graph to formulate strategies based on current environmental health.

## 4. Safety First: Method Adaptation vs Authority Expansion
**Method adaptation ? authority adaptation.**

- **ORION MAY Adapt Method:** The system can change routing, switch to local edge inference, select alternate communication paths, or retry failures.
- **ORION MAY NOT Expand Authority:** The system cannot grant itself permissions, bypass the OPA engine (VEIL), ignore geofences, or autonomously authorize High/Critical risk actions.

## 5. Research Program (FORGE)
The \experiments/adaptive/\ directory contains isolated, reproducible tests measuring ORION's capability to safely plan and recover from induced failures without violating static security protocols.

- **ADAPT-001:** Demonstrates bounded method adaptation under tested failure scenarios while preserving the defined policy boundary. In the tested scenarios, policy denial and unavailable capabilities caused autonomy to decrease and the planner to enter a fail-safe human-review state rather than escalate authority.
- **ADAPT-002:** Adversarial Capability Selection. Proves that TOCTOU (Time-of-Check to Time-of-Use) races and maliciously poisoned capability metadata cannot trick the planner into bypassing VEIL static policies.
- **ADAPT-003:** Dynamic Capability Discovery. Proves the planner can dynamically ingest new capabilities at runtime and utilize them for recovery, achieving the "intent-driven" orchestration vision.
