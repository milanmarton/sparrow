from textnode import TextNode
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


if __name__ == '__main__':
    copy_fulldir('./static', './public')
