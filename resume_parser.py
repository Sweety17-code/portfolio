from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import json
import re

def extract_text_from_pdf(pdf_path):
    """Extracts raw text from a PDF file."""
    try:
        laparams = LAParams()
        text = extract_text(pdf_path, laparams=laparams)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def parse_resume_with_llm(text, client):
    """Uses Groq API to parse raw resume text into structured JSON."""
    if not text:
        return None

    prompt = f"""
    You are a resume parser. Extract the following information from the resume text below and return it strictly as valid JSON.
    Do not add any markdown formatting (like ```json ... ```) or extra text. Just the JSON string.

    Target JSON Structure interactable with the dashboard template:
    {{
        "profile": {{
            "name": "Full Name",
            "title": "Professional Title (e.g. Software Engineer)",
            "about": "A short professional summary (2-3 sentences)",
            "email": "Email Address",
            "linkedin": "LinkedIn URL (or # if not found)",
            "github": "GitHub URL (or # if not found)"
        }},
        "skills": ["Skill 1", "Skill 2", ...],
        "projects": [
            {{
                "title": "Project Title",
                "description": "Short description",
                "tags": ["Tag1", "Tag2"],
                "link": "Project URL (or # if not found)"
            }},
            ...
        ],
        "experience": [
            {{
                "role": "Job Title",
                "company": "Company Name",
                "duration": "Duration (e.g. Jan 2023 - Present)",
                "description": "Short description of responsibilities"
            }},
            ...
        ]
    }}

    Resume Text:
    {text}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1, # Low temperature for consistent output
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        response_content = completion.choices[0].message.content
        # validation: ensure it parses
        data = json.loads(response_content)
        return data

    except Exception as e:
        print(f"Error parsing resume with LLM: {e}")
        # Fallback/Empty structure if parsing fails
        return {
            "profile": {"name": "Error Parsing Resume", "title": "", "about": "", "email": "", "linkedin": "#", "github": "#"},
            "skills": [],
            "projects": [],
            "experience": []
        }

def get_resume_data(pdf_path, client):
    """Main function to get structured data from PDF."""
    text = extract_text_from_pdf(pdf_path)
    if text:
        return parse_resume_with_llm(text, client)
    return None

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from groq import Groq

    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("GROQ_API_KEY not found in environment variables.")
    else:
        client = Groq(api_key=api_key)
        # Assuming the resume is in the same directory or adjust path
        resume_path = os.path.join(os.path.dirname(__file__), 'RESUME.2.pdf')
        if os.path.exists(resume_path):
            print("Extracting and parsing resume...")
            data = get_resume_data(resume_path, client)
            print(json.dumps(data, indent=4))
        else:
            print(f"Resume not found at {resume_path}")
