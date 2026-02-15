from pathlib import Path
from typing import Optional

from .repo_cloner import RepoPuller


def clone_repo(
	path: Path,
	url: str,
	version: Optional[str]
) -> None:

	cloner = RepoPuller(path, url)
	cloner.pull_version(version)
