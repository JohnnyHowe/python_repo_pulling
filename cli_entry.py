from scripts.clone_repo import main
from pathlib import Path
import sys

PACKAGE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE_DIR))

if __name__ == "__main__":
    main()
