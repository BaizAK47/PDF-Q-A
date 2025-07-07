# test_request.py
import requests

pdf_path = "Analysis.pdf"
question = "What are the keywords present?"

response = requests.post(
    "http://127.0.0.1:5000/ask",
    files={"pdf": open(pdf_path, "rb")},
    data={"question": question}
)

print(response.json())
