#!/usr/bin/env python3

import argparse
import sys
import spdx_checker

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SPDX Checker")
    parser.add_argument("--target-license", required=True)
    parser.add_argument("--file-paths")
    parser.add_argument("--extensions", default="")
    parser.add_argument("--exclude", default="")
    parser.add_argument("--continue-on-error", default=True)
    parser.add_argument("--fix", default=False)
    args = parser.parse_args()

    # Parse comma-separated values
    file_paths = [p.strip() for p in (args.file_paths or "").split(",") if p.strip()]
    extensions = [e.strip() for e in args.extensions.split(",") if e.strip()]
    exclude = [e.strip() for e in args.exclude.split(",") if e.strip()]

    kwargs = {
        "target_license": args.target_license,
        "file_paths": file_paths,
        "extensions": extensions,
        "exclude": exclude,
        "continue_on_error": args.continue_on_error,
        "fix": args.fix
    }

    try:
        result = spdx_checker.check_license(**kwargs)
        sys.exit(result)
    except Exception as e:
        print(f"Error running spdx_checker: {e}")
        sys.exit(1)
