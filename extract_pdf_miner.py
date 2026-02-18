from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

try:
    laparams = LAParams()
    text = extract_text(r'c:\Users\Dell\OneDrive\suuu\RESUME.2.pdf', laparams=laparams)
    print(text)
except Exception as e:
    print(f"Error: {e}")
