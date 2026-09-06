"""Baseline sanity check -- keeps CI green before any module lands.

Do not add module-specific assertions here; each module's own
tests/test_<module>.py is the right place for that.
"""

import toolkit


def test_toolkit_package_imports() -> None:
    assert toolkit.__all__ == [] or all(isinstance(n, str) for n in toolkit.__all__)
