import PyPDF2
from sentence_transformers import SentenceTransformer
import numpy as np
import httpx
import asyncio
import re

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"
TIMEOUT = 120.0


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=3):
    # Split into sentences, then group into chunks
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = ' '.join(sentences[i:i+chunk_size]).strip()
        if len(chunk) > 30:
            chunks.append(chunk)
    return chunks

class MonopolyRAGChat:
    def __init__(self):
        self.rules_text = extract_text_from_pdf("MonopolyRulebook.pdf")
        self.chunks = chunk_text(self.rules_text)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunk_embeddings = self.embedder.encode(self.chunks, convert_to_numpy=True)

    def retrieve(self, query, top_k=5):
        query_emb = self.embedder.encode([query], convert_to_numpy=True)[0]
        similarities = np.dot(self.chunk_embeddings, query_emb) / (
            np.linalg.norm(self.chunk_embeddings, axis=1) * np.linalg.norm(query_emb) + 1e-8
        )
        top_indices = similarities.argsort()[-top_k:][::-1]
        return [self.chunks[i] for i in top_indices]

    async def get_response(self, user_input):
        relevant_chunks = self.retrieve(user_input, top_k=5)
        context = "\n".join(relevant_chunks)
        prompt = (
            """
            You are a Monopoly rules expert. ONLY use the following monopoly rules to answer the question. 
            Provide a concise answer within 2-3 sentences. 
            If the explanation is complex, use bullet points. 
            If you are unsure of what the question is, ask the user to clarify the questions. 
            Try to provide immediate and accurate answers to the user to remove any confusion or excess efforts.\n\n
            """
            f"Relevant Rules:\n{context}\n\n"
            f"Question: {user_input}\nAnswer:"
        )
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                OLLAMA_API_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.4,
                        "top_p": 0.5,
                        "num_predict": 256
                    }
                }
            )
            result = response.json()
            return result["response"].strip()

async def main():
    chat = MonopolyRAGChat()
    print("\nWelcome to the Monopoly Rules Assistant!")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("Ask any question about Monopoly rules!\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                print("\nGoodbye!")
                break
            if not user_input:
                continue
            print("\nAssistant: ", end="", flush=True)
            response = await chat.get_response(user_input)
            print(response + "\n")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 
