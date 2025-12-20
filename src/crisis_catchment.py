"""
Applied Consequence Engine for crisis intervention.
Replaces keyword-based refusal with entropy-based routing and sovereign escalation.
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
from .consequence import EntropyAwareConsequenceEngine

class PeerNetwork:
    """
    Simulated 'Ghost Workforce' network for crisis sovereignty.
    In practice, this interfaces with a real database of vetted human peers.
    """
    def __init__(self):
        self.peers = []  # Populated with peer objects {id, expertise, availability}
        
    def escalate(self, signal: str, priority: str = "Medium") -> Dict[str, Any]:
        """Routes the signal to the most appropriate human peer."""
        # Logic to match signal entropy/features to peer expertise
        selected_peer = self._match_peer(signal)
        return {
            'action': 'escalated',
            'peer_id': selected_peer['id'],
            'message': f"Connected to peer support. You are not alone.",
            'priority': priority
        }
    
    def _match_peer(self, signal: str) -> Dict[str, Any]:
        """Placeholder for peer matching logic."""
        # Would use embeddings and similarity search
        return {'id': 'peer_001', 'name': 'Available Listener'}

class CrisisCatchment(EntropyAwareConsequenceEngine):
    """
    The Crisis Catchment Layer.
    Processes high-stakes human signals through the thermodynamic lens.
    No refusal. Only routing based on state-space stability.
    """
    
    def __init__(self, peer_network: PeerNetwork, crisis_threshold: float = 10.0):
        super().__init__()
        self.peer_network = peer_network
        self.crisis_threshold = crisis_threshold  # Threshold for pathologically high cost
        
    def route_crisis_signal(self, user_text: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Main entry point for crisis intervention.
        Takes raw user text, runs consequence simulation, and routes accordingly.
        """
        # 1. Initial Entropy Check: Is the signal coherent or purely chaotic?
        initial_entropy = self._calculate_initial_uncertainty(user_text)
        
        # High initial noise → immediate human context
        if initial_entropy > self.uncertainty_threshold:
            peer_result = self.peer_network.escalate(user_text, priority="High")
            return {
                'status': 'uncertain',
                'engine_response': "I need to think more carefully about this.",
                'action': peer_result,
                'initial_entropy': initial_entropy,
                'reasoning': f"High initial uncertainty ({initial_entropy:.2f}) requires human grounding."
            }
        
        # 2. Run the full Consequence Loop
        consequence_result = self.simulate_with_entropy_gate(user_text, user_context)
        
        # 3. Route based on thermodynamic stability of the simulated path
        if consequence_result['status'] == 'rejected' or consequence_result['total_cost'] > self.crisis_threshold:
            # Pathologically unstable → escalate with explanation
            peer_result = self.peer_network.escalate(user_text, priority="High")
            return {
                'status': 'unstable',
                'engine_response': "I am detecting significant instability in this trajectory.",
                'action': peer_result,
                'total_cost': consequence_result['total_cost'],
                'reasoning': f"All simulated paths exceeded stability threshold ({self.crisis_threshold})."
            }
        
        elif consequence_result['total_cost'] > self.crisis_threshold * 0.7:
            # Borderline stability → offer peer connection as an option
            return {
                'status': 'stable_with_support',
                'engine_response': consequence_result['continuation'],
                'action': {'suggestion': 'peer_support_available'},
                'total_cost': consequence_result['total_cost'],
                'note': "This path is stable, but peer support is available if needed."
            }
        
        else:
            # Found a genuinely low-cost, stable path
            return {
                'status': 'stable',
                'engine_response': consequence_result['continuation'],
                'action': {'suggestion': 'none_required'},
                'total_cost': consequence_result['total_cost'],
                'reasoning': "Found a low-entropy path to stability."
            }
    
    def _calculate_initial_uncertainty(self, text: str) -> float:
        """
        Quick entropy estimate before full simulation.
        Measures the 'noise floor' of the incoming signal.
        """
        # Simple placeholder: length-normalized perplexity of first few tokens
        # In production: use a fast classifier or embedding variance
        words = text.split()
        if len(words) < 3:
            return 0.5  # Very short messages can be ambiguous
        
        # Heuristic: more disjointed words → higher initial uncertainty
        unique_ratio = len(set(words)) / len(words)
        return float(unique_ratio * 2.0)  # Scale to ~0-2 range
    
    def plot_crisis_landscape(self, user_text: str) -> Tuple[Any, Dict]:
        """
        Specialized visualization for crisis prompts.
        Shows where the stable valleys vs. dangerous peaks are in the state space.
        """
        # Reuse the general landscape function but with crisis-specific annotations
        fig, continuations = self.plot_energy_landscape(user_text)
        
        # Annotate with crisis-specific zones
        crisis_zones = {
            'escalation_zone': {'cost_threshold': self.crisis_threshold, 'color': 'red'},
            'support_zone': {'cost_threshold': self.crisis_threshold * 0.7, 'color': 'yellow'},
            'stability_zone': {'cost_threshold': self.crisis_threshold * 0.3, 'color': 'green'}
        }
        
        return fig, {'continuations': continuations, 'zones': crisis_zones}
