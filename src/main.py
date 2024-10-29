from os import *
import shutil
from textnode import *
from constants import *
from markdown_parser import *
from pathlib import Path
import builtins

def main():
    clone_directory_contents("static", "public")
    generate_page_recursive("content", "template.html", "public")
    
    print("FIN.")

def clone_directory_contents(source_dir, dest_dir, prefix=""):
    if(source_dir and dest_dir):
        source_dir = path.realpath(source_dir)
        dest_dir = path.realpath(dest_dir)

        if(path.exists(source_dir)):
            print(f"{prefix}'{source_dir}' exists.")

            if path.exists(dest_dir):
                print(f"{prefix}Destination directory '{dest_dir}' exists. Wiping contents.")
                shutil.rmtree(dest_dir)

            print(f"{prefix}Created '{dest_dir}'.")
            mkdir(dest_dir)
            for entry in listdir(source_dir):
                if(path.isfile(source_dir + "/" + entry)):
                    print(f"{prefix}Copied file @ '{prefix}src: {source_dir}/{entry}' to '{dest_dir}/{entry}'")
                    shutil.copy(source_dir + "/" + entry, dest_dir + "/" + entry)

                elif(path.isdir(source_dir + "/" + entry)):
                    print(f"{prefix}Found directory. Recursing.\n{prefix}src: {source_dir}/{entry}\n{prefix}dest: {dest_dir}/{entry}")
                    clone_directory_contents(source_dir + "/" + entry, dest_dir + "/" + entry, (prefix + "\t"))

        else:
            print(f"{prefix}Fatal Error: '{source_dir}' doesn't exist. Can't clone directory.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_content = ""
    template_content = ""

    with builtins.open(Path(from_path).resolve(), "r") as from_file:
        from_content = from_file.read()

    with builtins.open(Path(template_path).resolve(), "r") as template_file:
        template_content = template_file.read()

    if not path.exists(dest_path.rsplit("/", 1)[0]):
        makedirs(dest_path.rsplit("/", 1)[0])
    
    title = extract_title(from_content)
    from_html = markdown_to_html_node(from_content)
    template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", from_html.to_html())

    dest_file = Path(dest_path).resolve()
    #dest_file.parent.mkdir(exist_ok=True, parents=True)
    dest_file.write_text(template_content)

def generate_page_recursive(content_path, template_path, dest_path):
    current_content_path = Path(content_path).resolve()
    current_template_path = Path(template_path).resolve()

    if(path.exists(current_content_path) and path.exists(current_template_path)):
        for entry in listdir(current_content_path):
            if(path.isfile(str(current_content_path) + "/" + str(entry)) and str(entry).endswith(".md")):
                generate_page(str(current_content_path) + "/" + str(entry), str(current_template_path), dest_path + "/" + str(entry).split(".")[0] + ".html")
            elif(path.isdir(str(current_content_path) + "/" + str(entry))):
                generate_page_recursive(str(current_content_path) + "/" + str(entry), template_path, dest_path + "/" + str(entry))


if(__name__ == "__main__"):
    main()