from htmlnode import HtmlNode

class LeafNode(HtmlNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if(self.value == None):
            raise ValueError("Leaf node must have a value.")
        elif(self.tag == None):
            return self.value
        else:    

            leaf_node = f"<{self.tag}" 
            
            if(self.props != None and len(self.props) > 0):
                leaf_node += " "
                leaf_node += self.props_to_html()
                
            leaf_node += f">{self.value}</{self.tag}>"

            return leaf_node
            