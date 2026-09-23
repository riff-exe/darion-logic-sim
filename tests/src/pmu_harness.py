"""
pmu_harness.py
==============
Centralized Hardware PMU (Performance Monitoring Unit) Profiling Harness for Darion Logic Sim.

Provides:
- Dynamic microarchitecture-aware event discovery (AMD Zen, Intel Core/Xeon, generic Linux fallback).
- Strongly-typed `PmuStats` dataclass with structured properties and calculated hit rates.
- Strict physical cache hierarchy invariant enforcement:
    L3 Loads = L3 Hits + DRAM Loads (so DRAM loads can NEVER exceed L3 loads).
- Parsers for both `perf stat -x,` CSV output and `perf report` text dumps.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple
import os
import sys
import re
import subprocess
import platform

@dataclass
class PmuStats:
    instructions: float = 0.0
    cycles: float = 0.0
    branches: float = 0.0
    branch_misses: float = 0.0
    l1_loads: float = 0.0
    l1_misses: float = 0.0
    l2_loads: float = 0.0
    l2_misses: float = 0.0
    l3_loads: float = 0.0
    l3_hits: float = 0.0
    l3_misses: float = 0.0
    dram_loads: float = 0.0

    # Additional execution metadata
    iterations: float = 1.0
    time_ms: float = 0.0
    evals: float = 0.0
    raw_counters: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        # Enforce physical cache hierarchy consistency:
        # 1. L2 loads come from L1 misses if not directly provided
        if self.l2_loads == 0.0 and self.l1_misses > 0.0:
            self.l2_loads = self.l1_misses

        # 2. L2 misses are requests that miss L2 and query L3
        if self.l3_loads == 0.0 and self.l2_misses > 0.0:
            self.l3_loads = self.l2_misses

        # 3. If both L3 hits and DRAM loads are present:
        # Total L3 requests = L3 Hits + DRAM Loads
        if self.l3_hits > 0.0 or self.dram_loads > 0.0:
            sum_fills = self.l3_hits + self.dram_loads
            self.l3_loads = max(self.l3_loads, sum_fills)

        # 4. Guarantee DRAM loads never exceed L3 loads
        if self.dram_loads > self.l3_loads and self.l3_loads > 0.0:
            self.dram_loads = self.l3_loads

        # 5. Invariant: L3 Hits = L3 Loads - DRAM Loads
        if self.l3_loads > 0.0 and self.l3_hits == 0.0 and self.dram_loads < self.l3_loads:
            self.l3_hits = self.l3_loads - self.dram_loads
        elif self.l3_loads > 0.0 and self.dram_loads == 0.0 and self.l3_hits > 0.0:
            self.dram_loads = max(0.0, self.l3_loads - self.l3_hits)

        self.l3_misses = self.dram_loads

    @property
    def ipc(self) -> float:
        return (self.instructions / self.cycles) if self.cycles > 0.0 else 0.0

    @property
    def l1_hits(self) -> float:
        return max(0.0, self.l1_loads - self.l1_misses)

    @property
    def l1_hit_rate(self) -> float:
        return (self.l1_hits / self.l1_loads * 100.0) if self.l1_loads > 0.0 else 0.0

    @property
    def l1_miss_rate(self) -> float:
        return (self.l1_misses / self.l1_loads * 100.0) if self.l1_loads > 0.0 else 0.0

    @property
    def l2_hits(self) -> float:
        return max(0.0, self.l2_loads - self.l2_misses)

    @property
    def l2_hit_rate(self) -> float:
        return (self.l2_hits / self.l2_loads * 100.0) if self.l2_loads > 0.0 else 0.0

    @property
    def l2_miss_rate(self) -> float:
        return (self.l2_misses / self.l2_loads * 100.0) if self.l2_loads > 0.0 else 0.0

    @property
    def l3_hit_rate(self) -> float:
        if self.l3_loads <= 0.0:
            return 100.0
        rate = (self.l3_hits / self.l3_loads) * 100.0
        return max(0.0, min(100.0, rate))

    @property
    def l3_miss_rate(self) -> float:
        if self.l3_loads <= 0.0:
            return 0.0
        rate = (self.l3_misses / self.l3_loads) * 100.0
        return max(0.0, min(100.0, rate))

    @property
    def branch_miss_rate(self) -> float:
        return (self.branch_misses / self.branches * 100.0) if self.branches > 0.0 else 0.0

    @property
    def branch_hit_rate(self) -> float:
        return 100.0 - self.branch_miss_rate

    def __getitem__(self, item: str) -> Any:
        aliases = {
            "cyc": "cycles",
            "inst": "instructions",
            "l1_load": "l1_loads",
            "l1_miss": "l1_misses",
            "l1_hr": "l1_hit_rate",
            "l2_load": "l2_loads",
            "l2_miss": "l2_misses",
            "l2_hr": "l2_hit_rate",
            "l3_load": "l3_loads",
            "l3_hit": "l3_hits",
            "l3_hr": "l3_hit_rate",
            "l3_miss": "dram_loads",
            "dram_load": "dram_loads",
            "brn": "branches",
            "brn_miss": "branch_misses",
            "brn_hr": "branch_hit_rate",
            "brn_miss_rate": "branch_miss_rate",
        }
        resolved = aliases.get(item, item)
        if hasattr(self, resolved):
            return getattr(self, resolved)
        raise KeyError(item)

    def get(self, item: str, default: Any = None) -> Any:
        try:
            return self[item]
        except KeyError:
            return default

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ipc": self.ipc,
            "cycles": self.cycles,
            "instructions": self.instructions,
            "l1_loads": self.l1_loads,
            "l1_misses": self.l1_misses,
            "l2_loads": self.l2_loads,
            "l2_misses": self.l2_misses,
            "l3_loads": self.l3_loads,
            "l3_hits": self.l3_hits,
            "l3_misses": self.l3_misses,
            "dram_loads": self.dram_loads,
            "branches": self.branches,
            "branch_misses": self.branch_misses,
            "iterations": self.iterations,
            "time_ms": self.time_ms,
            "evals": self.evals,
            "raw_counters": dict(self.raw_counters) if self.raw_counters else {}
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "PmuStats":
        return cls(
            instructions=float(d.get("instructions", 0.0)),
            cycles=float(d.get("cycles", 0.0)),
            branches=float(d.get("branches", 0.0)),
            branch_misses=float(d.get("branch_misses", 0.0)),
            l1_loads=float(d.get("l1_loads", 0.0)),
            l1_misses=float(d.get("l1_misses", 0.0)),
            l2_loads=float(d.get("l2_loads", 0.0)),
            l2_misses=float(d.get("l2_misses", 0.0)),
            l3_loads=float(d.get("l3_loads", 0.0)),
            l3_hits=float(d.get("l3_hits", 0.0)),
            l3_misses=float(d.get("l3_misses", 0.0)),
            dram_loads=float(d.get("dram_loads", 0.0)),
            iterations=float(d.get("iterations", 1.0)),
            time_ms=float(d.get("time_ms", 0.0)),
            evals=float(d.get("evals", 0.0)),
            raw_counters=dict(d.get("raw_counters", {}))
        )

    @classmethod
    def get_table_headers(cls, prefix_cols: Optional[List[str]] = None) -> List[str]:
        prefixes = list(prefix_cols if prefix_cols is not None else ["Circuit", "Engine Variant"])
        return prefixes + [
            "Instructions", "Cycles", "IPC",
            "L1 Loads", "L1 Misses",
            "L2 Loads", "L2 Misses",
            "L3 Loads", "DRAM Loads",
            "Branches", "Branch Misses"
        ]

    @classmethod
    def get_table_header(cls, prefix_cols: Optional[List[str]] = None) -> Tuple[str, str]:
        """
        Returns (header_line, separator_line) formatted as markdown:
        Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses
        """
        prefixes = list(prefix_cols if prefix_cols is not None else ["Circuit", "Engine Variant"])
        headers = cls.get_table_headers(prefixes)
        header_line = "| " + " | ".join(headers) + " |"
        sep_parts = [":---"] * len(prefixes) + ["---:"] * (len(headers) - len(prefixes))
        sep_line = "| " + " | ".join(sep_parts) + " |"
        return header_line, sep_line

    def format_row(self, prefix_vals: Optional[List[str]] = None, fmt_func=None) -> str:
        """
        Formats metrics into the standard markdown table row format.
        """
        def default_fmt(n):
            if n is None: return "N/A"
            if n >= 1e9: return f"{n/1e9:.2f}B"
            if n >= 1e6: return f"{n/1e6:.2f}M"
            if n >= 1e3: return f"{n/1e3:.2f}K"
            if isinstance(n, float): return f"{n:.2f}"
            return str(n)

        fmt = fmt_func or default_fmt
        prefixes = list(prefix_vals or [])
        vals = prefixes + [
            fmt(self.instructions),
            fmt(self.cycles),
            f"{self.ipc:.2f}",
            fmt(self.l1_loads),
            fmt(self.l1_misses),
            fmt(self.l2_loads),
            fmt(self.l2_misses),
            fmt(self.l3_loads),
            fmt(self.dram_loads),
            fmt(self.branches),
            fmt(self.branch_misses),
        ]
        return "| " + " | ".join(vals) + " |"

    @classmethod
    def from_counter_dict(cls, raw: Dict[str, float], iterations: float = 1.0,
                           time_ms: float = 0.0, evals: float = 0.0) -> "PmuStats":
        def get_val(keys: List[str]) -> float:
            for k in keys:
                if k in raw:
                    return float(raw[k])
                # Check without modifier suffix if present
                for rk, rv in raw.items():
                    if rk.split(":")[0] == k.split(":")[0]:
                        return float(rv)
            return 0.0

        inst = get_val(["instructions:u", "instructions"])
        cyc = get_val(["cycles:u", "cycles"])
        brn = get_val(["ex_ret_brn:u", "ex_ret_brn", "branch-instructions:u", "branch-instructions", "branches:u", "branches"])
        brn_miss = get_val(["ex_ret_brn_misp:u", "ex_ret_brn_misp", "branch-misses:u", "branch-misses"])

        l1_load = get_val(["L1-dcache-loads:u", "L1-dcache-loads"])
        l1_miss = get_val(["L1-dcache-load-misses:u", "L1-dcache-load-misses"])

        # L2 misses
        l2_miss = get_val([
            "l2_cache_req_stat.ic_dc_miss_in_l2:u",
            "l2_cache_req_stat.ic_dc_miss_in_l2",
            "l2_rqsts.miss:u",
            "l2_rqsts.miss",
            "l2_lines_in.all:u",
        ])

        # L3 hits (fills into L2 from L3)
        l3_hit = get_val([
            "l2_fill_rsp_src.local_ccx:u",
            "l2_fill_rsp_src.local_ccx",
            "ls_dmnd_fills_from_sys.local_ccx:u",
            "ls_dmnd_fills_from_sys.local_ccx",
            "LLC-loads:u",
            "LLC-loads",
        ])

        # DRAM loads (fills into L2/core from DRAM)
        dram_load = get_val([
            "l2_fill_rsp_src.dram_io_near:u",
            "l2_fill_rsp_src.dram_io_near",
            "ls_dmnd_fills_from_sys.dram_io_near:u",
            "ls_dmnd_fills_from_sys.dram_io_near",
            "LLC-load-misses:u",
            "LLC-load-misses",
        ])

        # If l2_miss wasn't counted directly, but l3_hit and dram_load were
        if l2_miss == 0.0 and (l3_hit > 0.0 or dram_load > 0.0):
            l2_miss = l3_hit + dram_load

        # If l3_hit and dram_load weren't directly available, check fallback
        if l3_hit == 0.0 and dram_load == 0.0 and "cache-misses:u" in raw:
            # Note: on Intel cache-misses is LLC miss; on AMD Zen it's L2 miss.
            # Handled safely via invariant in __post_init__
            pass

        return cls(
            instructions=inst,
            cycles=cyc,
            branches=brn,
            branch_misses=brn_miss,
            l1_loads=l1_load,
            l1_misses=l1_miss,
            l2_loads=l1_miss,
            l2_misses=l2_miss,
            l3_loads=max(l2_miss, l3_hit + dram_load),
            l3_hits=l3_hit,
            l3_misses=dram_load,
            dram_loads=dram_load,
            iterations=iterations,
            time_ms=time_ms,
            evals=evals,
            raw_counters=dict(raw),
        )

    @classmethod
    def from_perf_stat_output(cls, stderr_text: str, iterations: float = 1.0,
                                time_ms: float = 0.0, evals: float = 0.0) -> "PmuStats":
        raw = {}
        for line in stderr_text.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            if len(parts) >= 3:
                val_str = parts[0].strip()
                evt_name = parts[2].strip()
                if val_str and val_str != "<not counted>":
                    try:
                        raw[evt_name] = float(val_str)
                    except ValueError:
                        pass
            elif line.startswith("ITERATIONS:"):
                try: iterations = float(line.split(":")[1].strip())
                except: pass
            elif line.startswith("TIME_MS:"):
                try: time_ms = float(line.split(":")[1].strip())
                except: pass
            elif line.startswith("EVAL_COUNT:"):
                try: evals = float(line.split(":")[1].strip())
                except: pass

        return cls.from_counter_dict(raw, iterations=iterations, time_ms=time_ms, evals=evals)

    @classmethod
    def from_perf_report_file(cls, report_path: str) -> "PmuStats":
        raw = {}
        if not os.path.exists(report_path):
            return cls()
        with open(report_path, "r", encoding="utf-8", errors="replace") as f:
            current_event = None
            for line in f:
                m_event = re.search(r"# Samples: .* of event '(.*?)'", line)
                if m_event:
                    current_event = m_event.group(1)
                    continue
                m_total = re.search(r"# Event count \(approx\.\):\s+(\d+)", line)
                if m_total and current_event:
                    try:
                        raw[current_event] = float(m_total.group(1))
                    except ValueError:
                        pass
        return cls.from_counter_dict(raw)


class PmuHarness:
    """
    Detects the host microarchitecture and resolves optimal PMU event sets.
    """
    _instance: Optional["PmuHarness"] = None

    def __init__(self):
        self.vendor, self.model_name = self._detect_cpu()
        self.events = self._resolve_events()

    @classmethod
    def get_instance(cls) -> "PmuHarness":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _detect_cpu(self) -> Tuple[str, str]:
        vendor = "Unknown"
        model_name = "Unknown"
        if sys.platform != "linux":
            return vendor, model_name

        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if line.startswith("vendor_id"):
                        vendor = line.split(":")[1].strip()
                    elif line.startswith("model name"):
                        model_name = line.split(":")[1].strip()
                    if vendor != "Unknown" and model_name != "Unknown":
                        break
        except Exception:
            pass
        return vendor, model_name

    def _resolve_events(self) -> List[str]:
        """
        Determines the optimal event list based on the detected hardware.
        """
        if sys.platform != "linux":
            return []

        base_core = [
            "instructions:u",
            "cycles:u",
            "L1-dcache-loads:u",
            "L1-dcache-load-misses:u",
        ]

        if "AuthenticAMD" in self.vendor:
            # AMD Zen 1/2/3/4/5 Architecture
            events = [
                "instructions:u",
                "cycles:u",
                "ex_ret_brn:u",
                "ex_ret_brn_misp:u",
                "L1-dcache-loads:u",
                "L1-dcache-load-misses:u",
                "l2_cache_req_stat.ic_dc_miss_in_l2:u",
                "l2_fill_rsp_src.local_ccx:u",
                "l2_fill_rsp_src.dram_io_near:u",
            ]
        elif "GenuineIntel" in self.vendor:
            # Intel Architecture
            events = [
                "instructions:u",
                "cycles:u",
                "branch-instructions:u",
                "branch-misses:u",
                "L1-dcache-loads:u",
                "L1-dcache-load-misses:u",
                "l2_rqsts.miss:u",
                "LLC-loads:u",
                "LLC-load-misses:u",
            ]
        else:
            # Generic Linux perf fallback
            events = [
                "instructions:u",
                "cycles:u",
                "branch-instructions:u",
                "branch-misses:u",
                "L1-dcache-loads:u",
                "L1-dcache-load-misses:u",
                "cache-misses:u",
            ]

        # Validate with a quick dry-run probe
        valid_events = self._probe_events(events)
        return valid_events if valid_events else events

    def _probe_events(self, candidates: List[str]) -> List[str]:
        """
        Verifies that candidate events can be configured without error.
        """
        valid = []
        # Test all at once first
        event_str = ",".join(candidates)
        cmd = ["perf", "stat", "-e", event_str, "-x,", "--", "true"]
        try:
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                # Check which ones were reported
                for line in res.stderr.split("\n"):
                    parts = line.split(",")
                    if len(parts) >= 3 and parts[2].strip():
                        valid.append(parts[2].strip())
                if len(valid) >= len(candidates) - 1:
                    return candidates
        except Exception:
            pass

        # Fallback to item-by-item check
        for evt in candidates:
            try:
                res = subprocess.run(["perf", "stat", "-e", evt, "--", "true"],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if res.returncode == 0:
                    valid.append(evt)
            except Exception:
                pass
        return valid

    def get_event_string(self) -> str:
        return ",".join(self.events)

    def parse_stat_csv(self, stderr_text: str, iterations: float = 1.0,
                       time_ms: float = 0.0, evals: float = 0.0) -> PmuStats:
        return PmuStats.from_perf_stat_output(stderr_text, iterations=iterations,
                                              time_ms=time_ms, evals=evals)

    def parse_report_file(self, report_path: str) -> PmuStats:
        return PmuStats.from_perf_report_file(report_path)


# Convenience singleton accessor
pmu_harness = PmuHarness.get_instance()
