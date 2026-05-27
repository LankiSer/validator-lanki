import argparse

import uvicorn

from app.core.config import ensure_data_dirs
from app.paths import FRONTEND_DIR


def main() -> None:
    parser = argparse.ArgumentParser(prog="mini-shop", description="Запуск API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    ensure_data_dirs()

    print(f"API: http://{args.host}:{args.port}/docs")
    print(f"Frontend: cd {FRONTEND_DIR} && npm install && npm run dev")
    print("Логины: admin/admin123, manager/manager123, client/client123")

    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
