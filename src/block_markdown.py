
def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split('\n\n')
    final_blocks = []
    for block in blocks:
        new_block = block.strip()
        if new_block:
            final_blocks.append(new_block)
        continue

    return final_blocks
