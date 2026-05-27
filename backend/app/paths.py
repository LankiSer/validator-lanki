from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = APP_DIR.parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
