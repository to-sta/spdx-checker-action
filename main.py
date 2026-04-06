#!/usr/bin/env python3

import argparse
import fnmatch
import os
import sys

import spdx_checker


def str_to_bool(value: str) -> bool:
    """Convert a string to a boolean value."""
    return value.strip().lower() in ("true", "1", "yes")


def walk_directories(paths: list[str]) -> list[str]:
    """Walk directories recursively and return all individual file paths."""
    resolved = []
    for path in paths:
        if os.path.isfile(path):
            resolved.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for f in files:
                    resolved.append(os.path.join(root, f))
        else:
            print(f"Warning: path not found: {path}")
    return resolved


def is_within_scope(file_path: str, scope_dirs: list[str]) -> bool:
    """Check if a file path falls within any of the scoped directories."""
    normalized = os.path.normpath(file_path)
    for scope in scope_dirs:
        scope_norm = os.path.normpath(scope)
        if normalized.startswith(scope_norm + os.sep) or normalized == scope_norm:
            return True
    return False


def filter_files(
    files: list[str],
    extensions: list[str],
    exclude: list[str],
) -> list[str]:
    """Filter file list by extensions and exclusion patterns."""
    result = files

    # Filter by extensions (if provided)
    if extensions:
        ext_set = {e if e.startswith(".") else f".{e}" for e in extensions}
        result = [f for f in result if os.path.splitext(f)[1] in ext_set]

    # Apply exclusion patterns
    if exclude:
        result = [
            f for f in result
            if not any(fnmatch.fnmatch(f, pat) for pat in exclude)
        ]

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SPDX Checker")
    parser.add_argument("--target-license", required=True)
    parser.add_argument("--file-paths", default="")
    parser.add_argument("--changed-files", default="")
    parser.add_argument("--extensions", default="")
    parser.add_argument("--exclude", default="")
    parser.add_argument("--continue-on-error", default="false")
    parser.add_argument("--fix", default="false")
    args = parser.parse_args()

    # Parse comma-separated values
    file_paths = [p.strip() for p in args.file_paths.split(",") if p.strip()]
    changed_files = [f.strip() for f in args.changed_files.split(",") if f.strip()]
    extensions = [e.strip() for e in args.extensions.split(",") if e.strip()]
    exclude = [e.strip() for e in args.exclude.split(",") if e.strip()]

    # Convert string booleans to actual booleans
    continue_on_error = str_to_bool(args.continue_on_error)
    fix = str_to_bool(args.fix)

    # Determine which files to check
    if file_paths and changed_files:
        # Scope provided + PR with changes: only check changed files within scope
        scoped = [f for f in changed_files if is_within_scope(f, file_paths)]
        files_to_check = filter_files(scoped, extensions, exclude)
    elif file_paths:
        # Scope provided, no changed files: check all files in scope directories
        all_files = walk_directories(file_paths)
        files_to_check = filter_files(all_files, extensions, exclude)
    elif changed_files:
        # No scope, but have changed files: check all changed files
        files_to_check = filter_files(changed_files, extensions, exclude)
    else:
        print("No file paths or changed files provided.")
        sys.exit(0)

    if not files_to_check:
        print("No files to check after filtering.")
        sys.exit(0)

    kwargs = {
        "target_license": args.target_license,
        "file_paths": files_to_check,
        "continue_on_error": continue_on_error,
        "fix": fix,
    }

    try:
        result = spdx_checker.check_license(**kwargs)
        sys.exit(result)
    except Exception as e:
        print(f"Error running spdx_checker: {e}")
        sys.exit(1)
