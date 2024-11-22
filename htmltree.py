class TreeNode:
    def __init__(self, tag, attributes=None, content=None):
        self.tag = tag
        self.attributes = attributes or {}
        self.content = content or ""
        self.children = []

    def __repr__(self, level=0):
        indent = " " * (level * 4)
        result = f"{indent}<{self.tag}>\n"
        if self.content.strip():
            result += f"{indent}  {self.content.strip()}\n"
        for child in self.children:
            result += child.__repr__(level + 1)
        result += f"{indent}</{self.tag}>\n"
        return result


def parse_html(html_content):
    from html.parser import HTMLParser

    class CustomHTMLParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.root = None
            self.current_node = None
            self.in_body = False

        def handle_starttag(self, tag, attrs):
            if tag == "body":
                self.in_body = True
                self.root = TreeNode(tag, dict(attrs))
                self.current_node = self.root
            elif self.in_body:
                new_node = TreeNode(tag, dict(attrs))
                if self.current_node:
                    self.current_node.children.append(new_node)
                self.current_node = new_node

        def handle_endtag(self, tag):
            if self.in_body and tag == "body":
                self.in_body = False
            elif self.in_body and self.current_node and self.current_node.tag == tag:
                parent = self.find_parent(self.root, self.current_node)
                self.current_node = parent

        def handle_data(self, data):
            if self.in_body and self.current_node:
                self.current_node.content += data

        def find_parent(self, root, node):
            if not root:
                return None
            for child in root.children:
                if child == node:
                    return root
                result = self.find_parent(child, node)
                if result:
                    return result
            return None

    parser = CustomHTMLParser()
    parser.feed(html_content)
    return parser.root


def main():
    file_name = input("Enter the name of the HTML file to load: ")

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            html_content = file.read()

        tree = parse_html(html_content)

        if tree:
            print("\nTree structure:")
            print(tree)
            
        else:
            print("No <body> tag found in the HTML file.")

    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

