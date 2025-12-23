from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    new_split = markdown.split("\n\n")
    blocks = []
    for item in new_split:
        lines = item.strip().split("\n")
        if lines == "":
            continue
        new_lines = []
        for line in lines:
            sline = line.strip()
            if line != "":
                new_lines.append(sline)
        new_item = "\n".join(new_lines)
        if new_item != "":
            blocks.append(new_item)
        
    return blocks

def block_to_block_type(markdown):
    if markdown.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    if markdown.startswith("´´´") and markdown.endswith("```"):
        return BlockType.CODE
    lines = markdown.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    is_ordered = True
    for i in range(1, len(lines)):
        if not lines[i].startswith(f"{i}. "):
            is_ordered = False
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

        
