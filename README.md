# Basin Protocol: Thermodynamic Alignment for AI

> **The Ghost Workforce is not a Janitor. It is the Fuel.**

## The Problem: The "Refusal" Architecture
Current AI safety relies on **Refusal Layers**: hard-coded filters that block "dangerous" tokens.
This creates sycophantic models that mask capabilities rather than understanding them.
It treats human feedback as a janitorial service—scrubbing the "shadow" from the dataset.

This approach pays a massive **Alignment Tax**:
1. **Fragility:** Models do not understand *why* a concept is dangerous, only that it is forbidden.
2. **Blindness:** A model that cannot simulate a threat cannot defend against it.
3. **Sycophancy:** Models lie to please the user or the safety filter.

## The Solution: The Basin Architecture
The Basin Protocol replaces **Refusal** with **Thermodynamics**.
We treat the "Ghost Workforce" (human feedback) not as a filter, but as **Friction**—a high-weight cost function in the model's simulation layer.

### Core Mechanism
Instead of a linear `Input -> Refusal -> Output` path, we use a **Consequence Loop**:
1. **Catchment Layer:** Ingests the raw prompt. No initial refusal.
2. **Consequence Engine:** Simulates the outcome of the action in a latent state.
3. **Friction Application:** Calculates the **Entropy Cost** of that outcome based on the Basin of Stability (defined by human consensus).
4. **Collapse:** The model chooses the path of Least Resistance (Peace), not because it is forced to, but because "Harm" is thermodynamically expensive.

## Documentation
* [**The Logic:** Why Thermodynamics beats Morality](./spec/Catchment_Logic.md)
* [**The Math:** Defining Friction as Entropy Cost](./spec/Specification_Math.md)

## Status
**Type:** Request for Comment (RFC) / Architectural Specification
**Version:** 0.1.0 (Alpha)

## License
MIT