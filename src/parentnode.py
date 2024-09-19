from htmlnode import HtmlNode

class ParentNode(HtmlNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if(self.tag == None):
            raise ValueError("ParentNode must have a tag type.")
        
        elif(self.children == None or len(self.children) == 0):
            raise ValueError("ParentNode must have at least one child tag.")

        # Recurse and parse.
        else:
            parsed_html = f"<{self.tag}"

            if self.props != None and len(self.props) > 0:
                parsed_html += " " + self.props_to_html()
            
            parsed_html += ">"

            for child in self.children:
                parsed_html += child.to_html()

            parsed_html += f"</{self.tag}>"

            return parsed_html 

