#!/usr/bin/env python3
"""
Cleanup script for Semker project.
Removes __pycache__ directories and .pyc files from the project.
"""

import shutil
import sys
from pathlib import Path
from typing import List


def find_pycache_directories(root_path: Path) -> List[Path]:
    """Find all __pycache__ directories in the project."""
    pycache_dirs: List[Path] = []
    for item in root_path.rglob("__pycache__"):
        if item.is_dir():
            pycache_dirs.append(item)
    return pycache_dirs


def find_pyc_files(root_path: Path) -> List[Path]:
    """Find all .pyc files in the project."""
    pyc_files: List[Path] = []
    for item in root_path.rglob("*.pyc"):
        if item.is_file():
            pyc_files.append(item)
    return pyc_files


def cleanup_python_cache(project_root: str = ".") -> None:
    """
    Clean up Python cache files and directories.
    
    Args:
        project_root: Root directory of the project (default: current directory)
    """
    root_path = Path(project_root).resolve()
    
    if not root_path.exists():
        print(f"Error: Project root '{project_root}' does not exist.")
        sys.exit(1)
    
    print(f"Cleaning up Python cache files in: {root_path}")
    print("-" * 50)
    
    # Find and remove __pycache__ directories
    pycache_dirs = find_pycache_directories(root_path)
    if pycache_dirs:
        print(f"Found {len(pycache_dirs)} __pycache__ directories:")
        for dir_path in pycache_dirs:
            # Skip __pycache__ in virtual environments
            if ".venv" in str(dir_path) or "venv" in str(dir_path):
                print(f"  Skipping (in virtual env): {dir_path.relative_to(root_path)}")
                continue
            
            print(f"  Removing: {dir_path.relative_to(root_path)}")
            try:
                shutil.rmtree(dir_path)
            except OSError as e:
                print(f"    Error removing {dir_path}: {e}")
    else:
        print("No __pycache__ directories found.")
    
    # Find and remove .pyc files
    pyc_files = find_pyc_files(root_path)
    if pyc_files:
        print(f"\nFound {len(pyc_files)} .pyc files:")
        for file_path in pyc_files:
            # Skip .pyc files in virtual environments
            if ".venv" in str(file_path) or "venv" in str(file_path):
                print(f"  Skipping (in virtual env): {file_path.relative_to(root_path)}")
                continue
            
            print(f"  Removing: {file_path.relative_to(root_path)}")
            try:
                file_path.unlink()
            except OSError as e:
                print(f"    Error removing {file_path}: {e}")
    else:
        print("\nNo .pyc files found.")
    
    print("\nCleanup completed!")


if __name__ == "__main__":
    # Allow specifying project root as command line argument
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    cleanup_python_cache(project_root)
