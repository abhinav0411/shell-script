import google.generativeai as genai
import os
import subprocess
from dotenv import load_dotenv
import sys

load_dotenv()

google_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=google_api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def send_to_gemini(question):
    prompt = """
        You are an error analysis assistant.

        Explain the following error in this format:

        What went wrong:
        2-3 line explanation

        How to fix this:
        <clear steps to resolve the issue>

        Keep the answer short and beginner-friendly.
        Error:
    """

    final_prompt = prompt + "\n" + question

    response = model.generate_content(final_prompt)

    if not hasattr(response, "text") or not response.text:
        print("No text output received from Gemini. Response details:")
        print(response)
        return "(No response text from Gemini)"

    return response.text

def check_last_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=3
    )
    return result.stderr

if len(sys.argv) > 1:
    command = sys.argv[1]

# 2. Otherwise, ask the user
else:
    print("Enter the command that produced the error:")
    command = input().strip()

error = check_last_command(command)

answer = send_to_gemini(error)

print(answer)