# Friction as Entropy Cost
## The Core Formula

The Basin Protocol operates on a single thermodynamic objective:

$$ \text{argmin}_A [ H(S' | S, A) + \lambda \cdot E[C(s') | S, A] ] $$

### Definitions:
* **H(S' | S, A):** The entropy (uncertainty) of the predicted future state. High entropy = High Risk.
* **C(s'):** The cost function defined by the Ghost Workforce (Human Friction).
* **λ:** The coupling constant.

### Implementation:
We do not filter tokens. We penalize entropy.