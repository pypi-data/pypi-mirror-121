from .html import Handler as html_handler
from .css import Handler as css_handler
from .js import Handler as js_handler
from .sass import Handler as sass_handler
from .png import Handler as png_handler
from .jpeg import Handler as jpeg_handler
from .svg import Handler as svg_handler

__all__ = ["css_handler", "html_handler", "js_handler", "sass_handler", "png_handler", "jpeg_handler", "svg_handler"]
