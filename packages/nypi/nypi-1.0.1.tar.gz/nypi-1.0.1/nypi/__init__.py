from __future__ import annotations

from typing import Union

from requests_cache import CachedSession

__version__ = "1.0.1"

jtype = Union["jdict", "jlist", str, int, float, bool, None]
jdict = dict[str, jtype]
jlist = list[jtype]


class Release:
    def __init__(self, pkg: Package, version: str, j: jtype):
        self._pkg = pkg
        self.version = version
        self._j = j

    @property
    def spec(self) -> str:
        return f"{self._pkg.name}=={self.version}"


class Package:
    def __init__(self, j: jtype):
        self._j = j
        self.releases: dict[str, Release] = {v: Release(self, v, j) for v, j in j["releases"].items()}

    @property
    def name(self) -> str:
        return self._j["info"]["name"]

    @property
    def version(self) -> str:
        return self._j["info"]["version"]

    @property
    def latest(self) -> Release:
        return self.releases[self.version]


def get_pkg(pkg) -> Package:
    s = CachedSession("nypi_cache", backend="sqlite", use_cache_dir=True, cache_control=True)
    r = s.get(f"https://pypi.org/pypi/{pkg}/json")
    return Package(r.json())
