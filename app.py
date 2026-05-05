from flask import Flask,request,jsonify,send_from_directory
from pypdf import PdfReader
from collections import Counter
import re
 
app = Flask(__name__)
 
@app.route("/")
def index():
    return send_from_directory("static","index.html")
 
@app.route("/analyze", methods=["POST"])
def analyze_pdf():
    file=request.files["pdf"]
    extracted_text=extract_text(file)
    results=analyze(extracted_text)
    return jsonify(results)
 
 
def extract_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
 
def analyze(extracted_file):
    return {
        "Total characters"     : len(extracted_file),
        "Characters no spaces" : len(extracted_file.replace(" ", "").replace("\n", "")),
        "Total letters"        : len(re.findall("[a-zA-Z]", extracted_file)),
        "Total digits"         : len(re.findall("[0-9]", extracted_file)),
        "Total words"          : len(re.findall("[a-zA-Z]+", extracted_file)),
        "Total sentences"      : len([s for s in re.split("[.!?]", extracted_file) if s.strip()]),
        "Total paragraphs"     : len([p for p in extracted_file.split("\n") if p.strip()]),
        "Most common word"     : Counter(re.findall("[a-zA-Z]+", extracted_file.lower())).most_common(1),
    }
 
if __name__ == "__main__":
    app.run(debug=True)