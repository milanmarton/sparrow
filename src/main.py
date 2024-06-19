from os import (
    path,
    listdir,
    mkdir,
)
import shutil

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
    if title_count != 0 or title is None:
        raise ValueError('There is no h1 header or there are more than one h1 header!')
    return title

if __name__ == '__main__':
    copy_fulldir('./static', './public')
