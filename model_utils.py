# model_utils.py
import fitz  # PyMuPDF
from transformers import pipeline

# Load QA pipeline
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def answer_question_from_pdf(pdf_path, question):
    context = extract_text_from_pdf(pdf_path)
    result = qa_pipeline(question=question, context=context)
    return result['answer']
