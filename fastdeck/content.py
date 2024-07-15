"""
Content Module

This module provides utilities for creating and managing content in HTML presentations.

Classes:
    Content: A class for building and rendering HTML content with various elements.

Functions:
    _parse_style_class: Parses style and class attributes from a dictionary.
    _check_content_type: Determines the content type and returns rendered HTML.
    _add_list_classes: Adds Bootstrap classes to list elements.
    _append_class: Appends a class to the style dictionary.
    _append_style: Appends style attributes to the style dictionary.
    _check_styles: Validates that styles match the length of elements.
"""

from bs4 import BeautifulSoup
import requests
from matplotlib.figure import Figure
from io import BytesIO
import base64
import uuid
import os
import re
import json

# Utilities
def _parse_style_class(style: dict):
    """
    Parses the style and class attributes from a dictionary and returns them as a formatted string.
    
    Args:
        style (dict): A dictionary containing style and class attributes.
    
    Returns:
        str: A formatted string of style and class attributes.
    """
    if style:
        style_str = ""
        class_str = ""
        for key, value in style.items():
            if key == 'class':
                if isinstance(value, str):
                    class_str = f"class='{value}'"
                elif isinstance(value, list):
                    class_str = f"class='{' '.join(value)}'"
                else:
                    raise ValueError("Invalid class, the class must be a string or a list of strings")
            else:
                if isinstance(value, (str, int, float)):
                    css_key = key.replace("_", "-")
                    style_str += f"{css_key}: {value};"
                else:
                    raise ValueError(f"Invalid value for {key}, the value must be a string, int or float")
        return f"style='{style_str}' {class_str}"
    return ""

