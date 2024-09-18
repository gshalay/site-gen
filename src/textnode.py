class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, to_compare):
        return self.text == to_compare.text and self.text_type == to_compare.text_type and self.url == to_compare.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"