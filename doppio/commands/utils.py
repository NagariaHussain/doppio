from pathlib import Path


def create_file(path: Path, content: str = None):
	# Create the file if not exists
	if not path.exists():
		path.touch()

	# Write the contents (if any)
	if content:
		with path.open("w") as f:
			f.write(content)
