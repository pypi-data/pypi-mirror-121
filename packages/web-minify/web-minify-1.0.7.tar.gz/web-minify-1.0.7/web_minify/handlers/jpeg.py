# https://engineeringblog.yelp.com/2017/06/making-photos-smaller.html


def jpeg_minify(jpeg, settings: dict):
    """Minify JPEG main function."""
    # TODO: Implement this
    # print(f"JPEG WAS CALLED FOR {len(jpeg)}!!!!! #############################################")
    return jpeg, None


class Handler:
    """JPEG handler class"""
    def __init__(self, settings: dict):
        self.settings = settings

    def is_binary(self):
        return True

    def extensions(self):
        return ["jpeg", "jpg"]

    def name(self):
        return "jpeg"

    def process(self, raw:str):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            # TODO: Implement
            return raw, None
        elif "minify" == mode:
            return jpeg_minify(raw, self.settings)
        else:
            logger.warning(f"Unsupported mode '{mode}' for {self.name()} handler, skipping...")
            return raw, None
