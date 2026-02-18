from flask import Flask, render_template, request, jsonify
from groq import Groq
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize Groq Client
# WARNING: It is best practice to use environment variables for API keys.
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Load context from resume
def get_resume_context():
    try:
        resume_path = r'c:\Users\Dell\OneDrive\suuu\RESUME.2.pdf'
        if os.path.exists(resume_path):
            laparams = LAParams()
            text = extract_text(resume_path, laparams=laparams)
            return text
        return "No resume found."
    except Exception as e:
        print(f"Error reading resume: {e}")
        return "Error reading resume."

resume_context = get_resume_context()

# Mock Data (based on extraction + placeholders)
data = {
    "profile": {
        "name": "Suuu",  # Inferred from folder name, can be updated
        "title": "Software Developer",
        "about": "Aspiring software developer with a strong foundation in C++, Python, and Web Technologies. Passionate about building clean, efficient, and user-friendly applications.",
        "email": "contact@example.com",
        "linkedin": "linkedin.com/in/example",
        "github": "github.com/example"
    },
    "skills": ["C++", "Python", "HTML", "CSS", "C"],
    "projects": [
        {
            "title": "Project Alpha",
            "description": "A high-performance application optimizing data processing algorithms.",
            "tags": ["C++", "Optimization"],
            "link": "#"
        },
        {
            "title": "Web Dashboard",
            "description": "Minimalist portfolio dashboard using Flask and modern CSS.",
            "tags": ["Python", "Flask", "HTML/CSS"],
            "link": "#"
        },
        {
            "title": "Automation Script",
            "description": "Python script to automate daily file management tasks.",
            "tags": ["Python", "Automation"],
            "link": "#"
        }
    ],
    "experience": [
        {
            "role": "Intern",
            "company": "Tech Corp",
            "duration": "2023 - Present",
            "description": "Assisted in developing component libraries and fixing bugs in the core product."
        }
    ]
}

@app.route('/')
def dashboard():
    return render_template('dashboard.html', data=data)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful AI assistant for a portfolio website. "
                               f"Your goal is to answer questions about the candidate based on their resume. "
                               f"Be concise, professional, and friendly. "
                               f"Here is the resume content:\n\n{resume_context}"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.7,
            max_tokens=200,
            top_p=1,
            stop=None,
            stream=False
        )
        response = completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        print(f"Groq API Error: {e}")
        return jsonify({"error": "Failed to process request"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
