from pathlib import Path
import shlex
from typing import Optional

from .helpers import *
from .pretty_print import *


class RepoPuller:
	path: Path
	url: str

	_repo_name: str
	_log_header: str
	_indent_char: str = "    "

	def __init__(self, path: Path, url: str) -> None:
		self.path = path
		self.url = url

		self._repo_name = get_repo_name(url)
		self._log_header = f"[Clone {self._repo_name}] "

	def pull_version(self, version: Optional[str] = None) -> None:
		"""
		version can be a branch name, tag, or commit hash, checked in that order.
		"""
		if version is None:
			version = "HEAD"

		self._log(f"Parameters:")
		self._log(self._indent_char + f"url: {self.url}")
		self._log(self._indent_char + f"path: {self.path}")
		self._log(self._indent_char + f"version: {version}")

		self._clone_if_required()
		self._update_repo(version)

	def _clone_if_required(self) -> None:
		# Fresh clone: nothing at or in clone destination
		if not self.path.exists() or not any(self.path.iterdir()):
			self._log("Nothing exists at clone destination.")
			self._clone_repo()

		# Clear and clone: Something exists, but it isn't a repo
		elif not is_root_of_repo(self.path, self.url):
			self._log("Something exists locally, but it's not the repo we want. Deleting first.", color=Colors.WARNING)
			delete_repo(self.path)

		else:
			self._log(f"Not cloning. A repo exists at {str(self.path.resolve())}")

	def _clone_repo(self):
		self.path.mkdir(parents=True, exist_ok=True)
		command = ["git", "clone", self.url, "--no-checkout", "--depth=1", str(self.path.resolve())]
		self._run_command(command)

	def _update_repo(self, version: str) -> None:
		fetch_command = f"git fetch --tags origin".split(" ") + [version]
		self._run_command(fetch_command)

		checkout_command = "git checkout FETCH_HEAD".split(" ")
		self._run_command(checkout_command)

	def _run_command(self, command: list[str]):
		self._log("> " + shlex.join(command))
		self._log(f"(cwd={self.path})")

		process = subprocess.Popen(command, cwd=self.path, text=True)
		out, err = process.communicate()

		if err:
			for text in err.splitlines():
				is_error = text.startswith("error: ") or text.startswith("fatal: ")
				self._log("    " + text, color = Colors.ERROR if is_error else Colors.REGULAR)

				if is_error:
					self._log("    " + text, color=Colors.ERROR)
					raise Exception(text)

	def _log(self, text: str, *args, **kwargs) -> None:
		pretty_print(self._log_header + text, *args, **kwargs)

