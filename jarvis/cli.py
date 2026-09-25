from __future__ import annotations

import argparse
import sys

from . import __version__
from .config import load_settings
from .core import JarvisCore
from .diagnostics import self_test, status
from .llm import LLMError, OllamaProvider
from .logging import configure_logging
from .memory import MemoryRepository
from .tools import default_tools


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jarvis", description="Local-first JARVIS")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--status", action="store_true")
    group.add_argument("--doctor", action="store_true")
    group.add_argument("--version", action="store_true")
    parser.add_argument("--ui", action="store_true", help="Launch the ambient desktop HUD")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        settings = load_settings()
    except (OSError, ValueError) as exc:
        print(f"JARVIS configuration error: {exc}", file=sys.stderr)
        return 2

    configure_logging(settings.log_level, PathLog.path(settings))

    if args.version:
        print(__version__)
        return 0
    if args.status:
        for key, value in status(settings).items():
            print(f"{key}: {value}")
        return 0
    if args.self_test or args.doctor:
        results = self_test(settings)
        for key, value in results:
            print(f"{key}: {value}")
        return 0 if all(not value.startswith("FAIL") for _, value in results) else 1

    if args.ui:
        from .ui import launch_hud
        launch_hud()
        return 0

    provider = OllamaProvider(settings.ollama_base_url, settings.ollama_model, settings.ollama_timeout)
    core = JarvisCore(
        settings,
        provider,
        MemoryRepository(settings.db_path),
        default_tools(settings.workspace),
    )
    print("JARVIS ready. Type 'exit' to quit.")
    while True:
        try:
            text = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if text.strip().lower() in {"exit", "quit"}:
            return 0
        try:
            print("JARVIS: ", end="", flush=True)
            for chunk in core.stream_chat(text):
                print(chunk, end="", flush=True)
            print()
        except (LLMError, ValueError) as exc:
            print(f"\nJARVIS ERROR: {exc}")


class PathLog:
    @staticmethod
    def path(settings) -> object:
        # Kept tiny so logging remains optional and does not couple config to logging.
        from pathlib import Path
        return Path(settings.db_path).with_name("jarvis.log")


if __name__ == "__main__":
    raise SystemExit(main())
