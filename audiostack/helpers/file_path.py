import os


def validate_and_resolve_file_path(file_path: str) -> str:
    """Validate and resolve a file path for upload operations.

    This function validates that a file path is valid, exists, is a regular
    file (not a directory), and is readable. It also normalises the path by
    expanding user home directory (~) and resolving relative paths to absolute.

    Args:
        file_path: The file path to validate and resolve.

    Returns:
        str: The resolved absolute path to the file.

    Raises:
        ValueError: If file_path is not provided, is not a string, is not a
            valid file path, or is a directory.
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
    """
    if not file_path:
        raise ValueError("Please supply a file path (path to your local file)")

    try:
        expanded_path = os.path.expanduser(file_path)
        resolved_path = os.path.abspath(expanded_path)
    except (OSError, ValueError) as e:
        raise ValueError(f"Invalid file path '{file_path}': {str(e)}") from e

    if not os.path.exists(resolved_path):
        raise FileNotFoundError(
            f"File not found: '{file_path}' " f"(resolved to '{resolved_path}')"
        )

    # Check if it's a file (not a directory)
    if not os.path.isfile(resolved_path):
        if os.path.isdir(resolved_path):
            raise ValueError(f"Path is a directory, not a file: '{file_path}'")
        raise ValueError(f"Path exists but is not a regular file: '{file_path}'")

    # Check if file is readable
    if not os.access(resolved_path, os.R_OK):
        raise PermissionError(f"File is not readable: '{file_path}'")

    return resolved_path
