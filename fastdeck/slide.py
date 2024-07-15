"""
Slide Module

This module provides tools for creating and managing individual slides in a presentation.

Classes:
    Slide: A class representing a single slide in a presentation.

Functions:
    create_slide_html: Creates HTML for a given slide or list of slides.
"""

from matplotlib.figure import Figure
from .content import Content, _check_content_type, _add_list_classes, _parse_style_class, _check_styles

def create_slide_html(slide):
    """
    Creates HTML for a given slide or list of slides.

    Args:
        slide (Slide or list): The slide or list of slides to convert to HTML.

    Returns:
        str: The HTML representation of the slide(s).
    """
    if isinstance(slide, list):
        return "<section>" + "\n" + "\n".join([create_slide_html(subslide) for subslide in slide]) + "</section>"

    kwargs_str = ' '.join([f'{k}="{v}"' for k, v in slide.kwargs.items()])
    return f"""<section {kwargs_str} class='{'center' if slide.center else ''}'>
        <div class='container' style='text-align: left;' >
            {slide.content}
        </div>
    </section>"""

class Slide:
    """
    A class representing a slide in the presentation.

    Attributes:
        content (str): The HTML content of the slide.
        center (bool): Whether the slide content should be centered.
        kwargs (dict): Additional attributes for the slide element.
    """
    def __init__(self, center=False, **kwargs):
        """
        Initializes a new Slide object.

        Args:
            center (bool): Whether the slide content should be centered (default is False).
            **kwargs: Additional attributes for the slide element.
        """
        self.content = ""
        self.center = center
        self.kwargs = kwargs

    def add_title(self, text: str, tag: str = "h3", icon: str = None, **kwargs):
        """
        Adds a title to the slide.

        Args:
            text (str): The title text.
            tag (str, optional): The HTML tag for the title (default is "h3").
            icon (str, optional): The icon class for the title.
            **kwargs: Additional style and class attributes.
        """
        c = Content()
        c.add_heading(text, tag, icon, **kwargs)
        row = "<div class='row'><div class='col-12 mx-auto'>"
        self.content += row + c.render() + "</div></div>"

    def add_content(self, content: list, columns=None, styles: list = None):
        """
        Adds content to the slide.

        Args:
            content (list): A list of content elements (str or Figure).
            columns (list, optional): A list of column sizes for the content elements (default is [12]).
            styles (list, optional): A list of style dictionaries for the content elements.
        """
        if columns is None:
            columns = [12]

        _check_styles(styles, content, columns)

        row = "<div class='row'>"
        for i in range(len(content)):
            col = content[i]
            if isinstance(col, (str, Figure)):
                col = _check_content_type(col)
                if styles and len(styles) > i:
                    col = f"<div class='col-md-{columns[i]}' {_parse_style_class(styles[i])}>{col}</div>"
                else:
                    col = f"<div class='col-md-{columns[i]}'>{col}</div>"
            row += col
        self.content += row + "</div>"

    def add_card(self, cards: list, styles: list = None):
        """
        Adds cards to the slide.

        Args:
            cards (list): A list of card dictionaries with 'image', 'title', and 'text' keys.
            styles (list, optional): A list of style dictionaries for the cards.
        """
        _check_styles(styles, cards)

        if styles is None:
            styles = [{'class': 'bg-info'}] * len(cards)

        cards_html = ""
        for card, style in zip(cards, styles):
            if 'class' not in style:
                style['class'] = []
            elif isinstance(style['class'], str):
                style['class'] = [style['class']]
            style['class'].append('card h-100')

            s = _parse_style_class(style)
            card_html = ""
            for key in card.keys():
                if key == 'image':
                    card_html += f'<img src="{card[key]}" class="card-img-top mx-auto" alt="">'
                elif key == 'title':
                    card_html += f'<h4 class="card-title">{card[key]}</h4>'
                elif key == 'text':
                    card[key] = _add_list_classes(card[key])
                    card_html += f'<p class="card-text" style="font-size:60%">{card[key]}</p>'
            cards_html += f"""
            <div class="col">
                <div {s}> 
                    {card_html}
                </div>
            </div>"""
        self.content += f"<div class='row'>{cards_html}</div>"

    def add_title_page(self, title_page_content: dict, styles: list = None):
        """
        Adds a title page to the slide.

        Args:
            title_page_content (dict): A dictionary with 'title', 'subtitle', 'authors', and 'logo' keys.
            styles (list, optional): A list of style dictionaries for the title, subtitle, authors, and logo.
        """
        title = title_page_content.get('title', '')
        subtitle = title_page_content.get('subtitle', '')
        authors = title_page_content.get('authors', '')
        logo = title_page_content.get('logo', '')

        _check_styles(styles, title_page_content)

        if styles is None:
            styles = []

        title_s = _parse_style_class(styles[0]) if styles else ""
        subtitle_s = _parse_style_class(styles[1]) if styles else ""
        authors_s = _parse_style_class(styles[2]) if styles else ""
        logo_s = _parse_style_class(styles[3]) if styles else ""

        title_html = f'<div class="row"><div class="col-12"><h2 {title_s}>{title}</h2></div></div>' if title else ''
        subtitle_html = f'<div class="row"><div class="col-12"><h3 {subtitle_s}>{subtitle}</h3></div></div>' if subtitle else ''
        authors_html = f'<div class="col-9"><h4 {authors_s}>{authors}</h4></div>' if authors else ''
        logo_html = f'<div class="col-3"><img src="{logo}" {logo_s}></div>' if logo else ''
        authors_logo_html = f'<div class="row align-items-center">{authors_html}{logo_html}</div>'


        title_page_html = f'<div class="title-page">{title_html}{subtitle_html}{authors_logo_html}</div>'
        self.content += title_page_html

    def render_slide_html(self):
        """
        Renders the slide as an HTML string.

        Returns:
            str: The HTML representation of the slide.
        """
        css_links = """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.4.0/reveal.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.4.0/theme/moon.min.css">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css">
        """
        js_links = """
        <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.4.0/reveal.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.4.0/plugin/notes/notes.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
        <script src="https://cdn.jsdelivr.net/npm/vega-lite@4.8"></script>
        <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
        <script src="https://cdn.plot.ly/plotly-2.17.1.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        """

        kwargs_str = ' '.join([f'{k}="{v}"' for k, v in self.kwargs.items()])
        slide_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Slide</title>
            {css_links}
            <style>
                .reveal .slides section {{
                    top: 0 !important;
                }}
            </style>
        </head>
        <body>
            <div class="reveal">
                <div class="slides">
                    <section {kwargs_str} class='{'center' if self.center else ''}'>
                        <div class='container' style='text-align: left;' >
                            {self.content}
                        </div>
                    </section>
                </div>
            </div>
            {js_links}
            <script>
                Reveal.initialize({{
                    center: false,
                    controls: true,
                    progress: true,
                    history: true,
                    transition: 'slide',
                    plugins: [RevealNotes]
                }});
            </script>
        </body>
        </html>
        """
        return slide_html

    def save_slide_html(self, file_name):
        """
        Saves the slide as an HTML file.

        Args:
            file_name (str): The name of the file to save the slide as.
        """
        slide_html = self.render_slide_html()
        with open(file_name, "w") as f:
            f.write(slide_html)
