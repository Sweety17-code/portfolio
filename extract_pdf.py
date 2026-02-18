import sys

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 not installed")
    sys.exit(1)

try:
    with open(r'c:\Users\Dell\OneDrive\suuu\RESUME.2.pdf', 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        print(text)
except Exception as e:
    print(f"Error: {e}")
