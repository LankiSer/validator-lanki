"""Сборка Python-пакета для PyPI (без сборки frontend)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    subprocess.run([sys.executable, "-m", "pip", "install", "build"], check=True)
    subprocess.run([sys.executable, "-m", "build"], cwd=ROOT, check=True)

    dist = ROOT / "dist"
    print("\nГотово. Файлы пакета:")
    for file in sorted(dist.glob("*")):
        print(f"  {file.name}")
    print("\nВ пакете исходники Vue в app/frontend/ — без production build.")


if __name__ == "__main__":
    main()
