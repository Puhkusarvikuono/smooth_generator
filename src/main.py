import os, shutil, sys
from textnode import TextNode
from htmlnode import HTMLNode, ParentNode
from markdown_utils import markdown_to_html_node, extract_title



def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    docs_path = os.path.abspath("docs/")
    static_path = os.path.abspath("static/")
    safe_remove(docs_path)
    copy_function(static_path, docs_path)
    generate_pages_recursive("content/", "template.html", "docs/", basepath)

def safe_remove(path):
    if os.path.exists(path):
        files = os.listdir(path)
        if files == []:
            print("Directory empty")
            return
        print(f"There are these files here: {files}")
        for file in files:
            file_path = path + "/" + file
            if os.path.isfile(file_path):
                print(f"Attempting to delete file: {file}")
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting: {e}")
                print(f"Deleted file: {file}")
            if os.path.isdir(file_path):
                try:
                    print(f"Attempting to delete directory: {file_path}")
                    shutil.rmtree(file_path)
                    print(f"Deleted directory, subdirectories and files")
                except Exception as e:
                    print(f"Error deleting directory: {e}")
        print("All files gone")

def copy_function(copy_from, copy_to):
    if os.listdir(copy_to) != []:
        raise Exception(f"Location directory is not empty.")
    copy_list = os.listdir(copy_from)
    if copy_list == []:
        print(f"Copied all from {copy_from}")
        return 
    print(f"There are these files here: {copy_list}")
    for file in copy_list:
        from_file_path = copy_from + "/" + file
        to_file_path = copy_to + "/" + file
        if os.path.isfile(from_file_path):
            new_file_path = shutil.copy(from_file_path, to_file_path)
            print(f"Copied new file: {new_file_path}")
        if os.path.isdir(from_file_path):
            try:
                os.mkdir(to_file_path)
            except Exception as e:
                print(f"Error creating directory: {e}")
            print(f"Copied directory to {to_file_path}  Moving to subfiles.")
            copy_function(from_file_path + "/", to_file_path)
    print("Everything is copied.")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    new_page = template.replace("{{ Title }}", title).replace("{{ Content }}", content).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    directory_creator(dest_path)
    with open(dest_path, mode='w') as file:
        print(f"Creating file: {dest_path}")
        file.write(new_page)

def directory_creator(dest_path):
    if not dest_path.startswith("docs/"):
        raise Exception("Invalid destionation directory")
    file_name = dest_path.split("/")[-1]
    if file_name == "":
        raise Exception("No filename given.")
    directory_path = dest_path.rstrip(file_name)
    if os.path.exists(directory_path):
        print("Directory already exist")
        return
    try:
        print("Trying to create missing directories.")
        os.makedirs(directory_path)
        print(f"Created directory path {directory_path}")
    except Exception as e:
        print(f"Something went wrong: {e}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_files = os.listdir(dir_path_content)
    for content_file in content_files:
        dest_file_path = os.path.join(dest_dir_path, content_file)
        content_file_path = os.path.join(dir_path_content, content_file)
        if content_file.endswith(".md"):
            print(f"Found Markdown file {content_file} in {dir_path_content}")
            generation_dest_path = dest_file_path.replace(".md", ".html")
            generate_page(content_file_path, template_path, generation_dest_path, basepath)
        if os.path.isdir(content_file_path):
            print(f"Moving to subdirectory: {content_file}.")
            generate_pages_recursive(content_file_path, template_path, dest_file_path, basepath)

if __name__ == "__main__":
    main()
