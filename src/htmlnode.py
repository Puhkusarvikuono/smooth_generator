class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if (value is None) == (children is None):
            # both None or both not None
            raise ValueError("Provide exactly one of value or children")
        if tag is not None and not isinstance(tag, str):
            raise TypeError("tag must be None or str")
        if value is not None and not isinstance(value, str):
            raise TypeError("value must be None or str")
        if children is not None:
            if not isinstance(children, list) or any(not isinstance(c, HTMLNode) for c in children):
                raise TypeError("children must be a list[HTMLNode] or None")
        if props is not None and not isinstance(props, dict):
            raise TypeError("props must be a dict or None")
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError("Method not implemented.")

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())

    def __repr__(self): 
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        if value is None:
            raise ValueError("Provide value")
        if not isinstance(value, str):
            raise TypeError("value must be str")
        if tag is not None and not isinstance(tag, str):
            raise TypeError("tag must be str or None")
        self.value = value

    def to_html(self):
        if self.value is None:
            raise ValueError("All leafnodes must have a value")
        if self.tag is None:
            return self.value
        if self.props_to_html() == "":
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>' 

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
        if tag is None:
            raise ValueError("Provide tag")
        if children is None:
            raise ValueError("Provide children")
        if not isinstance(tag, str):
            raise TypeError("tag must be str")

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parentnodes must have a tag")
        if self.children is None:
            raise ValueError("Value error: Parentnode missing children")
        children_to_html_string = ""
        for child in self.children:
            if child.children is not None:
                child.to_html()
            children_to_html_string += child.to_html()
        if self.props_to_html() == "":
            return f'<{self.tag}>{children_to_html_string}</{self.tag}>'
        else:
            return f'<{self.tag}{self.props_to_html()}>{children_to_html_string}</{self.tag}>'
            

            






