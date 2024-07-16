from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fastdeck",
    version="0.1.0",
    author="Avratanu Biswas",
    author_email="avrab.yt@gmail.com",
    description="A library for creating and managing slide decks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fastdeck",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',
        'requests',
        'matplotlib',
    ],
    extras_require={
        'full': ['plotly', 'pandas', 'vega', 'vega_datasets', 'altair'],
    },
)