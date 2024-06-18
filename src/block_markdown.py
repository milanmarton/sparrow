from enum import Enum

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
    if not lines:
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
    
