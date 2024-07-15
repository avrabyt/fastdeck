"""
Presentation Module

This module provides tools for creating and managing full presentations.

Classes:
    Presentation: A class representing a complete presentation, consisting of multiple slides.
"""

from .slide import Slide, create_slide_html
from bs4 import BeautifulSoup

class Presentation:
    """
    A class representing a presentation.

    Attributes:
        slides (list): A list of slides in the presentation.
    """

    def __init__(self):
        """Initializes a new Presentation object."""
        self.slides = []

    def add_slide(self, slide):
        """
        Adds a slide or list of slides to the presentation.

        Args:
            slide (Slide or list): The slide or list of slides to add to the presentation.
        """
        if isinstance(slide, list):
            for sl in slide:
                self.slides.append(sl)
        else:
            self.slides.append(slide)

    def to_html(self, theme="moon", width=960, height=600, minscale=0.2, maxscale=1.5, margin=0.1, custom_theme=None):
        """
        Returns the presentation as an HTML string.

        Args:
            theme (str): The name of the reveal.js theme to use (default is 'moon').
            width (int): The width of the presentation (default is 960).
            height (int): The height of the presentation (default is 600).
            minscale (float): The minimum scale of the presentation (default is 0.2).
            maxscale (float): The maximum scale of the presentation (default is 1.5).
            margin (float): The margin of the presentation (default is 0.1).
            custom_theme (str, optional): A link to a custom theme CSS file if theme is set to 'custom'.

        Returns:
            str: The presentation in HTML format.

        Raises:
            ValueError: If the theme is set to 'custom' but no custom_theme link is provided.
        """
        if theme == "custom" and custom_theme is None:
            raise ValueError("If the theme is set to 'custom', a URL for the custom theme must be provided.")

        if custom_theme:
            theme_link = custom_theme
        else:
            theme_link = f"https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.4.0/theme/{theme}.min.css"

        css_links = [
            "https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.4.0/reveal.min.css",
            theme_link,
            "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css",
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css"
        ]
        js_links = [
            "https://cdn.jsdelivr.net/npm/vega@5",
            "https://cdn.jsdelivr.net/npm/vega-lite@4.8",
            "https://cdn.jsdelivr.net/npm/vega-embed@6",
            "https://cdn.plot.ly/plotly-2.17.1.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js",
            "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        ]

        css_links = "\n".join([f"<link type='text/css' href='{link}' rel='stylesheet'>" for link in css_links])
        js_links = "\n".join([f"<script src='{link}' type='text/javascript'></script>" for link in js_links])

        slides_html = "\n".join([create_slide_html(slide) for slide in self.slides])

        presentation_html = f"""
        <html>
         <head>
          <meta charset="UTF-8">
          {css_links}
          <style type='text/css'>svg{{max-width: 100%;}}</style>
          {js_links}
         </head>
         <body>
            <div class='reveal'>
                <div class='slides'>
                    {slides_html}
                </div>
            </div>
            <!--Correction to allow transition between slides-->
            <style type='text/css'>[hidden] {{display: inherit !important;}}</style>
            
            <script>
            // from nbconvert
            require(
            {{
              // it makes sense to wait a little bit when you are loading
              // reveal from a cdn in a slow connection environment
              waitSeconds: 15
            }},
            [
              "https://unpkg.com/reveal.js@4.4.0/dist/reveal.js",
              "https://unpkg.com/reveal.js@4.4.0/plugin/notes/notes.js"
            ],
        
            function(Reveal, RevealNotes){{
                Reveal.initialize({{
                    center: false,
                    pdfMaxPagesPerSlide: 1,
                    pdfSeparateFragments: false,
                    display:'block',
                    slideNumber: 'c/t',  
                    controls: true,
                    
                    progress: true,
                    history: true,
                    transition: "slide",
        
                    plugins: [RevealNotes],
                    width: {width},
                    height: {height},
                    center: true,
                    margin: {margin},
                        
                    minScale: {minscale},
                    maxScale: {maxscale},
            }});
              
                var update = function(event){{
                  if(MathJax.Hub.getAllJax(Reveal.getCurrentSlide())){{
                    MathJax.Hub.Rerender(Reveal.getCurrentSlide());
                  }}
                }};
        
                Reveal.addEventListener('slidechanged', update);
        
                function setScrollingSlide() {{
                    var scroll = false
                    if (scroll === true) {{
                      var h = $('.reveal').height() * 0.95;
                      $('section.present').find('section')
                        .filter(function() {{
                          return $(this).height() > h;
                        }})
                        .css('height', 'calc(95vh)')
                        .css('overflow-y', 'scroll')
                        .css('margin-top', '20px');
                    }}
                }}
        
                // check and set the scrolling slide every time the slide change
                Reveal.addEventListener('slidechanged', setScrollingSlide);
            }}
            );
            </script>
             </body>
        </html>
        """
        soup = BeautifulSoup(presentation_html, "html.parser")
        return presentation_html

    def save_html(self, file_name, theme="moon", width=960, height=600, minscale=0.2, maxscale=1.5, margin=0.1,
                  custom_theme=None):
        """
        Saves the presentation as an HTML file.

        Args:
            file_name (str): The name of the file to save the presentation as.
            theme (str, optional): The name of the reveal.js theme to use (default is 'moon').
            width (int, optional): The width of the presentation (default is 960).
            height (int, optional): The height of the presentation (default is 600).
            minscale (float, optional): The minimum scale of the presentation (default is 0.2).
            maxscale (float, optional): The maximum scale of the presentation (default is 1.5).
            margin (float, optional): The margin of the presentation (default is 0.1).
            custom_theme (str, optional): A link to a custom theme CSS file if theme is set to 'custom'.

        Raises:
            ValueError: If the theme is set to 'custom' but no custom_theme link is provided.
        """
        if theme == "custom" and custom_theme is None:
            raise ValueError("If the theme is set to 'custom', a URL for the custom theme must be provided.")

        if custom_theme:
            theme_link = custom_theme
        else:
            theme_link = theme

        presentation_html = self.to_html(theme=theme_link, width=width, height=height, minscale=minscale,
                                         maxscale=maxscale, margin=margin, custom_theme=custom_theme)

        with open(file_name, "w") as f:
            f.write(presentation_html)

    # def save_slide_html(self, slide, file_name, theme="moon"):
    #     """
    #     Saves a single slide as an HTML file.

    #     Args:
    #         slide (Slide): The slide to save.
    #         file_name (str): The name of the file to save the slide as.
    #         theme (str, optional): The name of the reveal.js theme to use (default is 'moon').
    #     """
    #     css_links = [
    #         "https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.4.0/reveal.min.css",
    #         f"https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.4.0/theme/{theme}.min.css",
    #         "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css",
    #         "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css"
    #     ]
    #     js_links = [
    #         "https://cdn.jsdelivr.net/npm/vega@5",
    #         "https://cdn.jsdelivr.net/npm/vega-lite@4.8",
    #         "https://cdn.jsdelivr.net/npm/vega-embed@6",
    #         "https://cdn.plot.ly/plotly-2.17.1.min.js",
    #         "https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js",
    #         "https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js",
    #         "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
    #     ]

    #     css_links = "\n".join([f"<link type='text/css' href='{link}' rel='stylesheet'>" for link in css_links])
    #     js_links = "\n".join([f"<script src='{link}' type='text/javascript'></script>" for link in js_links])

    #     slide_html = f"""
    #     <html>
    #     <head>
    #     <meta charset="UTF-8">
    #     {css_links}
    #     </head>
    #     <body>
    #     <div class='reveal'>
    #         <div class='slides'>
    #             {create_slide_html(slide)}
    #         </div>
    #     </div>
    #     {js_links}
    #     <script>
    #     document.addEventListener('DOMContentLoaded', function() {{
    #         Reveal.initialize({{
    #             center: false,
    #             controls: true,
    #             progress: true,
    #             history: true,
    #             transition: 'slide',
    #             plugins: [RevealNotes]
    #         }});
    #     }});
    #     </script>
    #     </body>
    #     </html>
    #     """
    #     with open(file_name, "w") as f:
    #         f.write(slide_html)
