"""
{readme_content}

Classes:
    Content: Utilities for creating and managing content in HTML presentations
    Slide: Tools for creating and managing individual slides
    Presentation: Tools for creating and managing full presentations
"""

import os

from .content import Content
from .slide import Slide
from .presentation import Presentation

__all__ = ["Content", "Slide", "Presentation"]

# Read the README content
readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
try:
    with open(readme_path, 'r', encoding='utf-8') as readme_file:
        readme_content = readme_file.read()
    # Replace the placeholder in the module docstring with the README content
    __doc__ = __doc__.format(readme_content=readme_content)
except FileNotFoundError:
    print("README.md not found. The documentation will not include the README content.")

# Control what's shown in the documentation
__pdoc__ = {}

# Hide the __init__ methods
__pdoc__["Content.__init__"] = False
__pdoc__["Slide.__init__"] = False
__pdoc__["Presentation.__init__"] = False

# Ensure all public methods of each class are shown
for cls in [Content, Slide, Presentation]:
    for attr in dir(cls):
        if not attr.startswith("_"):
            __pdoc__[f"{cls.__name__}.{attr}"] = True

# Hide any utility functions or implementation details
__pdoc__["_parse_style_class"] = False
__pdoc__["_check_content_type"] = False
__pdoc__["_add_list_classes"] = False
__pdoc__["_append_class"] = False
__pdoc__["_append_style"] = False
__pdoc__["_check_styles"] = False
__pdoc__["create_slide_html"] = False

# Hide module-level attributes
__pdoc__["content"] = False
__pdoc__["slide"] = False
__pdoc__["presentation"] = False