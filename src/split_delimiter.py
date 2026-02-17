import re
from textnode import TextNode, TextType, TextNodeDelimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown Syntax")

        for index, part in enumerate(parts):
            if part == "":
                continue
            elif index % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)

    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for i, image in enumerate(images, 1):
            parts = text.split(f"![{image[0]}]({image[1]})", 1)

            if parts[0] == "":
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            elif parts[1] == "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            else:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            if i == len(images) and parts[1] != "":
                new_nodes.append(TextNode(parts[1], TextType.TEXT))
            else:
                text = parts[1]

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for i, link in enumerate(links, 1):
            parts = text.split(f"[{link[0]}]({link[1]})", 1)

            if parts[0] == "":
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            elif parts[1] == "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            else:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            if i == len(links) and parts[1] != "":
                new_nodes.append(TextNode(parts[1], TextType.TEXT))
            else:
                text = parts[1]

    return new_nodes

def text_to_textnodes(text: str):
    nodes = split_nodes_delimiter(
        old_nodes=[TextNode(text, TextType.TEXT)],
        delimiter=TextNodeDelimiter.BOLD,
        text_type=TextType.BOLD,
    )

    nodes = split_nodes_delimiter(
        old_nodes=nodes,
        delimiter=TextNodeDelimiter.ITALIC,
        text_type=TextType.ITALIC,
    )

    nodes = split_nodes_delimiter(
        old_nodes=nodes,
        delimiter=TextNodeDelimiter.CODE,
        text_type=TextType.CODE,
    )

    nodes = split_nodes_image(old_nodes=nodes)
    nodes = split_nodes_link(old_nodes=nodes)

    return nodes