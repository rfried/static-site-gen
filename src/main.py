from process_markdown import generate_pages_recursive
import shutil
import os

def recursive_copy(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for item in os.listdir(source_folder):
        source_path = os.path.join(source_folder, item)
        destination_path = os.path.join(destination_folder, item)
        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
        else:
            shutil.copy2(source_path, destination_path)

def main():
    if os.path.exists('public'):
        shutil.rmtree('public')
    recursive_copy('static', 'public')
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()