import unittest
from fastdeck import Content, Slide, Presentation
from matplotlib import pyplot as plt
import tempfile
import os
from unittest.mock import patch, mock_open
from bs4 import BeautifulSoup

class TestContent(unittest.TestCase):
    def setUp(self):
        self.content = Content()

    def test_add_heading(self):
        self.content.add_heading("Test Heading", "h2", icon="fa-test")
        rendered = self.content.render()
        self.assertIn("<h2", rendered)
        self.assertIn("Test Heading", rendered)
        self.assertIn("fa-test", rendered)

    def test_add_text(self):
        self.content.add_text("Test paragraph", "p", class_="test-class")
        rendered = self.content.render()
        self.assertIn("<p", rendered)
        self.assertIn("Test paragraph", rendered)
        self.assertIn("test-class", rendered)

    def test_add_list(self):
        self.content.add_list(["Item 1", "Item 2"], ordered=True)
        rendered = self.content.render()
        self.assertIn("<ol", rendered)
        self.assertIn("Item 1", rendered)
        self.assertIn("Item 2", rendered)

    @patch('fastdeck.content.open', new_callable=mock_open, read_data=b'fake image data')
    def test_add_image(self, mock_file):
        self.content.add_image("test.jpg", "Test Image")
        rendered = self.content.render()
        self.assertIn("<img", rendered)
        self.assertIn("data:image/png;base64,", rendered)
        self.assertIn("Test Image", rendered)

    def test_add_svg(self):
        svg_content = "<svg><circle cx='50' cy='50' r='40'/></svg>"
        self.content.add_svg(svg_content)
        rendered = self.content.render()
        soup = BeautifulSoup(rendered, 'html.parser')
        svg = soup.find('svg')
        self.assertIsNotNone(svg)
        self.assertEqual(svg.circle['cx'], '50')
        self.assertEqual(svg.circle['cy'], '50')
        self.assertEqual(svg.circle['r'], '40')

    def test_add_plotly(self):
        plotly_json = '{"data": [{"y": [1, 2, 3]}]}'
        self.content.add_plotly(plotly_json)
        rendered = self.content.render()
        self.assertIn("Plotly.newPlot", rendered)
        self.assertIn(plotly_json, rendered)

    def test_add_altair(self):
        altair_json = '{"$schema": "https://vega.github.io/schema/vega-lite/v4.json"}'
        self.content.add_altair(altair_json)
        rendered = self.content.render()
        self.assertIn("vegaEmbed", rendered)
        self.assertIn(altair_json, rendered)

    def test_add_fig(self):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4])
        self.content.add_fig(fig)
        rendered = self.content.render()
        self.assertIn("<svg", rendered)

class TestSlide(unittest.TestCase):
    def setUp(self):
        self.slide = Slide()

    def test_add_title(self):
        self.slide.add_title("Test Title", "h2", icon="fa-test")
        self.assertIn("Test Title", self.slide.content)
        self.assertIn("<h2", self.slide.content)
        self.assertIn("fa-test", self.slide.content)

    def test_add_content(self):
        self.slide.add_content(["Content 1", "Content 2"], columns=[6, 6])
        self.assertIn("Content 1", self.slide.content)
        self.assertIn("Content 2", self.slide.content)
        self.assertIn("col-md-6", self.slide.content)

    def test_add_card(self):
        cards = [{"title": "Card 1", "text": "Text 1"}, {"title": "Card 2", "text": "Text 2"}]
        self.slide.add_card(cards)
        self.assertIn("Card 1", self.slide.content)
        self.assertIn("Card 2", self.slide.content)
        self.assertIn("card", self.slide.content.lower())

    def test_add_title_page(self):
        title_page_content = {
            "title": "Main Title",
            "subtitle": "Subtitle",
            "authors": "John Doe",
            "logo": "logo.png"
        }
        self.slide.add_title_page(title_page_content)
        self.assertIn("Main Title", self.slide.content)
        self.assertIn("Subtitle", self.slide.content)
        self.assertIn("John Doe", self.slide.content)
        self.assertIn("logo.png", self.slide.content)

    def test_render_slide_html(self):
        self.slide.add_title("Test Slide")
        rendered = self.slide.render_slide_html()
        self.assertIn("<html", rendered)
        self.assertIn("Test Slide", rendered)
        self.assertIn("reveal.js", rendered)

class TestPresentation(unittest.TestCase):
    def setUp(self):
        self.presentation = Presentation()

    def test_add_slide(self):
        slide1 = Slide()
        slide1.add_title("Slide 1")
        slide2 = Slide()
        slide2.add_title("Slide 2")
        self.presentation.add_slide([slide1, slide2])
        self.assertEqual(len(self.presentation.slides), 2)

    def test_to_html(self):
        slide = Slide()
        slide.add_title("Test Slide")
        self.presentation.add_slide(slide)
        html = self.presentation.to_html()
        self.assertIn("<html", html)
        self.assertIn("Test Slide", html)
        self.assertIn("reveal.js", html)

    def test_save_html(self):
        slide = Slide()
        slide.add_title("Test Slide")
        self.presentation.add_slide(slide)
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_filename = temp_file.name
            self.presentation.save_html(temp_filename)
            temp_file.seek(0)
            html = temp_file.read()
        os.unlink(temp_filename)
        self.assertIn("<html", html)
        self.assertIn("Test Slide", html)
        self.assertIn("reveal.js", html)

if __name__ == '__main__':
    unittest.main()