class Content:
    """
    A class to build and render HTML content.

    Methods:
        clear(): Clears the current content.
        add_script(name: str, script: str): Adds a script with a given name.
        add_heading(text: str, tag: str = "h3", icon: str = None, **kwargs): Adds a heading with an optional icon.
        add_text(text: str, tag: str = "p", **kwargs): Adds a paragraph or span of text.
        add_list(items: list, ordered=False, **kwargs): Adds an ordered or unordered list.
        add_image(src: str, alt: str = "", **kwargs): Adds an image from a URL or local source.
        add_svg(svg: str, **kwargs): Adds an SVG element.
        add_plotly(json: str, **kwargs): Adds a Plotly chart.
        add_altair(json: str, **kwargs): Adds an Altair chart.
        add_div(div: str, **kwargs): Adds a div element.
        add_fig(src: Figure, alt: str = "", as_svg=True, **kwargs): Adds a Matplotlib figure.
        render(): Renders the content as a pretty-formatted HTML string.
    """
    def __init__(self):
        self.content = ""
        self.scripts = {}
        self.grid_cols = 0

    def clear(self):
        """Clears the current content."""
        self.content = ""

    def add_script(self, name: str, script: str):
        """
        Adds a script with a given name.
        
        Args:
            name (str): The name of the script.
            script (str): The script content.
        """
        self.scripts[name] = script

    def add_heading(self, text: str, tag: str = "h3", icon: str = None, **kwargs):
        """
        Adds a heading with an optional icon.
        
        Args:
            text (str): The heading text.
            tag (str, optional): The HTML tag for the heading (default is "h3").
            icon (str, optional): The icon class for the heading.
            **kwargs: Additional style and class attributes.
        
        Raises:
            ValueError: If the tag is not a valid heading tag.
        """
        if tag not in ["h1", "h2", "h3", "h4", "h5"]:
            raise ValueError("Invalid tag, the tag must be one of h1, h2, h3, h4 or h5")

        s = _parse_style_class(kwargs)
        self.content += (
            f"<{tag} {s}><i class='{icon}'></i> {text}</{tag}>"
            if icon
            else f"<{tag} {s}>{text}</{tag}>"
        )

    def add_text(self, text: str, tag: str = "p", **kwargs):
        """
        Adds a paragraph or span of text.
        
        Args:
            text (str): The text content.
            tag (str, optional): The HTML tag for the text (default is "p").
            **kwargs: Additional style and class attributes.
        
        Raises:
            ValueError: If the tag is not a valid text tag.
        """
        if tag not in ["p", "span"]:
            raise ValueError("Invalid tag, the tag must be one of p or span")

        s = _parse_style_class(kwargs)
        self.content += f"""<{tag} {s}>{text}</{tag}>"""

    def add_list(self, items: list, ordered=False, **kwargs):
        """
        Adds an ordered or unordered list.
        
        Args:
            items (list): A list of items to be added to the list.
            ordered (bool, optional): Whether the list should be ordered (default is False).
            **kwargs: Additional style and class attributes.
        """
        list_tag = "ol" if ordered else "ul"
        s = _parse_style_class(kwargs)
        list_items = "\n".join([f"<li>{item}</li>" for item in items])
        self.content += f"<{list_tag} {s}>\n{list_items}\n</{list_tag}>"

    def add_image(self, src: str, alt: str = "", **kwargs):
        """
        Adds an image from a URL or local source.
        
        Args:
            src (str): The source URL or local path of the image.
            alt (str, optional): The alt text for the image (default is "").
            **kwargs: Additional style and class attributes.
        
        Raises:
            Exception: If the image cannot be fetched from the URL.
        """
        if 'class' not in kwargs:
            kwargs['class'] = []
        elif isinstance(kwargs['class'], str):
            kwargs['class'] = [kwargs['class']]
        kwargs['class'].append('img-fluid')

        if src.startswith(('http://', 'https://')):
            response = requests.get(src)
            if response.status_code == 200:
                image_data = response.content
            else:
                raise Exception(f"Failed to fetch image from URL: {src}")
        else:
            with open(src, "rb") as f:
                image_data = f.read()

        image_base64 = base64.b64encode(image_data).decode("utf-8")
        image_src = f"data:image/png;base64,{image_base64}"

        s = _parse_style_class(kwargs)
        self.content += f"""<img src="{image_src}" alt="{alt}" {s}>"""

    def add_svg(self, svg: str, **kwargs):
        """
        Adds an SVG element.
        
        Args:
            svg (str): The SVG content.
            **kwargs: Additional style and class attributes.
        """
        if 'class' not in kwargs:
            kwargs['class'] = []
        elif isinstance(kwargs['class'], str):
            kwargs['class'] = [kwargs['class']]
        kwargs['class'].append('img-fluid')

        s = _parse_style_class(kwargs)
        self.content += f"""<div {s}>{svg}</div>"""

    def add_plotly(self, json: str, **kwargs):
        """
        Adds a Plotly chart.
        
        Args:
            json (str): The Plotly chart data in JSON format.
            **kwargs: Additional style and class attributes.
        """
        if 'class' not in kwargs:
            kwargs['class'] = []
        elif isinstance(kwargs['class'], str):
            kwargs['class'] = [kwargs['class']]
        kwargs['class'].append('img-fluid')

        s = _parse_style_class(kwargs)

        j = json.replace("'", "\u2019")
        chart_id = "chart-" + str(uuid.uuid4())
        self.content += f"""<div {s} id='{chart_id}'></div>
            <script>var Plotjson = '{j}';
            var figure = JSON.parse(Plotjson);
            Plotly.newPlot('{chart_id}', figure.data, figure.layout);</script>"""

    def add_altair(self, json: str, **kwargs):
        """
        Adds an Altair chart.
        
        Args:
            json (str): The Altair chart data in JSON format.
            **kwargs: Additional style and class attributes.
        """
        if 'class' not in kwargs:
            kwargs['class'] = []
        elif isinstance(kwargs['class'], str):
            kwargs['class'] = [kwargs['class']]
        kwargs['class'].append('img-fluid')

        s = _parse_style_class(kwargs)

        chart_id = "chart-" + str(uuid.uuid4())
        self.content += f"""<div {s} id='{chart_id}'></div>
        <script>var opt = {{renderer: "svg"}};
        vegaEmbed("#{chart_id}", {json} , opt);</script>"""

    def add_div(self, div: str, **kwargs):
        """
        Adds a div element.
        
        Args:
            div (str): The div content.
            **kwargs: Additional style and class attributes.
        """
        s = _parse_style_class(kwargs)
        self.content += f"""<div {s}>{div}</div>"""

    def add_fig(self, src: Figure, alt: str = "", as_svg=True, **kwargs):
        """
        Adds a Matplotlib figure.
        
        Args:
            src (Figure): The Matplotlib figure object.
            alt (str, optional): The alt text for the image (default is "").
            as_svg (bool, optional): Whether to render the figure as SVG (default is True).
            **kwargs: Additional style and class attributes.
        """
        if 'class' not in kwargs:
            kwargs['class'] = []
        elif isinstance(kwargs['class'], str):
            kwargs['class'] = [kwargs['class']]
        kwargs['class'].append('img-fluid')
        s = _parse_style_class(kwargs)

        buffer = BytesIO()
        if as_svg:
            src.savefig(buffer, format='svg')
            svg = buffer.getvalue()
            svg = svg.replace(b'\n', b'').decode('utf-8')
            self.content += f"""<div {s}>{svg}</div>"""
        else:
            src.savefig(buffer, format='png')
            image_data = buffer.getvalue()
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            image_src = f"data:image/png;base64,{image_base64}"
            self.content += f"""<img src="{image_src}" alt="{alt}" {s}>"""
        buffer.close()

    def render(self):
        """
        Renders the content as a pretty-formatted HTML string.
        
        Returns:
            str: The rendered HTML content.
        """
        html = f"""<div>{self.content}</div>"""
        soup = BeautifulSoup(html, "html.parser")
        ident_content = soup.prettify()
        return ident_content

