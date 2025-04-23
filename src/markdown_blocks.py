from enum import Enum

from htmlnode import ParentNode 
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    # print(blocks)
    new_blocks = []
    for block in blocks:
       if block != "":
            trimmed_block = block.strip().strip("    ")
            split_block = trimmed_block.split("   ")
            # print(split_block)
            new_block = ""
            for split in split_block:
                new_block = new_block + split.strip(" ") # Mysteriously, a whitespace gets added to replace the split tab at the start of a new line.
                # print(new_block)
            new_blocks.append(new_block)
    return new_blocks # Returns a List of blocks.

def block_to_block_type(block):
    lines = block.split("\n")
    # Can alternatively use .startswith method.
    if (block[0:2] == "# " or # Check if block starts with 1-6 #'s, followed by a space, then text.
        block[0:3] == "## " or
        block[0:4] == "### " or
        block[0:5] == "#### " or
        block[0:6] == "##### " or
        block[0:7] == "###### "): 
        return BlockType.HEADING

    if (len(lines) > 1 and
        lines[0].startswith("```") and # Starts w/ ```, ends with ```
        lines[-1].startswith("```")): 
            return BlockType.CODE
    
    list_number = 0
    quote_number = 0
    unordered_number = 0
    ordered_number = 0
    for line in lines: # Every line starts w/ a number, followed by ., and a space. Number starts at 1 and increments by 1.
        if line[0] == ">": # Every line starts w/ >
            quote_number += 1
            # How to check every line before returning?
            """ Try incrementing a counter for each correct line beginning.
                if the counter equals the length of the line list,
                return the BlockType."""
        if line[:2] == "- ": # Every line starts w/ -, followed by a space
            unordered_number += 1
        list_number += 1
        if line[0:3] == f"{list_number}. ":
            ordered_number += 1

    if quote_number == len(lines):
        return BlockType.QUOTE
    if unordered_number == len(lines):
        return BlockType.UNORDERED_LIST
    if ordered_number == len(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children # Returns a List. ParentNode's .to_html method doesn't work on Lists.

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break 
    if level + 1 >= len(block): # Not actually limited to <h6>, only by the block length.
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :] # Exclude the "#"'s and whitespace.
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT) 
    child = text_node_to_html_node(raw_text_node) 
    code = ParentNode("code", [child]) # This makes the text itself a selectable node within a code node.
    return ParentNode("pre", [code]) # Children are kept in an array (as one "object" to fit children in one parameter)

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children)) # Text within <li> as its own node.
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip()) 
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)