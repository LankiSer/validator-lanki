import argparse
import shutil
import subprocess
import sys

import uvicorn

from app.core.config import ensure_data_dirs
from app.paths import FRONTEND_DIR


def _run_frontend() -> None:
    npm = shutil.which("npm")
    if not npm:
        print("npm не найден. Установите Node.js и добавьте npm в PATH.")
        sys.exit(1)

    if not (FRONTEND_DIR / "node_modules").exists():
        print("Устанавливаю npm-зависимости...")
        subprocess.run([npm, "install"], cwd=FRONTEND_DIR, check=True)

    print(f"Frontend dev: http://localhost:5173")
    print(f"Исходники: {FRONTEND_DIR}")
    subprocess.run([npm, "run", "dev"], cwd=FRONTEND_DIR, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mini-shop",
        description="Мини интернет-магазин: backend (FastAPI) + исходники Vue",
    )
    subparsers = parser.add_subparsers(dest="command")

    backend = subparsers.add_parser("backend", help="запустить API (по умолчанию)")
    backend.add_argument("--host", default="127.0.0.1")
    backend.add_argument("--port", type=int, default=8000)
    backend.add_argument("--reload", action="store_true")

    subparsers.add_parser("frontend", help="запустить Vue dev-сервер")
    subparsers.add_parser("frontend-path", help="показать путь к исходникам Vue")

    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")

    args = parser.parse_args()

    if args.command == "frontend-path":
        print(FRONTEND_DIR)
        return

    if args.command == "frontend":
        _run_frontend()
        return

    ensure_data_dirs()

    host = args.host
    port = args.port

    print(f"Backend API: http://{host}:{port}")
    print(f"Docs: http://{host}:{port}/docs")
    print(f"Vue source: {FRONTEND_DIR}")
    print("Frontend: mini-shop frontend")
    print("Admin: admin@example.com / admin123")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
