from .scour import scourString


def svg_minify(svg, settings: dict):
    """Minify SVG main function."""
    svg = scourString(in_string=svg, options=settings)
    return svg, None




class Handler:
    """SVG handler class"""
    def __init__(self, settings: dict):
        self.settings = settings

    def is_binary(self):
        return False

    def extensions(self):
        return ["svg"]

    def name(self):
        return "svg"

    def process(self, raw:str):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            # TODO: Implement
            return raw, None
        elif "minify" == mode:
            return svg_minify(raw, self.settings)
        else:
            logger.warning(f"Unsupported mode '{mode}' for {self.name()} handler, skipping...")
            return raw, None
