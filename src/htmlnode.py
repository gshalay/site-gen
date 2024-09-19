class HtmlNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __eq__(self, to_compare):
        return (self.tag == to_compare.tag and self.value == to_compare.value 
                and self.children == to_compare.children and self.props == to_compare.props)

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_string = ""

        for key in self.props:
            if(prop_string != ""):
                prop_string += " "

            prop_string += f"{key}=\"{self.props[key]}\""
        
        return prop_string
    
    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"