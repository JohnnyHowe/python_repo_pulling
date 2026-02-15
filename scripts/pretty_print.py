"""Pretty print utilities for colorized console output."""

from pathlib import Path
from typing import Type


class Colors:
	"""Hex color constants for terminal output."""
	REGULAR=None
	WARNING="#f1c40f"
	ERROR="#e06c75"
	SUCCESS="#98c379"
	TODO="#4F37D7"


def raise_pretty_exception(error: Type[Exception], message: str) -> None:
	"""Print an error message in red and raise the provided exception type."""
	pretty_print(message, color=Colors.ERROR)
	raise error(message)


def pretty_print(*args, color=None, **kwargs) -> None:
	"""Print arguments, optionally colorized with an RGB hex string."""
	text = " ".join(str(a) for a in args)  # join everything manually
	if not color:
		print(text, **kwargs)
		return

	color = color.lstrip("#")
	r, g, b = (int(color[i:i+2], 16) for i in (0, 2, 4))
	print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", **kwargs)


def get_pretty_path_string(path: Path) -> str:
	"""Return a path string including the absolute location for clarity."""
	return f"{path} ({path.absolute()})"
