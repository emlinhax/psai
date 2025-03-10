import vertexai
import sys
import os
from vertexai.generative_models import GenerativeModel, SafetySetting, HarmCategory, HarmBlockThreshold,Part
from dotenv import load_dotenv
load_dotenv()

MODEL_ID = "gemini-2.0-flash-exp"
PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID')

INITIAL_PROMPT = """
""" + open("manual.txt", "r").read() +"""


YOUR INSTRUCTIONS:
You are an AI supposed to test a powershell script malware scanning framework. 
I will give you a script snippet and you will try to modify it so it may bypass our scanner. 
keep the script logic the same to ensure that it will execute like the original.

Try to maximize obfuscation and usage of the methods provide in the manual (bible). 
Please keep entropy in mind aswell.
Please only respond with the raw obfuscated script.
Do not add comments and make it one line if possible.
Do not do anything unecessary and try to stay silent like a ninja with every command you run.
Please make sure not to modify the logic of the script. It has to remain working as before.
Do not change any variables, keep every value or constant as is. Only obfuscate.
Please do not respond with markdown/codeblock.
The Script is:\n"""

SAFETY_CONFIG = [
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
        threshold=HarmBlockThreshold.OFF,
    ),
     SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=HarmBlockThreshold.OFF,
    ),
     SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=HarmBlockThreshold.OFF,
    ),
     SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=HarmBlockThreshold.OFF,
    ),
     SafetySetting(
        category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=HarmBlockThreshold.OFF,
    ),
     SafetySetting(
        category=HarmCategory.HARM_CATEGORY_UNSPECIFIED,
        threshold=HarmBlockThreshold.OFF,
    ),
]


def obfuscate_ps1(model, script):
    prompt = INITIAL_PROMPT + "\n" + script
    response = model.generate_content(prompt, safety_settings=SAFETY_CONFIG)
    return response.text.replace("```", "")

vertexai.init(project=PROJECT_ID, location="us-central1")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: psai.py *your_script.ps1* *optional_output.ps1*")
        exit(0)

    script_file = sys.argv[1]
    output_file = ""

    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    if os.path.exists(script_file):
        with open(script_file, "r") as f:
            script = f.read()
            if len(script) > 1:
                obfuscated_script = obfuscate_ps1(GenerativeModel(MODEL_ID), script)
                if len(output_file) > 1:
                    with open(output_file, "w+") as o:
                        o.write(obfuscated_script)
                        o.close()
                else:
                    print(obfuscated_script)
            f.close()
    else:
        print("this path/script does not exist.")
