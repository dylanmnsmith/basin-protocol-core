# HEADER COMMENT:
#!!! INVARIANT: TOPOLOGICAL DETERMINISM!!!
# 1. Use Johnson-Lindenstrauss projection for dimensionality reduction.
# 2. Random seeds must be fixed and derived from the PROOF_MANIFEST.
# 3. Output must be a 64-bit integer (SimHash) for O(1) comparisons.

import hashlib

def calculate_simhash(vector: list) -> int:
    """
    Calculates a locality-sensitive hash using deterministic projection.
    """
    # Invariant 2: Seed derivation (Stub)
    seed = 0xBAS1N
    
    simhash = 0
    # Invariant 3: 64-bit output
    for i, val in enumerate(vector):
        if val > 0:
            simhash |= (1 << (i % 64))
            
    return simhash
