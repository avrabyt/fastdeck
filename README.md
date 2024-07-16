# Fastdeck

<table>
  <tr>
    <td>
      <a href="https://pypi.org/project/fastdeck/" target="_blank">
        <img src="https://img.shields.io/pypi/v/fastdeck.svg" alt="PyPI">
      </a>
    </td>
    <td>
      <a href="https://avrabyt.github.io/fastdeck/fastdeck.html#fastdeck" target="_blank">
        <img src="https://img.shields.io/badge/docs-latest-brightgreen.svg" alt="Documentation">
      </a>
    </td>
  </tr>
</table>


Fastdeck is a Python library for creating and managing slide decks.

**Fastdeck Python library is maintained to support the app ⚡️[Fastdeck AI](https://fastdeckai.com).**

**Create and share minimal slides in seconds, on the go.**

## Installation

You can install `fastdeck` using pip:

```bash
pip install fastdeck==0.1.0
```

## Usage

Here's a basic overview of how to use Fastdeck:

1. Import the necessary classes:

```python
from fastdeck import Presentation, Slide, Content
```

2. Create a presentation:

```python
presentation = Presentation()
```

3. Create slides and add content:

```python
slide = Slide()
content = Content()

content.add_heading("Welcome to FastDeck")
content.add_text("This is a simple demonstration of FastDeck capabilities.")

slide.add_content([content.render()])
```

4. Add the slide to the presentation:

```python
presentation.add_slide(slide)
```

5. Generate and save the HTML:

```python
presentation.save_html("my_presentation.html")
```

## Example

```python
from fastdeck import Presentation, Slide, Content
import plotly.express as px
import os

# Create output directory
output_dir = 'fastdeck_demo_output'
os.makedirs(output_dir, exist_ok=True)

# Create a new presentation
presentation = Presentation()

# Define a common style for centering
center_style = {'style': 'display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; text-align: center;'}

# Create the title slide
title_slide = Slide(center=True)
title_content = Content()
title_content.add_heading("Fastdeck", tag="h1")
title_content.add_text("Create and manage slide decks in pure Python.")
title_slide.add_content([title_content.render()], styles=[center_style])
presentation.add_slide(title_slide)
# Save indiviual slides
# title_slide.save_slide_html(os.path.join(output_dir, 'title_slide.html'))

# Create a content slide
content_slide = Slide()
content = Content()
content.add_heading("Features of Fastdeck")
content.add_list([
    "Easy to use Python API",
    "Support for various content types",
    "Customizable styles",
    "Export to HTML"
])
content_slide.add_content([content.render()], styles=[center_style])
presentation.add_slide(content_slide)


# Create a slide advertising Fastdeck AI App
ai_app_slide = Slide()
ai_app_content = Content()
ai_app_content.add_heading("Try Fastdeck AI App", tag="h2")
ai_app_content.add_text("Create and share minimal slides in seconds, on the go")
ai_app_content.add_text("Powered by AI")
ai_app_content.add_text('<a href="https://fastdeckai.com" target="_blank">Try ⚡️ Fastdeck AI</a>')
ai_app_slide.add_content([ai_app_content.render()], styles=[center_style])
presentation.add_slide(ai_app_slide)


# Create a slide about what more you can do with Fastdeck
more_features_slide = Slide()
more_features_content = Content()
more_features_content.add_heading("What more you can do with Fastdeck", tag="h2")
more_features_content.add_list([
    "Create interactive charts and graphs",
    "Embed videos and images",
    "Customize themes and layouts",
    "Generate presentations programmatically",
    "Integrate with data analysis workflows",
    "and more ..."
])
more_features_slide.add_content([more_features_content.render()], styles=[center_style])
presentation.add_slide(more_features_slide)


# Create a slide with a Plotly graph
plotly_slide = Slide()
plotly_content = Content()
plotly_content.add_heading("Plotly Graph")
df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species', size='petal_length', hover_data=['petal_width'])

# Make the plot transparent
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot area
    autosize=True
)

json_fig = fig.to_json()
plotly_slide.add_content([json_fig], columns=[12], styles=[{'class': 'stretch'}])
presentation.add_slide(plotly_slide)
plotly_slide.save_slide_html('plotly_slide.html')  # Save individual slide


# Create a slide with an embedded video
video_slide = Slide()
video_content = Content()
video_content.add_heading("Embedded Video Support", tag="h2")
video_embed = '<iframe width="560" height="315" src="https://www.youtube.com/embed/d2JPEDpMiw8" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen style="max-width: 80%; max-height: 60vh;"></iframe>'
video_content.add_div(video_embed)
video_slide.add_content([video_content.render()], styles=[center_style])
presentation.add_slide(video_slide)


# Create a slide with a cat image
image_slide = Slide()
image_content = Content()
image_content.add_heading("Image Integration", tag="h2")
image_url = "https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D"
image_content.add_image(image_url, alt="Cute cat", **{'style': 'max-width: 80%; max-height: 60vh; object-fit: contain;'})
image_slide.add_content([image_content.render()], styles=[center_style])
presentation.add_slide(image_slide)


# Save the entire presentation
presentation.save_html(
    os.path.join(output_dir, "fastdeck_demo.html"),
    theme="night",  # 'black', 'white', 'league', 'beige', 'sky', 'night', 'serif', 'simple', 'solarized', 'blood', 'moon'
    width=1920,     # 16:9 width 
    height=1080,    # 16:9 height 
    margin=0.07,    # 7% margin
    minscale=0.3,   # Can shrink to 30% of original size
    maxscale=2.0    # Can grow to 200% of original size
)

print(f"Presentation and individual slides have been saved in the directory: {output_dir}")

# Returns the presentation as an HTML string
html_string = presentation.to_html(
    theme="blood",
    width=1920,
    height=1080,
    margin=0.07,
    minscale=0.3,
    maxscale=2.0
)

print("HTML string generated. You can paste it directly into any HTML viewer to render.")
```
After running this script, you'll have an HTML file named `fastdeck_demo.html` that you can open in a web browser to view your presentation.

## Documentation

For more detailed information about Fastdeck's classes and methods, please refer to the [documentation](https://avrabyt.github.io/fastdeck/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements
- [Reveal.js](https://revealjs.com)
- This python package is inspired by the [respysive-slide wrapper](https://github.com/fbxyz/respysive-slide/tree/master).
