from jsbeautifier.javascript.options import BeautifierOptions
from jsbeautifier.javascript.beautifier import Beautifier

import pprint
import logging

logger = logging.getLogger(__name__)

class Handler:
    """JS handler class"""
    def __init__(self, settings: dict):
        self.settings = settings

    def is_binary(self):
        return False

    def extensions(self):
        return ["js"]

    def name(self):
        return "js"

    def process(self, raw:str):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            b = Beautifier()
            opts = BeautifierOptions()
            js = b.beautify(raw, opts)
            logger.info(f"returning beautified {js}")
            return js, None
        elif "minify" == mode:
            # TODO: Implement
            logger.info(f"returning minified {raw}")
            return raw, None
        else:
            logger.warning(f"Unsupported mode '{mode}' for {self.name()} handler, skipping...")
            return raw, None

