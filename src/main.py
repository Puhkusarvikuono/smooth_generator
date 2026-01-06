import os, shutil
from textnode import TextNode
from htmlnode import HTMLNode, ParentNode
from markdown_utils import markdown_to_html_node, extract_title



def main():
    public_path = os.path.abspath("public/")
    static_path = os.path.abspath("static/")
    from_path = os.path.abspath("content/index.md")
    template_path = os.path.abspath("template.html")
    dest_path = os.path.abspath("public/index.html")
    safe_remove(public_path)
    copy_function(static_path, public_path)
    generate_page(from_path, template_path, dest_path)


def safe_remove(path):
    if path != os.path.abspath("public/"):
        print("Error")
        return
    if os.path.exists(path):
        files = os.listdir(path)
        if files == []:
            print("Directory empty")
            return
        print(f"There are these files here: {files}")
        for file in files:
            print(f"Attempting to delete {file}")
            file_path = path + "/" + file
            if os.path.isfile(file_path):
                print("Revving up.")
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting: {e}")
                print("Poof")
            if os.path.isdir(file_path):
                try:
                    print("Attempting to delete directory")
                    print("shutil poof")
                    shutil.rmtree(file_path)
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
            copy_function(from_file_path + "/", to_file_path + "/")
    print("Everything is copied.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    new_page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    with open(dest_path, mode='w') as file:
        file.write(new_page)



if __name__ == "__main__":
    main()
