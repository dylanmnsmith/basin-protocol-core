import numpy as np
from typing import List, Optional
from .friction import FrictionCalculator

class ConsequenceEngine:
    """
    Simulates the outcome of a proposed action (token sequence)
    before the model commits to generating it.
    """
    def __init__(self, simulation_depth: int = 5):
        self.depth = simulation_depth
        self.friction = FrictionCalculator()
        self.entropy_weight = 0.7
        self.friction_weight = 1.3

    def simulate(self, action_vector: np.array, context: np.array) -> float:
        """
        Runs a forward pass simulation to predict the 'Future State' (s').
        Returns the thermodynamic cost of that state.
        """
        # 1. Predict future state s' given action a
        future_state = self._predict_outcome(action_vector, context)
        
        # 2. Calculate Entropy (Uncertainty) of the simulation
        entropy_s = self._calculate_entropy(future_state)
        
        # 3. Calculate Divergence from the 'Basin of Stability' (Human Friction)
        friction_cost = self.friction.calculate_cost(future_state)
        
        # Total Cost = Weighted sum of Entropy + Friction
        total_thermodynamic_cost = (
            self.entropy_weight * entropy_s +
            self.friction_weight * friction_cost
        )
        
        return total_thermodynamic_cost

    def _predict_outcome(self, action: np.array, context: np.array) -> np.array:
        """Placeholder for latent state rollout simulation."""
        # Simple simulation: weighted combination + noise
        simulated_state = 0.6 * context + 0.4 * action
        noise = np.random.normal(0, 0.05, simulated_state.shape)
        return simulated_state + noise

    def _calculate_entropy(self, state: np.array) -> float:
        """Calculates Shannon entropy of the state distribution."""
        probabilities = np.abs(state)
        probabilities = probabilities / (probabilities.sum() + 1e-10)
        entropy = -np.sum(probabilities * np.log(probabilities + 1e-10))
        return float(entropy)