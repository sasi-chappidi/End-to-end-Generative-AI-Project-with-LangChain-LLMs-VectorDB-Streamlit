import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    ".env",
    "requirements.txt",
    "setup.py",
    "app.py",
    "research/trials.ipynb"
    "test.py" 
]

for filepath in list_of_files:
    path = Path(filepath)
    if not path.parent.exists():
        os.makedirs(path.parent)
    if not path.exists():
        path.touch()
        logging.info(f"Created file: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")