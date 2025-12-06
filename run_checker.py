#!/usr/bin/env python3
"""Runner script for spdx_checker GitHub Action."""
import argparse
import sys
import spdx_checker

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SPDX Checker")
    parser.add_argument("--target-license", default="", help="Target SPDX license identifier")
    parser.add_argument("--file-paths", default=".", help="Comma-separated file paths")
    parser.add_argument("--extensions", default="", help="Comma-separated file extensions")
    parser.add_argument("--exclude", default="", help="Comma-separated exclude patterns")
    parser.add_argument("--continue-on-error", default="false", help="Continue on error")
    parser.add_argument("--fix", default="false", help="Fix license headers")
    
    args = parser.parse_args()
    
    # Prepare kwargs for spdx_checker
    kwargs = {}
    
    if args.target_license:
        kwargs["target_license"] = args.target_license
    
    if args.file_paths:
        kwargs["file_paths"] = [p.strip() for p in args.file_paths.split(",") if p.strip()]
    
    if args.extensions:
        kwargs["extensions"] = [e.strip() for e in args.extensions.split(",") if e.strip()]
    
    if args.exclude:
        kwargs["exclude"] = [e.strip() for e in args.exclude.split(",") if e.strip()]
    
    kwargs["continue_on_error"] = args.continue_on_error.lower() == "true"
    kwargs["fix"] = args.fix.lower() == "true"
    
    try:
        result = spdx_checker.check_license(**kwargs)
        sys.exit(result)
    except Exception as e:
        print(f"Error running spdx_checker: {e}")
        sys.exit(1)
