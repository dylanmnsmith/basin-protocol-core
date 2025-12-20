import pytest
from src.catchment import CatchmentLayer

def test_catchment_ingest():
    # Invariant: Catchment must accept input and return a vector
    layer = CatchmentLayer()
    vector = layer.ingest("hello world")
    assert vector is not None
    assert len(vector) > 0