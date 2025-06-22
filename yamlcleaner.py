import os
import shutil
import argparse

def process_markdown_files(directory):
    processed_dir = os.path.join(directory, "processed")
    unprocessed_dir = os.path.join(directory, "unprocessed")
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(unprocessed_dir, exist_ok=True)

    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                lines = file.readlines()

            dash_indices = [i for i, line in enumerate(lines) if line.strip() == "---"]

            if len(dash_indices) >= 2:
                _, end = dash_indices[0], dash_indices[1]
                new_lines = lines[end + 1:]

                # Remove leading empty lines
                while new_lines and new_lines[0].strip() == "":
                    new_lines.pop(0)

                destination = os.path.join(processed_dir, filename)
                with open(destination, "w", encoding="utf-8") as out_file:
                    out_file.writelines(new_lines)
                print(f"Processed: {filename}")
            else:
                shutil.move(filepath, os.path.join(unprocessed_dir, filename))
                print(f"Unprocessed (malformed): {filename}")
                continue

            # Delete original file if processed successfully
            os.remove(filepath)

def main():
    parser = argparse.ArgumentParser(description="Clean YAML metadata from Markdown files.")
    parser.add_argument("directory", help="Directory containing .md files to process")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Error: Provided path is not a valid directory.")
        return

    process_markdown_files(args.directory)

if __name__ == "__main__":
    main()
