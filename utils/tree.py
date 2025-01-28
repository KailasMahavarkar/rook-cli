import re
import os
from pathlib import Path
from typing import Optional


def convert_to_bytes(size_value: float, unit: str) -> int:
    unit = unit.upper()
    if unit == 'GB':
        return int(size_value * 1024 * 1024 * 1024)
    elif unit == 'MB':
        return int(size_value * 1024 * 1024)
    elif unit == 'KB':
        return int(size_value * 1024)
    elif unit == 'B':
        return int(size_value)
    else:
        raise ValueError(f"Invalid size unit: {unit}")


def convert_bytes_to(size_value: int, unit: str) -> float:
    unit = unit.upper()
    if unit == 'GB':
        return size_value / (1024 * 1024 * 1024)
    elif unit == 'MB':
        return size_value / (1024 * 1024)
    elif unit == 'KB':
        return size_value / 1024
    elif unit == 'B':
        return size_value
    else:
        raise ValueError(f"Invalid size unit: {unit}")


def get_folder_size(folder_path: Path) -> int:
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size


def get_tree_helper(
    current_path: Path,
    current_depth: int,
    prefix: str,
    min_file_size: float,
    min_folder_size: float,
    file_unit: str,
    folder_unit: str,
    hide_size: bool,
    show_folder_path: bool,
    show_file_path: bool,
    include_regex: Optional[str],
    exclude_regex: Optional[str],
    folder_only: bool,
    sort: bool
):
    # Base case to stop recursion when depth reaches zero
    if current_depth <= 0:
        return

    # Store the current working directory before processing
    initial_cwd = os.getcwd()

    # Check if the current path is within the initial CWD

    items = list(current_path.iterdir())
    filtered_items = []

    # Compile the include and exclude regex patterns if provided
    if include_regex:
        include_regex = re.compile(include_regex)
    if exclude_regex:
        exclude_regex = re.compile(exclude_regex)

    for item in items:
        # Exclude based on the exclude_regex if provided
        if exclude_regex and exclude_regex.search(str(item)):
            continue

        if include_regex and not include_regex.search(str(item)):
            continue

        if folder_only and not item.is_dir():
            continue

        if item.is_dir():
            folder_size = get_folder_size(item)
            folder_size_in_unit = convert_bytes_to(folder_size, folder_unit)
            if folder_size < min_folder_size:
                continue
        else:
            item_size_in_bytes = item.stat().st_size
            item_size_in_unit = convert_bytes_to(item_size_in_bytes, file_unit)
            if item_size_in_bytes < min_file_size:
                continue

        filtered_items.append(item)

    # Sort items if required (by size or alphabetically)
    if sort:
        filtered_items.sort(key=lambda x: get_folder_size(
            x) if x.is_dir() else x.stat().st_size, reverse=True)
    else:
        filtered_items.sort()

    for i, item in enumerate(filtered_items):
        is_last = i == len(filtered_items) - 1
        connector = "└──" if is_last else "├──"

        if item.is_dir():
            output = f"{prefix}{connector} {item.relative_to(current_path) if show_folder_path else item.name}"
        else:
            output = f"{prefix}{connector} {item.relative_to(current_path) if show_file_path else item.name}"

        if not hide_size:
            if item.is_file():
                output += f" - {item_size_in_unit:.2f} {file_unit}"
            elif item.is_dir():
                output += f" - {folder_size_in_unit:.2f} {folder_unit}"

        yield output

        # Recursion: Decrease depth and pass the new prefix for child elements
        if item.is_dir():
            new_prefix = f"{prefix}{'    ' if is_last else '│   '}"
            # Ensure depth decreases only on directories
            yield from get_tree_helper(
                item,
                current_depth - 1,  # Decrease depth for the next recursive call
                new_prefix,
                min_file_size,
                min_folder_size,
                file_unit,
                folder_unit,
                hide_size,
                show_folder_path,
                show_file_path,
                include_regex.pattern if include_regex else None,
                exclude_regex.pattern if exclude_regex else None,
                folder_only,
                sort
            )

    # Ensure that the CWD is not changed during the recursive traversal
    final_cwd = os.getcwd()
    if initial_cwd != final_cwd:
        print(f"Warning: CWD has changed from {initial_cwd} to {final_cwd}")
