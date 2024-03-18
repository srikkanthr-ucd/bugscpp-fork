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

# # # print(prompt)

# response = model.generate_content(prompt)

# display(response.text)
prompt = '''
You are an Automatic Program Repair Tool. The following C++ code snippet is taken from an open source GitHub Project and contains an error.
The function as written has an error and I require your assistance in fixing it. 
In the code the variables defined and their meaning are as follows.

`RA()` - this is a function that returns a pointer. 
`RKB()` - this is a function that returns a pointer.
The datatypes of `RA()` and `RKB()` are customly defined and their exact outline is not important.
`*RA()->v.i` returns the value stored by `RA()` and is a 32 bit unsigned integer.

The purpose of the code is to store the value of `~*RKB()` in `RA()`.

```cpp
opcase(FLIP): {
             bvalue *dst = RA(), *a = RKB();
             if (var_isint(a)) {
                var_setint(dst, -a->v.i);
             } else if (var_isinstance(a)) {
                ins_unop(vm, "~", *RKB());
                reg = vm->reg;
```

When the above code is run on an input where the value of `RKB()` is 3, 
the output is 4294967293, but the intended output is 4294967292.

Format your response as follows.
```json
{{
  "error": [
    {{
      "line_number": 
      "error_type": 
      "explanation": <Do not include backslash and double quote characters here>
    }}
  ],
  "confidence":
}}
```

For example, for the following function,
```
int fibonacci(int n) {
  if (n <= 1) {
    return fibonacci(n-1) - fibonacci(n-2);
  }
}
```
A sample output is as follows:

```json
{{
  "error": [
    {{
      "line_number": 3 
      "error_type": logical-error
      "explanation": The recursion formula is wrong
    }}
  ],
  "confidence": 1.0
}}
```
The corrected code is as follows,

```
int fibonacci(int n) {
  if (n <= 1) {
    return fibonacci(n-1) + fibonacci(n-2);
  }
}
```
'''

# class geminiWrapper:
  # def setup():

model = genai.GenerativeModel('gemini-pro')
def configure():
  genai.configure(api_key=GOOGLE_API_KEY)
  model = genai.GenerativeModel('gemini-pro')

def start_chat(): 
  chat = model.start_chat(history=[])
  chat
  return chat

def query_llm(gchat, prompt):
  res = []
  response = gchat.send_message(prompt)
  for chunk in response:
    res.append(chunk.text)
  return "".join(res)


messages = []
def start_chat2(_message):
  _message = []

HISTORY_MESSAGE = ''' Here is a history of previous interactions. Take them into account to provide a response for the last prompt.
The interactions are formated as follows:

[User Prompt]: <A string describing user prompt>
<Response Ends>

[Your Response]: <A string describing your response>
<Response Ends>

For example a sample interaction is given below:

[User Prompt]:
The following C++ function has an error. Please provide a fix.
```cpp
int fib(int n) {
    return fib(n) - fib(n-1);
}
```
<Prompt Ends>

[Your Response]:  
The provided C++ function fib(int n) has two main errors:

    Incorrect Logic: It attempts to calculate the Fibonacci sequence using subtraction, which is not the correct formula. The Fibonacci sequence is defined as F(n) = F(n-1) + F(n-2), where each number is the sum of the two preceding ones.

    Infinite Recursion: The function calls itself recursively without any base cases to stop the recursion. This causes it to loop infinitely until the program crashes.

Here's a corrected version of the function:
C++
```cpp
int fib(int n) {
    if (n <= 1) {  // Base cases: 0th and 1st Fibonacci numbers are 0 and 1
        return n;
    } else {
        return fib(n-1) + fib(n-2);  // Recursive call with the correct formula
    }
}
```
Use code with caution.

This version implements the correct recursive formula for the Fibonacci sequence and includes base cases to terminate the recursion, ensuring a valid calculation.
<Response Ends>

[User Prompt]: 
Please provide only the code (without explanation)
<Prompt Ends>

[Your Response]:
C++
```cpp
int fib(int n) {
    if (n <= 1) {
        return n;
    } else {
        return fib(n-1) + fib(n-2);
    }
}
```
<Response Ends>

'''

def query_llm2(messages, prompt):
  while len(messages) > 3:
    messages.pop()
  messages.append(prompt)
  gen_prompt = messages[0] + "\n"
  if len(messages) > 1:
    gen_prompt += HISTORY_MESSAGE

  for p in range(1, len(messages)-2):
    if p%2 == 1:
      gen_prompt += "\n [Your Response]:\n" + messages[p] + "\n <Response Ends>\n"
    else:
      gen_prompt += "\n [User Prompt]:\n" + messages[p] + "\n <Prompt Ends>\n"
  response = model.generate_content(gen_prompt)
  messages.append(response.text)
  return response.text

def queryPlain(prompt):
  response = model.generate_content(prompt)
  return response.text

# response = chat.send_message(prompt)
# # go = query_llm(prompt)
# print(response)
# print(chat.history)
# prompt = 'The previous solution was incorrect, can you provide another one?'
# response = chat.send_message(prompt)
# # go = query_llm(prompt)
# print(response)
# print(chat.history)
# %%
  
# configure()
# gchat = start_chat()
# go = chat_llm(gchat, prompt)
# print(go)
# go = chat_llm(gchat, 'The previous solution was incorrect, can you provide another one?')
# print(go)
