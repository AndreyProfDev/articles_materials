# Introduction

This repostory contains the source code for the article "OpenAI or Open-Source? Choosing the Right Embedding Model for Polish Text" on [Medium](https://medium.com/).

# Google Colab

The main notebook is aviailable on Google Colab (don't forget to select T4 as a runtime):

[OpenAI or Open-Source? Choosing the Right Embedding Model for Polish Text](https://colab.research.google.com/drive/1odBFSu7XftsYlDvLZaXjY4nkaAfAupye#scrollTo=yMdlgBTLZeR-)

# Pre-requisites
WSL2 or any other linux environment

# Installation

Install **uv** dependency manager (for more details see: [Installing uv](https://docs.astral.sh/uv/getting-started/installation/)):
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install python version:

```
uv venv --python ">=3.12,<3.13"
```

Install the required python packages:
```
uv sync
```

# Run tests

```
uv run python -m unittest discover
```

# Run the experiment

Main notebook can be found here:

_src/OpenAI or Open-Source? Choosing the Right Embedding Model for Polish Text.ipynb_

Just run it step by step using _.env_ kernel created earlier.