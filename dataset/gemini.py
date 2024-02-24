import pathlib
import textwrap
import sys

import google.generativeai as genai

from IPython.display import display, display_markdown
from IPython.display import Markdown

import os


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Used to securely store your API key
# from google.colab import userdata

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.

GOOGLE_API_KEY='AIzaSyDq8bZpcx_RYHonUvCU5b_rMkEYY2xn_U8'
# print(GOOGLE_API_KEY)

def query_llm(prompt):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    # display(response.text)
    return str(response.text)

# genai.configure(api_key=GOOGLE_API_KEY)

# model = genai.GenerativeModel('gemini-pro')

# %%time

# print(sys.argv[1])
# file_name = sys.argv[1]

# prompt = open(file_name, 'r').read()
# # print(prompt)
# # prompt = "Who is Taylor Swift?"

# # # print(prompt)

# response = model.generate_content(prompt)

# display(response.text)

# %%
