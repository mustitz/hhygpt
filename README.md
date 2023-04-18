# HhyGpt Vim Plugin

This is a Vim plugin for comfortable work with an OpenAI GPT network.

## Features

- Code completion
- Command line interface

## Installation

1. Download the plugin from the [GitHub repository](https://github.com/mustitz/hhygpt).
2. Extract the plugin into your `~/.vim/` directory.
3. Add the `requests` Python package to the current venv.
4. Set your OpenAI key into an `OPENAI_API_KEY` environment variable.
5. Restart Vim.

## Usage

`GPT status`
Prints current plugin settings.

`GPT complete`
Provides text/code completion from GPT network.
The whole current line is included to GPT prompt.
A mark line with `<<<`s is added at the end of the completion.
