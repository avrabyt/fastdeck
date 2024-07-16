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

# Create a new presentation
presentation = Presentation()

# Create the title slide
title_slide = Slide(center=True)
title_content = Content()
title_content.add_heading("FastDeck Demo", tag="h1")
title_content.add_text("A powerful library for creating slide decks")
title_slide.add_content([title_content.render()])
presentation.add_slide(title_slide)
title_slide.save_slide_html('title_slide.html')  # Save individual slide

# Create a content slide
content_slide = Slide()
content = Content()
content.add_heading("Features of FastDeck")
content.add_list([
    "Easy to use Python API",
    "Support for various content types",
    "Customizable styles",
    "Export to HTML"
])
content_slide.add_content([content.render()])
presentation.add_slide(content_slide)
content_slide.save_slide_html('content_slide.html')  # Save individual slide

# Create a slide with a Plotly graph
plotly_slide = Slide()
plotly_content = Content()
plotly_content.add_heading("Plotly Graph")
df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species', size='petal_length', hover_data=['petal_width'])
fig.update_layout(autosize=True)
json_fig = fig.to_json()
plotly_slide.add_content([json_fig], columns=[12], styles=[{'class': 'stretch'}])
presentation.add_slide(plotly_slide)
plotly_slide.save_slide_html('plotly_slide.html')  # Save individual slide

# Save the entire presentation
presentation.save_html("fastdeck_demo.html")

# Returns the presentation as an HTML string
presentation.to_html() # Paste it directly over any html viewer to render
```

This example creates a presentation with three slides:
1. A title slide
2. A content slide with a list of features
3. A slide with a Plotly graph

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