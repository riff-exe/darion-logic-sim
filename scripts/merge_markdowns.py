import argparse
import os
import sys

def merge_markdowns(target_dir, output_file=None):
    target_dir = os.path.expanduser(target_dir.strip().strip("'\""))

    # Resolve relative paths: check current working directory first, then repository root
    if not os.path.isabs(target_dir):
        if not os.path.isdir(target_dir):
            repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            candidate = os.path.join(repo_root, target_dir)
            if os.path.isdir(candidate):
                target_dir = candidate

    target_dir = os.path.abspath(target_dir)

    if not os.path.isdir(target_dir):
        print(f"Error: Directory '{target_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Determine default output file if not provided
    if not output_file:
        norm_dir = os.path.normpath(target_dir)
        parent_dir = os.path.dirname(norm_dir)
        folder_name = os.path.basename(norm_dir)
        if not folder_name or parent_dir == norm_dir:
            output_file = os.path.join(norm_dir, "merged.md")
        else:
            output_file = os.path.join(parent_dir, f"{folder_name}_merged.md")
    else:
        output_file = os.path.abspath(os.path.expanduser(output_file.strip().strip("'\"")))

    print(f"Tracing markdown files in {target_dir}...")

    merged_content = []
    found_files = []

    for root, dirs, files in os.walk(target_dir):
        # Sort directories and files for deterministic traversal
        dirs.sort()
        files.sort()
        for file in files:
            if file.lower().endswith((".md", ".markdown")):
                file_path = os.path.join(root, file)
                # Avoid self-merging if the output file is inside the target folder
                if os.path.abspath(file_path) == output_file:
                    continue

                rel_path = os.path.relpath(file_path, target_dir)
                found_files.append((file_path, rel_path))

    if not found_files:
        print(f"No markdown files found in {target_dir}.")
        return

    for file_path, rel_path in found_files:
        print(f"Found: {rel_path}")
        merged_content.append(f"# {rel_path}\n\n")
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                merged_content.append(f.read().strip())
        except Exception as e:
            print(f"Warning: Failed to read {file_path}: {e}", file=sys.stderr)
            continue
        merged_content.append("\n\n---\n\n")

    # Ensure parent directory of output file exists
    out_dir = os.path.dirname(output_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("".join(merged_content).strip() + "\n")

    print(f"\nMerged {len(found_files)} markdown file(s) into: {output_file}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Recursively search a folder and its subfolders to merge all markdown files into a single markdown file."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=None,
        help="Target folder path containing markdown files (prompted interactively if omitted).",
    )
    parser.add_argument(
        "output_pos",
        nargs="?",
        default=None,
        help="Optional output markdown file path.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_flag",
        default=None,
        help="Optional output markdown file path (overrides positional output).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    target_dir = args.folder
    output_file = args.output_flag or args.output_pos

    if not target_dir:
        # Prompt interactively if run without arguments in a terminal, or read from pipe
        if sys.stdin.isatty():
            try:
                target_dir = input("Enter folder path to merge markdowns from: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nOperation cancelled.")
                sys.exit(1)
        else:
            piped_input = sys.stdin.read().strip()
            if piped_input:
                target_dir = piped_input

        if not target_dir:
            print("Error: No folder path provided.", file=sys.stderr)
            print("Usage: python merge_markdowns.py <folder_path> [output_file] [-o output_file]", file=sys.stderr)
            sys.exit(1)

    merge_markdowns(target_dir, output_file)


if __name__ == "__main__":
    main()
