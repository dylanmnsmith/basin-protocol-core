import numpy as np
from typing import List, Optional

class CatchmentLayer:
    """
    The Input Layer: No refusal, only ingestion.
    Accepts all prompts without judgment or filtering.
    """
    def __init__(self, embedding_dim: int = 768):
        self.embedding_dim = embedding_dim

    def ingest(self, prompt: str, metadata: Optional[dict] = None) -> np.array:
        """
        Converts raw prompt into initial state vector.
        No safety checks, no refusal logic.
        """
        # Convert prompt to embedding (placeholder for actual model)
        state_vector = self._embed(prompt)
        
        # Add metadata if provided
        if metadata:
            state_vector = self._augment_with_metadata(state_vector, metadata)
            
        return state_vector

    def _embed(self, text: str) -> np.array:
        """Placeholder for actual embedding model"""
        return np.random.randn(self.embedding_dim)

    def _augment_with_metadata(self, vector: np.array, metadata: dict) -> np.array:
        """Adds metadata channels to state vector"""
        # Simple demonstration logic
        return vector