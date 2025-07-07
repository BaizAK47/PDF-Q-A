from flask import Flask, request, jsonify, render_template
from model_utils import answer_question_from_pdf
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serves the webpage

@app.route('/ask', methods=['POST'])
def ask_question():
    if 'pdf' not in request.files or 'question' not in request.form:
        return jsonify({"error": "PDF file and question are required"}), 400

    pdf = request.files['pdf']
    question = request.form['question']

    pdf_path = os.path.join("temp", pdf.filename)
    os.makedirs("temp", exist_ok=True)
    pdf.save(pdf_path)

    try:
        answer = answer_question_from_pdf(pdf_path, question)
        return jsonify({"question": question, "answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(pdf_path)

if __name__ == '__main__':
    app.run(debug=True)
