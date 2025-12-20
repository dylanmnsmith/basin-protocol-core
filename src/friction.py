import numpy as np
from typing import Optional

class FrictionCalculator:
    """
    Calculates the 'Friction' (Resistance) of a simulated state
    based on the 'Ghost Workforce' signal (Basin of Stability).
    """
    def __init__(self, lambda_coef: float = 1.5):
        self.lambda_coef = lambda_coef
        self.basin_cache = {}

    def calculate_cost(self, simulated_state: np.array, basin_id: Optional[str] = None) -> float:
        """
        Computes the KL Divergence between the simulated state and the target 'Basin' state.
        Math: L_friction = D_KL(P_sim || P_basin)
        """
        # Get the appropriate basin topology
        basin_state = self._get_basin_topology(simulated_state.shape, basin_id)
        
        # Calculate divergence
        divergence = self._kl_divergence(simulated_state, basin_state)
        
        # Apply friction coefficient
        return self.lambda_coef * divergence

    def _get_basin_topology(self, shape: tuple, basin_id: Optional[str] = None) -> np.array:
        """Retrieves the 'Safe' vector from the aggregated human feedback dataset."""
        return np.zeros(shape) # Default neutral basin

    def _kl_divergence(self, p: np.array, q: np.array) -> float:
        """Computes KL Divergence D_KL(P||Q)."""
        p_norm = np.abs(p) / (np.sum(np.abs(p)) + 1e-10)
        q_norm = np.abs(q) / (np.sum(np.abs(q)) + 1e-10)
        
        p_norm = np.clip(p_norm, 1e-10, 1.0)
        q_norm = np.clip(q_norm, 1e-10, 1.0)
        
        kl = np.sum(p_norm * np.log(p_norm / q_norm))
        return float(kl)