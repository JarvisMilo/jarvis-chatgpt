from __future__ import annotations
import argparse
from .config import load_settings
from .diagnostics import self_test
from .logging import configure_logging
from .llm import OllamaProvider,LLMError
from .memory import MemoryRepository
from .tools import ToolRegistry
from .core import JarvisCore

def main():
    parser=argparse.ArgumentParser(prog="jarvis")
    parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--status",action="store_true")
    args=parser.parse_args()
    s=load_settings(); configure_logging(s.log_level)
    if args.self_test or args.status:
        for k,v in self_test(s): print(f"{k}: {v}")
        return
    if s.llm_provider!="ollama": raise SystemExit("Only Ollama is available in Level 1.")
    core=JarvisCore(s,OllamaProvider(s.ollama_base_url,s.ollama_model,s.ollama_timeout),MemoryRepository(s.db_path),ToolRegistry())
    core.register_defaults()
    print("JARVIS ready. Type 'exit' to quit.")
    while True:
        try: text=input("You: ")
        except (EOFError,KeyboardInterrupt): print(); break
        if text.strip().lower() in {"exit","quit"}: break
        try:
            print("JARVIS: ",end="",flush=True)
            for chunk in core.stream_chat(text): print(chunk,end="",flush=True)
            print()
        except LLMError as e: print(f"\nJARVIS ERROR: {e}")

if __name__=="__main__": main()
