from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv
from resume_parser import get_resume_data

load_dotenv()

app = Flask(__name__)

# Initialize Groq Client
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Load context from resume once at startup
resume_path = os.path.join(os.path.dirname(__file__), 'RESUME.2.pdf')
print("Parsing resume... this may take a moment.")
data = get_resume_data(resume_path, client)

if not data:
    print("Failed to parse resume. Using fallback data.")
    data = {
        "profile": {
            "name": "Candidate Name",
            "title": "Professional Title",
            "about": "Could not extract data from resume.",
            "email": "",
            "linkedin": "#",
            "github": "#"
        },
        "skills": ["Error extracting skills"],
        "projects": [],
        "experience": []
    }

# For chat context, we need the raw text or the structured data stringified
# Let's re-extract text or just use JSON. JSON is better for the bot to understand structure.
resume_context = str(data)

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
                               f"Here is the resume data in JSON format:\n\n{resume_context}"
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
