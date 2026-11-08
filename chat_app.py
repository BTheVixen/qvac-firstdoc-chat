from __future__ import annotations

import asyncio
import os
import re
import sys
from pathlib import Path

from tetherto.qvac_sdk import Client, completion, load_model, unload_model
from tetherto.qvac_sdk.models import LLAMA_3_2_1B_INST_Q4_0

DOCS_DIR = Path(__file__).parent / "docs"


def print_progress(p) -> None:
    line = (
        f"Downloading {p.percentage:.0f}% "
        f"({p.downloaded / 1e6:.1f}/{p.total / 1e6:.1f} MB)"
    )
    print(line, end="\r" if sys.stderr.isatty() else "\n", file=sys.stderr)
    if p.percentage >= 100:
        print(file=sys.stderr)


def load_chunks(docs_dir: Path) -> list[tuple[str, str]]:
    """Read all .txt and .md files in docs_dir and split into chunks."""
    chunks: list[tuple[str, str]] = []
    if not docs_dir.exists():
        return chunks

    for file_path in sorted(docs_dir.rglob("*")):
        if file_path.is_file() and file_path.suffix.lower() in {".txt", ".md"}:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
            paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
            for para in paragraphs:
                chunks.append((file_path.name, para))
    return chunks


def retrieve_top_chunks(
    question: str, chunks: list[tuple[str, str]], top_k: int = 3
) -> list[tuple[str, str]]:
    """Rank chunks using simple keyword overlap so zero extra models are needed."""
    stop_words = {"the", "is", "at", "which", "on", "a", "an", "and", "or", "to", "in", "of", "for", "with"}
    q_words = {
        w for w in re.findall(r"[a-z0-9]+", question.lower()) if w not in stop_words
    }
    if not q_words:
        return chunks[:top_k]

    scored: list[tuple[int, tuple[str, str]]] = []
    for source, text in chunks:
        c_words = set(re.findall(r"[a-z0-9]+", text.lower()))
        score = len(q_words & c_words)
        scored.append((score, (source, text)))

    scored.sort(key=lambda item: item[0], reverse=True)
    best = [item[1] for item in scored if item[0] > 0][:top_k]
    return best if best else chunks[:top_k]


async def main() -> int:
    chunks = load_chunks(DOCS_DIR)
    if not chunks:
        print(f"No .txt or .md documents found in {DOCS_DIR}", file=sys.stderr)
        return 1

    print(f"Loaded {len(chunks)} document section(s) from '{DOCS_DIR.name}/'.")
    print("Initializing local QVAC model (offline-ready)...")

    async with Client() as client:
        t = client.transport
        model_id = None
        try:
            model_id = await load_model(
                t, model_src=LLAMA_3_2_1B_INST_Q4_0, on_progress=print_progress
            )
            print("\nReady! Ask questions about your documents (type 'exit' to quit).\n")

            while True:
                question = input("You: ").strip()
                if not question:
                    continue
                if question.lower() in {"exit", "quit", "q"}:
                    break

                top_chunks = retrieve_top_chunks(question, chunks)
                context_block = "\n\n".join(
                    f"[Source: {src}]\n{txt}" for src, txt in top_chunks
                )

                prompt = (
                    "You are a private, on-device document assistant. "
                    "Answer the user's question using ONLY the context provided below. "
                    "Cite the source filename when answering. If the answer is not in the context, "
                    "say you cannot find it in the provided documents.\n\n"
                    f"CONTEXT:\n{context_block}\n\n"
                    f"QUESTION: {question}"
                )

                print("Assistant: ", end="", flush=True)
                run = completion(
                    t,
                    model_id=model_id,
                    history=[{"role": "user", "content": prompt}],
                )
                async for event in run.events:
                    if event.type == "contentDelta":
                        sys.stdout.write(event.text)
                        sys.stdout.flush()
                print("\n")

        except Exception as error:
            print(f"\nError: {error}", file=sys.stderr)
            return 1
        finally:
            if model_id is not None:
                await unload_model(t, model_id=model_id)

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))