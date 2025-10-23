import openai
from django.conf import settings
from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader

openai.api_key = settings.OPENAI_API_KEY  # store in settings not hardcoded

def extract_text_from_resume(resume_file):
    """Extract text from PDF, DOCX, or TXT resume."""
    filename = resume_file.name.lower()

    if filename.endswith('.txt'):
        return resume_file.read().decode('utf-8')

    elif filename.endswith('.pdf'):
        reader = PdfReader(BytesIO(resume_file.read()))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif filename.endswith('.docx'):
        doc = Document(BytesIO(resume_file.read()))
        text = "\n".join([p.text for p in doc.paragraphs])
        return text

    else:
        raise ValueError("Unsupported file format. Please upload PDF, DOCX, or TXT.")


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
