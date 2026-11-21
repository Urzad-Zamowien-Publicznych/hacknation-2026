"""Entry point. Settings are defined here in code instead of command-line arguments.

Run from the repo root:  python -m src.run
"""

from pathlib import Path

from src.text_extraction.docling_models import use_local_models

ROOT = Path(__file__).resolve().parents[1]

# --- Settings ---------------------------------------------------------------
MODE = "run"  # "run" -> process input into output | "eval" -> F1 against training set
INPUT_DIR = ROOT / "dane" / "input"
OUTPUT_DIR = ROOT / "dane" / "output"
MODELS_DIR = ROOT / "models"  # Docling models, downloaded here on first run
# ----------------------------------------------------------------------------


def run(input_dir: Path, output_dir: Path) -> None:
    raise SystemExit("Pipeline not implemented yet (Phase 2).")


def evaluate() -> None:
    raise SystemExit("Evaluator not implemented yet (Phase 1).")


def main() -> None:
    use_local_models(MODELS_DIR)
    if MODE == "run":
        run(INPUT_DIR, OUTPUT_DIR)
    elif MODE == "eval":
        evaluate()
    else:
        raise SystemExit(f"Unknown MODE: {MODE!r}")


if __name__ == "__main__":
    main()
