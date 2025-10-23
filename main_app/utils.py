import openai
from django.conf import settings
from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader

openai.api_key = settings.OPENAI_API_KEY  # store in settings not hardcoded

import requests
from PyPDF2 import PdfReader
from io import BytesIO

def extract_text_from_resume(file_url):
    """
    Extracts text from a resume (supports Supabase Storage public URLs or local file paths).
    """
    try:
        if file_url.startswith("http"):
            # ✅ Download file directly from Supabase
            response = requests.get(file_url)
            response.raise_for_status()
            file_stream = BytesIO(response.content)
        else:
            # Local development fallback
            file_stream = open(file_url, "rb")

        # ✅ Handle PDF (you can extend this for DOCX/TXT later)
        reader = PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        file_stream.close()
        return text.strip()

    except Exception as e:
        print("Error extracting resume text:", e)
        return ""



# def generate_teleprompter_text(job_title, job_description, resume_text):
#     """Generate a full 2–3 minute teleprompter script based on resume, job title, and description."""
#     try:
#         messages = [
#             {
#                 "role": "system",
#                 "content": "You are an expert career coach and script writer. "
#                            "Generate a professional, natural, conversational self-introduction teleprompter script."
#             },
#             {
#                 "role": "user",
#                 "content": f"""
# Job Title: {job_title}
# Job Description: {job_description}
# Resume:
# {resume_text}

# Using the above information, write a 2–3 minute teleprompter script for a video introduction.
# The script should:
# - Sound like the candidate is speaking naturally
# - Highlight key experiences, skills, and achievements from the resume
# - Align the strengths to the job description
# - Maintain a friendly but professional tone
# - Include a short closing line
#                 """
#             }
#         ]

#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=messages,
#             max_tokens=900,  # 👈 enough for 2–3 minutes of text
#             temperature=0.7
#         )

#         return response['choices'][0]['message']['content'].strip()

#     except Exception as e:
#         return f"Error generating teleprompter text: {e}"

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Fetch API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def generate_teleprompter_text(job_title, job_description, resume_text):
    """Generate a full 2–3 minute teleprompter script based on resume, job title, and description."""
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert career coach and script writer. "
                    "Generate a professional, natural, conversational self-introduction teleprompter script."
                ),
            },
            {
                "role": "user",
                "content": f"""
Job Title: {job_title}
Job Description: {job_description}
Resume:
{resume_text}

Using the above information, write a 2–3 minute teleprompter script for a video introduction.
The script should:
- Sound like the candidate is speaking naturally
- Highlight key experiences, skills, and achievements from the resume
- Align the strengths to the job description
- Maintain a friendly but professional tone
- Include a short closing line
                """,
            },
        ]

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=900,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating teleprompter text: {e}"
