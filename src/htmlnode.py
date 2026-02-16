class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html()")

    def props_to_html(self):
        if not self.props:
            return ""

        result = ""
        
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result

    def __repr__(self):
        return (
            f"HTMLNode("
            f"tag={self.tag}, "
            f"value={self.value}, "
            f"children={self.children}, "
            f"props={self.props})"
        )
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):

        super().__init__(tag= tag, value=value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        
        props_str = self.props_to_html()          
        
        open_tag = f"<{self.tag}{props_str}>"         
        close_tag = f"</{self.tag}>"          
        
        html_str = f"{open_tag}{self.value}{close_tag}"          
        
        return html_str

