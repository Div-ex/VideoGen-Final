import ollama
import requests
import re
import logging



def generate_script(prompt):
    try:
        result = ollama.chat(model='llama3.2:3b', messages=[
            {
                'role': 'system',
                'content': """Give me eight lines on this topic. They should not be numbered""",
            },
            {
                'role': 'user',
                'content': prompt,
            },
        ])
#        
        print(result['message']['content'])
        return result['message']['content']
    except Exception as e:
        return f"Exception occurred: {str(e)}"


# def get_ollama_images(prompt, keywords):
#     try:
#         result = ollama.chat(model='llama3.2:3b', messages=[
#             {
#                 'role': 'system',
#                 'content': f'Give me a single keyword for this input except for{keywords}',
#             },
#             {
#                 'role': 'user',
#                 'content': prompt,
#             },
#         ])
#         print(result['message']['content'])
#         return result['message']['content']
#     except Exception as e:
#         return f"Exception occurred: {str(e)}"
    
# def parse_script(output):
#     """
#     Parse the script output to extract keywords and a list of (duration, text).
#     """
#     if not output:
#         return [], []

#     keywords = []
#     script = []

#     keyword_match = re.search(r'KEYWORDS:\s*([^\n]+)', output, re.IGNORECASE)
#     if keyword_match:
#         keywords = [k.strip() for k in keyword_match.group(1).split(',') if k.strip()]

#     script_lines = re.findall(r'-?\s*(\d+\.\d+):?\s*([^\n]+)', output)
#     for duration, text in script_lines:
#         try:
#             duration = float(duration)
#             # if 1 <= duration <= 20:
#             script.append((duration, text.strip()))
#         except ValueError:
#             continue

#     return keywords, script

# import re

def parse_script(output):
    """
    Parse plain paragraph text and extract a list of script lines (text only).
    Each sentence is considered one script line.
    """
    if not output:
        return [], []

    keywords = []  # Placeholder for future keyword extraction if needed

    # Use regular expression to split on sentence boundaries (., ?, !)
    sentences = re.split(r'(?<=[.!?])\s+', output.strip())
    script = [sentence.strip() for sentence in sentences if sentence.strip()]
    print(script)
    return script


# parse_script(generate_script("World war 2"))