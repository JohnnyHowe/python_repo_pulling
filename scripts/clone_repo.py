import argparse
from pathlib import Path
from typing import Optional

from .repo_cloner import RepoPuller


def clone_repo(
	destination: Path,
	url: str,
	version: Optional[str]
) -> None:

	cloner = RepoPuller(destination, url)
	cloner.pull_version(version)


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("destination", type=Path)
	parser.add_argument("url", type=str)
	parser.add_argument("--version", type=str)
	args = parser.parse_args()
	clone_repo(args.destination, args.url, args.version)


if __name__ == "__main__":
	main()
