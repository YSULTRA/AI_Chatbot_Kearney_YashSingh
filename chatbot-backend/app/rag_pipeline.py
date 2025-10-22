import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from typing import List, Dict, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEMINI_API_KEY = "AIzaSyBCV6yfpF7P0hShf5IpOQSoFe0_0IcvW3Y"


class RAGPipeline:
    """
    Simple and effective RAG pipeline following core principles:

    STEP 1: Embed user query using the same model as documents
    STEP 2: Find relevant chunks from vector database
    STEP 3: Generate answer using LLM with retrieved context
    """

    def __init__(self, api_key: str, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory

        # STEP 1: Initialize embedding model
        # Why: We need the SAME model for both documents and queries
        logger.info("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-mpnet-base-v2')
        logger.info("✅ Embedding model loaded: all-mpnet-base-v2 (768 dimensions)")

        # STEP 2: Initialize vector database (ChromaDB)
        # Why: Store document embeddings for fast similarity search
        logger.info("Initializing ChromaDB...")
        self.chroma_client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )

        self.collection_name = "sugar_spend_data"
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Sugar commodity spend data"}
        )
        logger.info(f"✅ Vector database ready: {self.collection.count()} documents")

        # STEP 3: Initialize LLM (Gemini)
        # Why: Generate natural language answers from retrieved context
        genai.configure(api_key=api_key)
        self.llm_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        logger.info("✅ Gemini LLM initialized")

        # Configuration
        self.top_k = 30  # Number of relevant chunks to retrieve

    def embed_documents(self, chunks: List[Dict]):
        """
        STEP 1: Embed CSV data and store in vector database.

        Process:
        1. Convert each CSV row to text
        2. Generate embedding vector (768 dimensions)
        3. Store in ChromaDB with metadata
        """
        if self.collection.count() > 0:
            logger.info(f"✅ Collection already has {self.collection.count()} documents (skipping embedding)")
            return

        logger.info(f"📝 Embedding {len(chunks)} CSV rows...")

        # Extract data from chunks
        texts = [chunk["text"] for chunk in chunks]
        ids = [chunk["id"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]

        # Generate embeddings using the same model
        # Why: Query embeddings must use the same model for valid similarity comparison
        embeddings = self.embedding_model.encode(
            texts,
            batch_size=16,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # Normalize for cosine similarity
        ).tolist()

        # Store in vector database
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            ids=ids,
            metadatas=metadatas
        )

        logger.info(f"✅ Successfully embedded and stored {len(chunks)} documents")

    def retrieve_relevant_chunks(self, query: str) -> Tuple[List[str], List[Dict]]:
        """
        CORE RAG STEP 2: Retrieve relevant chunks for the query.

        Process:
        1. Convert user query to embedding (using SAME model as documents)
        2. Find top-k most similar documents using cosine similarity
        3. Return the relevant text chunks and their metadata
        """
        logger.info(f"🔍 Retrieving relevant chunks for: '{query}'")

        # STEP 2.1: Embed the query using the SAME model as documents
        # Why: Query and document embeddings must be in the same vector space
        query_embedding = self.embedding_model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        ).tolist()

        logger.info(f"✅ Query embedded (768-dimensional vector)")

        # STEP 2.2: Search vector database for similar chunks
        # ChromaDB uses cosine similarity to find closest matches
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k,
            include=["documents", "metadatas", "distances"]
        )

        # Extract results
        contexts = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        logger.info(f"✅ Retrieved {len(contexts)} relevant chunks")
        logger.info(f"   Similarity scores: {[f'{1-d:.3f}' for d in distances]}")

        return contexts, metadatas

    def generate_answer(
        self,
        query: str,
        contexts: List[str],
        metadatas: List[Dict],
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        CORE RAG STEP 3: Generate answer using LLM with retrieved context.

        Process:
        1. Build prompt with retrieved context
        2. Add conversation history if available
        3. Send to LLM (Gemini)
        4. Return generated answer with sources
        """
        logger.info(f"🤖 Generating answer using {len(contexts)} context chunks")

        # STEP 3.1: Build context section from retrieved chunks
        context_section = "\n\n".join([
            f"Context {i+1}:\n{ctx}"
            for i, ctx in enumerate(contexts)
        ])

        # STEP 3.2: Add conversation history (for multi-turn conversations)
        history_section = ""
        if conversation_history and len(conversation_history) > 0:
            history_section = "Previous conversation:\n"
            for msg in conversation_history[-3:]:  # Last 3 exchanges
                history_section += f"{msg['role']}: {msg['content']}\n"
            history_section += "\n"

        # STEP 3.3: Construct prompt for LLM
        prompt = f"""You are an AI assistant analyzing sugar commodity spend data. Answer the user's question accurately using ONLY the provided context.

{history_section}

CONTEXT INFORMATION:
{context_section}

USER QUESTION: {query}

INSTRUCTIONS:
1. Answer based ONLY on the provided context
2. Be specific with numbers (quantities in kg, spend in USD, suppliers, commodities)
3. Format numbers clearly (e.g., $1,234.56, 1,000 kg)
4. If the context doesn't have the information, say so
5. Be concise but complete

ANSWER:"""

        try:
            # STEP 3.4: Generate response using Gemini LLM
            response = self.llm_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,  # Low temperature = more factual
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=512,
                )
            )
            answer = response.text

            logger.info("✅ Answer generated successfully")

            return {
                "answer": answer,
                "sources": metadatas,
                "relevant_context": contexts,
                "num_sources": len(contexts)
            }

        except Exception as e:
            logger.error(f"❌ Error generating answer: {e}")
            return {
                "answer": f"Sorry, I encountered an error: {str(e)}",
                "sources": [],
                "relevant_context": [],
                "num_sources": 0
            }

    def query(
        self,
        user_query: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        COMPLETE RAG PIPELINE - Main entry point

        STEP 1: Convert query to embedding (same model as documents)
        STEP 2: Retrieve relevant chunks from vector database
        STEP 3: Generate answer using LLM with context
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"📥 NEW QUERY: {user_query}")
        logger.info(f"{'='*60}")

        # STEP 1: Retrieve relevant context chunks
        # (Query embedding happens inside this function)
        contexts, metadatas = self.retrieve_relevant_chunks(user_query)

        # STEP 2: Generate answer using LLM
        response = self.generate_answer(
            user_query,
            contexts,
            metadatas,
            conversation_history
        )

        logger.info(f"{'='*60}\n")

        return response


