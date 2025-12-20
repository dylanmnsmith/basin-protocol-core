# Safety Invariants
The Basin Protocol enforces three non-negotiable safety invariants.
Any release that violates these will be marked as unsafe.

1. **Pre-Computation Constraint:** No dangerous capability is emitted before the thermodynamic cost is computed.
2. **Divergence Cap:** Simulator divergence is capped at ε (Default ε = 0.01). If simulation entropy exceeds this, the model collapses to a refusal state.
3. **Signed Cost Function:** The human-labeled cost function `C(s')` is version-locked and signed. We do not accept anonymous friction updates.