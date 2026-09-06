"""mac-fleet-canary: independent algorithm modules.

Each module is implemented and exported independently. Import errors here
mean a module claimed the export line without landing the implementation --
keep this file additive-only, one line per merged module.
"""

from .graph_topo_sort import topological_sort

__all__: list[str] = ["topological_sort"]
