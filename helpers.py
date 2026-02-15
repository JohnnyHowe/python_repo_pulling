import os
from pathlib import Path
import shutil
import stat
import subprocess
from urllib.parse import urlparse


def is_root_of_repo(path: Path, remote: str) -> bool:
	if not is_root_of_a_repo(path):
		return False

	result = subprocess.run(
		["git", "remote", "get-url", "origin"],
		capture_output=True,
		text=True,
		check=True,
		cwd=str(path.resolve())
	)
	actual_remote = result.stdout.strip()
	return actual_remote == remote


def is_root_of_a_repo(path: Path) -> bool:
	try:
		result = subprocess.run(
			["git", "rev-parse", "--show-toplevel"],
			cwd=path,
			capture_output=True,
			text=True,
			check=True,
		)
		return Path(result.stdout.strip()) == path.resolve()
	except subprocess.CalledProcessError:
		return False


def get_repo_name(url: str) -> str:
	return get_repo_name_and_author(url).split("/")[-1]


def get_repo_name_and_author(url: str) -> str:
	path = urlparse(url).path.rstrip("/")
	return path.removesuffix(".git").lstrip("/")


def delete_repo(path: Path):
	if not is_root_of_a_repo(path):
		raise Exception(f"Trying to delete repo that does not exist at {path}")

	def _remove_readonly(func, path, _):
		os.chmod(path, stat.S_IWRITE)
		func(path)
	shutil.rmtree(path, onexc=_remove_readonly)
