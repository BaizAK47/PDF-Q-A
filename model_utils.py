import fitz  # PyMuPDF
import numpy as np
from logger import logger
import faiss
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load models once
embedder = SentenceTransformer("all-MiniLM-L6-v2")
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

# Global index and chunk store (can be improved later)
chunk_store = []
faiss_index = None

def extract_text_from_pdf(pdf_path):
    logger.info(f"Extracting text from: {pdf_path}")
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    logger.info(f"Total text length: {len(text)} characters")
    return text

def build_index(text):
    global faiss_index, chunk_store
    chunk_store.clear()

    logger.info("Splitting text into chunks...")
    chunks = text_splitter.split_text(text)
    logger.info(f"Created {len(chunks)} chunks")

    chunk_store.extend(chunks)

    logger.info("Embedding chunks...")
    embeddings = embedder.encode(chunks)
    dim = embeddings[0].shape[0]
    faiss_index = faiss.IndexFlatL2(dim)
    faiss_index.add(np.array(embeddings))
    logger.info(f"FAISS index built with dimension: {dim}")

def retrieve_top_chunks(query, k=3):
    logger.info(f"Retrieving top {k} chunks for query: '{query}'")
    if faiss_index is None:
        logger.error("FAISS index not built!")
        return []
    query_vec = embedder.encode([query])
    distances, indices = faiss_index.search(np.array(query_vec), k)
    top = [chunk_store[i] for i in indices[0]]
    for i, chunk in enumerate(top):
        logger.info(f"Chunk {i+1}: {chunk[:100]}...")  # preview
    return top

def answer_question_from_pdf(pdf_path, question):
    logger.info(f"QUESTION: {question}")
    text = extract_text_from_pdf(pdf_path)
    build_index(text)
    top_chunks = retrieve_top_chunks(question, k=3)
    context = " ".join(top_chunks)
    result = qa_pipeline(question=question, context=context)
    logger.info(f"ANSWER: {result['answer']}")
    return result["answer"]