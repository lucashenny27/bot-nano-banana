import chromadb
from chromadb.utils import embedding_functions

import os

# Initialize ChromaDB (Local) with OpenAI Embeddings
# Wrapped in a function or global try/except to avoid crashing the whole agent on import/init
collection = None

try:
    embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=embedding_model
    )
    chroma_client = chromadb.PersistentClient(path="./brain/memory_openai")
    collection = chroma_client.get_or_create_collection(name="post_history", embedding_function=openai_ef)
except Exception as e:
    print(f"⚠️ Critic Memory Disabled (Auth Error): {e}")
    collection = None

def quality_control(state):
    print("--- [Node] Critic (Quality Control) ---")
    draft = state.get("draft_caption")
    
    # 1. Check for Similarity (Duplication Check)
    if collection:
        try:
            results = collection.query(
                query_texts=[draft],
                n_results=1
            )
            if results['documents'] and results['documents'][0]:
                # If distance is very low, it means it's too similar (optional logic)
                pass
        except Exception as e:
            print(f"⚠️ Similarity check failed: {e}")
    else:
        print("ℹ️ Skipping similarity check (Memory disabled)")

    # 2. Heuristic Checks (Simple "Unit Tests")
    feedback = []
    if "#FuturaRadio" not in draft:
        feedback.append("Missing mandatory hashtag #FuturaRadio.")
    if len(draft) > 2200:
        feedback.append("Caption is too long for Instagram.")
    
    # Decision
    if feedback:
        return {
            "critique_feedback": " ".join(feedback),
            "status": "revision_needed"
        }
    else:
        # If approved, save to memory NOW (or after publish, but here is safe)
        if collection:
            try:
                collection.add(
                    documents=[draft],
                    ids=[str(hash(draft))]
                )
            except Exception:
                pass
        
        return {
            "critique_feedback": "APPROVED",
            "status": "approved"
        }
