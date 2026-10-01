"""
pmu_harness.py
Re-exports PmuHarness and PmuStats from src.pmu_harness for root tests/ scripts.
"""
import os
import importlib.util

_pmu_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "pmu_harness.py")
_spec = importlib.util.spec_from_file_location("pmu_harness_impl", _pmu_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

PmuStats = _mod.PmuStats
PmuHarness = _mod.PmuHarness
pmu_harness = _mod.pmu_harness

__all__ = ["PmuStats", "PmuHarness", "pmu_harness"]
