from pathlib import Path
from typing import List


def profile_paths() -> List[Path]:
    return [
        Path(__file__).parent.absolute(),
    ]