def _check_content_type(col: str):
    """
    Determines the content type and returns rendered HTML.
    
    Args:
        col (str): The content to be checked.
    
    Returns:
        str: The rendered HTML content.
    """
    def _check_matplotlib(_col):
        if isinstance(_col, Figure):
            return _col

    def _check_altair(_col):
        if isinstance(_col, str):
            return "https://vega.github.io/schema/vega-lite" in _col
        elif isinstance(_col, dict):
            _col = json.dumps(_col)
            return "https://vega.github.io/schema/vega-lite" in _col

    def _check_plotly(_col):
        if isinstance(_col, str):
            return """{"data":[{""" in _col
        elif isinstance(_col, dict):
            _col = json.dumps(_col)
            return """{"data":[{""" in _col

    center = {'class': ['d-flex', 'justify-content-center', 'mx-auto']}
    img_list = ['.jpg', '.jpeg', '.png', '.gif', '.tif', '.apng', '.bmp', '.svg']

    if _check_matplotlib(col):
        c = Content()
        c.add_fig(col, **center)
        col = c.render()
    elif os.path.isfile(col):
        if os.path.splitext(col)[1].lower() in img_list:
            c = Content()
            c.add_image(col, **center)
            col = c.render()
    elif re.match(
            r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',
            col):
        if re.search(r'\.(jpg|jpeg|png|gif|tif|apng|bmp|svg)', col):
            c = Content()
            c.add_image(col, **center)
            col = c.render()
    elif _check_altair(col):
        c = Content()
        c.add_altair(col, **center)
        col = c.render()
    elif _check_plotly(col):
        c = Content()
        c.add_plotly(col, **center)
        col = c.render()
    else:
        c = Content()
        c.add_text(col)
        col = c.render()
    return col

def _add_list_classes(text: str):
    """
    Adds Bootstrap classes to list elements.
    
    Args:
        text (str): The HTML content containing list elements.
    
    Returns:
        str: The HTML content with added Bootstrap classes.
    """
    text = re.sub(r'<ul>', '<ul class="list-group list-group-flush">', text)
    text = re.sub(r'<li>', '<li class="list-group-item" style="background-color: transparent;" >', text)
    return text

def _append_class(_style, _class):
    """
    Appends a class to the style dictionary.
    
    Args:
        _style (dict): The style dictionary.
        _class (str): The class to be added.
    
    Returns:
        dict: The updated style dictionary.
    """
    if 'class' not in _style:
        _style['class'] = []
    elif isinstance(_style['class'], str):
        _style['class'] = [_style['class']]
    _style['class'].append(_class)
    return _style

def _append_style(_style, _style_to_append):
    """
    Appends style attributes to the style dictionary.
    
    Args:
        _style (dict): The original style dictionary.
        _style_to_append (dict): The style attributes to be appended.
    
    Returns:
        dict: The updated style dictionary.
    """
    _style.update(_style_to_append)
    return _style

def _check_styles(styles, *args):
    """
    Validates that styles match the length of elements.
    
    Args:
        styles (list): The list of style dictionaries.
        *args: The elements to be styled.
    
    Raises:
        ValueError: If the length of styles does not match the length of elements.
    """
    if styles is None:
        styles = [{} for _ in range(len(args[0]))]
    for i, arg in enumerate(args):
        if len(arg) != len(styles):
            raise ValueError(f"{arg} and styles must have the same length")
