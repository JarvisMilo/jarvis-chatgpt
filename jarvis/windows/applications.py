from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import shutil

@dataclass(frozen=True)
class Application:
    name: str
    executable: str | None = None
    source: str = "unknown"
    arguments: str = ""


def _add(found: dict[str, Application], app: Application) -> None:
    key = app.name.strip().lower()
    if key and key not in found:
        found[key] = app


def _start_menu(found: dict[str, Application]) -> None:
    roots = [
        os.environ.get("ProgramData"),
        os.environ.get("APPDATA"),
    ]
    for root in roots:
        if not root:
            continue
        base = Path(root) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
        if not base.exists():
            continue
        try:
            for path in base.rglob("*"):
                if path.suffix.lower() == ".lnk":
                    _add(found, Application(path.stem, str(path), "start_menu"))
        except OSError:
            continue


def _path_apps(found: dict[str, Application]) -> None:
    for name in ("python", "python3", "git", "ollama", "code", "chrome", "msedge", "firefox"):
        hit = shutil.which(name)
        if hit:
            _add(found, Application(name, hit, "path"))


def _registry_apps(found: dict[str, Application]) -> None:
    if os.name != "nt":
        return
    try:
        import winreg
    except ImportError:
        return
    locations = (
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\App Paths"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\App Paths"),
    )
    for hive, root in locations:
        try:
            with winreg.OpenKey(hive, root) as key:
                for index in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        name = winreg.EnumKey(key, index)
                        with winreg.OpenKey(key, name) as app_key:
                            executable, _ = winreg.QueryValueEx(app_key, None)
                        _add(found, Application(Path(name).stem, str(executable), "registry"))
                    except (OSError, TypeError):
                        continue
        except OSError:
            continue


def discover_applications() -> list[Application]:
    found: dict[str, Application] = {}
    _start_menu(found)
    _registry_apps(found)
    _path_apps(found)
    return sorted(found.values(), key=lambda app: app.name.lower())
