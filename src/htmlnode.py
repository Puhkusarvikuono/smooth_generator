class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Method not implemented.")

    def props_to_html(self):
        return_string = ""
        if self.props == None:
            return("HTML tag has no attributes.")
        if type(self.props) is dict: 
            for prop in self.props:
                return_string += f"{prop.strip('"')}={self.props[prop]} "
            return return_string[:-1]
        else:
            return("Invalid attributes. HTML tag has no attributes.")

    def __repr__(self): 
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

