from os import (
    makedirs,
    path,
    listdir,
    mkdir,
)
import shutil
from block_markdown import (
    markdown_to_htmlnode,
)
import pathlib

def copy_fulldir(src: str, dst: str) -> None:
    if not path.exists(src):
        raise OSError('Source directory not found')
    if not path.exists(dst):
        mkdir(dst)

    for item in listdir(src):
        src_item = path.join(src, item) # get source path of file/dir
        dst_item = path.join(dst, item) # get destination path of file/dir

        if path.isdir(src_item):
            copy_fulldir(src_item, dst_item) # call the function recursively
        else:
            shutil.copy2(src_item, dst_item) # copy if item is a file

def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    title_count = 0
    title = None
    for line in lines:
        if line.startswith('# '):
            parts = line.split(' ', 1)
            if len(parts) < 2:
                raise SyntaxError('There might be an empty h1 heading in your markdown')
            title_count += 1
            title = parts[1]
    if title_count != 1 or title is None:
        raise SyntaxError('There is no h1 header or there are more than one h1 header!')
    return title

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')   

    with open(from_path, 'r') as md:
        md_contents = md.read()
    with open(template_path, 'r') as tp:
        tp_contents = tp.read()

    html = markdown_to_htmlnode(md_contents).to_html()
    title = extract_title(md_contents)

    html_file = tp_contents.replace('{{ Title }}', title).replace('{{ Content }}', html)
    # if not path.exists(dest_path):
        # mkdir(dest_path)
    with open(dest_path, 'w') as dst:
        dst.write(html_file)

    # shutil.copy2('./index.css', './public/index.css')
    # copy_fulldir('./images', './public/images')

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    if not path.exists(dir_path_content):
        raise OSError('Content directory not found')
    if not path.exists(dest_dir_path):
        makedirs(dest_dir_path)

    concrete_template_path = pathlib.Path(template_path)

    for item in listdir(dir_path_content):
        src_item = path.join(dir_path_content, item)
        dst_item = path.join(dest_dir_path, item)

        if path.isdir(src_item):
            generate_pages_recursive(src_item, str(concrete_template_path), dst_item)
        elif src_item.endswith('.md'):
            dst_item = dst_item.replace('.md', ".html")
            generate_page(src_item, str(concrete_template_path), dst_item)
        else:
            shutil.copy2(src_item, dst_item)

if __name__ == '__main__':
    generate_pages_recursive('./content', './template.html', './public')
