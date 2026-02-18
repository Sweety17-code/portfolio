# Portfolio Dashboard

A minimalist portfolio dashboard using Flask, HTML/CSS, and Groq API for AI chat capabilities. The content is dynamically extracted from a PDF resume.

## Features
- **Dynamic Content**: Extracts information from `RESUME.2.pdf`.
- **AI Chat**: Chat with an AI assistant that knows about the candidate's resume (powered by Groq).
- **Responsive Design**: Modern, minimalist UI.

## Local Setup

1.  **Clone the repository** (if applicable) or download the source code.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up environment variables**:
    - Create a `.env` file in the root directory.
    - Add your Groq API key:
      ```
      GROQ_API_KEY=your_groq_api_key_here
      ```
4.  **Run the application**:
    ```bash
    python app.py
    ```
5.  **Access the dashboard**:
    Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Deployment on Render

1.  **Push to GitHub/GitLab**: Ensure your code is in a git repository.
2.  **Create a new Web Service on Render**:
    - Connect your repository.
    - Set the **Build Command** to: `pip install -r requirements.txt`
    - Set the **Start Command** to: `gunicorn app:app`
3.  **Add Environment Variables**:
    - in the Render dashboard, go to the **Environment** tab.
    - Add `GROQ_API_KEY` with your actual API key value.
    - Add `PYTHON_VERSION` (optional, e.g., `3.9.0`) if needed.
4.  **Deploy**: Render will automatically build and deploy your application.

## Project Structure
- `app.py`: Main Flask application.
- `templates/`: HTML templates.
- `static/`: CSS and JavaScript files.
- `test_groq.py`: Test script for Groq API.
- `extract_pdf.py` / `extract_pdf_miner.py`: Scripts for PDF extraction.
