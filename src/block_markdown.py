from enum import Enum
from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
    text_node_to_html_node
)
from inline_markdown import (
    text_to_textnodes,
)

class block_type(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split('\n\n')
    final_blocks = []
    for block in blocks:
        new_block = block.strip()
        if new_block:
            final_blocks.append(new_block)
        continue

    return final_blocks

def block_to_block(markdown_block: str) -> block_type:
    if is_heading_block(markdown_block):
        return block_type.HEADING
    if is_code_block(markdown_block):
        return block_type.CODE
    if is_quote_block(markdown_block):
        return block_type.QUOTE
    if is_unordered_list_block(markdown_block):
        return block_type.UNORDERED_LIST
    if is_ordered_list_block(markdown_block):
        return block_type.ORDERED_LIST
    return block_type.PARAGRAPH


def is_heading_block(str) -> bool:
    first_part = str.split(' ')[0]
    if len(first_part) >= 1 and len(first_part) <= 6:
        return all(char == '#' for char in first_part)
    return False

def is_code_block(str) -> bool:
    lines = str.splitlines()
    if not lines or len(lines) < 2:
        return False
    if lines[0].strip() == '```' and lines[-1].strip() == '```':
        return True
    return False

def is_quote_block(str) -> bool:
    lines = str.splitlines()
    is_quote = True
    for line in lines:
        if line[0] != '>':
            is_quote = False
            break
    return is_quote    

def is_unordered_list_block(str) -> bool:
    lines = str.splitlines()
    is_unord_list = True
    for line in lines:
        if line[0] == '*' or line[0] == '-':
            continue
        is_unord_list = False
        break
    return is_unord_list   
    
def is_ordered_list_block(str) -> bool:
    lines = str.splitlines()
    is_ord_list = True
    last_line_num = 1
    for line in lines:
        expected_prefix = f'{last_line_num}. '
        if line.startswith(expected_prefix):
            last_line_num += 1
            continue
        is_ord_list = False
        break
    return is_ord_list   
    
def markdown_to_htmlnode(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    root_html_node = ParentNode('div', children=[])
    for block in blocks:
        type = block_to_block(block)    
        if type == block_type.QUOTE:
            block_node = quote_block_to_htmlnode(block)
        elif type == block_type.UNORDERED_LIST:
            block_node = unordered_block_to_htmlnode(block)
        elif type == block_type.ORDERED_LIST:
            block_node = ordered_block_to_htmlnode(block)
        elif type == block_type.CODE:
            block_node = code_block_to_htmlnode(block)
        elif type == block_type.HEADING:
            heading_type = count_hashtags(block)
            if heading_type < 1 or heading_type > 6:
                raise ValueError('Invalid header type (valid:1-6)')
            block_node = heading_block_to_htmlnode(block, heading_type)
        else: # block is a paragraph
            block_node = paragraph_block_to_htmlnode(block)
        root_html_node.children.append(block_node)
    return root_html_node

def quote_block_to_htmlnode(block: str) -> HTMLNode:
    block_content = block[2:] # quotes start with '> '
    text_nodes = text_to_textnodes(block_content)
    content_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return ParentNode('blockquote', children=content_nodes)

def unordered_block_to_htmlnode(block: str) -> HTMLNode:
    list_items = block.strip().split('\n')
    list_item_nodes = []
    for item in list_items:
        clean_item = item.lstrip('- ').strip()
        text_nodes = text_to_textnodes(clean_item)
        content_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        list_item_node = ParentNode('li', children=content_nodes)
        list_item_nodes.append(list_item_node)
    return ParentNode('ul', children=list_item_nodes)

def ordered_block_to_htmlnode(block: str) -> HTMLNode:
    list_items = block.strip().split('\n')
    list_item_nodes = []
    for item in list_items:
        clean_item = item.split('.', 1)[1].strip() # removes the number, period and whitespace from linestart
        text_nodes = text_to_textnodes(clean_item)
        content_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        list_item_node = ParentNode('li', children=content_nodes)
        list_item_nodes.append(list_item_node)
    return ParentNode('ol', children=list_item_nodes)

def code_block_to_htmlnode(block: str) -> HTMLNode:
    cleaned_block = block.strip('`').strip()
    code_node = LeafNode('code', cleaned_block)
    pre_node = ParentNode('pre', children=[code_node])
    return pre_node

def count_hashtags(block: str) -> int:
    heading = block.split(' ', 1)[0]
    return len(heading)

def heading_block_to_htmlnode(block: str, type: int) -> HTMLNode:
    cleaned_block = block.lstrip('#').strip()
    text_nodes = text_to_textnodes(cleaned_block)
    content_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return ParentNode(f'h{type}', children=content_nodes)

def paragraph_block_to_htmlnode(block: str) -> HTMLNode:
    cleaned_block = block.strip()
    text_nodes = text_to_textnodes(cleaned_block)
    content_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return ParentNode('p', children=content_nodes)
    
