class BaseParser:
    def parse(self, html: str):
        raise NotImplementedError("Subclasses should implement this method")