from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from typing import Dict
from pathlib import Path
import socket

from .models import ChatRequest, ChatResponse
from .data_processor import DataProcessor
from .rag_pipeline import RAGPipeline

# Load environment variables
env_path = Path('.env')
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded .env from {env_path.absolute()}")
else:
    print("⚠️ No .env file found, using environment variables")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sugar Spend AI Chatbot",
    description="RAG-powered chatbot for commodity spend analysis",
    version="1.0.0"
)

# CORS configuration - ALLOW ALL ORIGINS FOR NETWORK ACCESS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Changed to allow any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for pipeline
rag_pipeline: RAGPipeline = None
data_processor: DataProcessor = None
summary_stats: Dict = None

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Create a socket connection to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline on startup."""
    global rag_pipeline, data_processor, summary_stats

    logger.info("🚀 Starting up AI Chatbot...")

    # Get API key - REMOVE HARDCODED FALLBACK FOR SECURITY
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        logger.error("❌ GEMINI_API_KEY not found!")
        logger.error("Please create a .env file with: GEMINI_API_KEY=your_key")
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    logger.info(f"✅ API key found: {api_key[:10]}...")

    # Initialize data processor
    logger.info("📊 Loading and processing data...")
    data_processor = DataProcessor("data/Sugar_Spend_Data.csv")
    chunks = data_processor.create_text_chunks()
    summary_stats = data_processor.get_summary_stats()

    # Initialize RAG pipeline
    logger.info("🤖 Initializing RAG pipeline...")
    rag_pipeline = RAGPipeline(api_key=api_key)

    # Embed documents
    logger.info("📝 Embedding documents...")
    rag_pipeline.embed_documents(chunks)

    # Display network access info
    local_ip = get_local_ip()
    logger.info("✅ Startup complete! Ready to chat.")
    logger.info("="*60)
    logger.info("📡 Server is accessible at:")
    logger.info(f"   Local:   http://localhost:8000")
    logger.info(f"   Network: http://{local_ip}:8000")
    logger.info("="*60)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Sugar Spend AI Chatbot is running",
        "version": "1.0.0",
        "network_ip": get_local_ip()
    }

@app.get("/api/stats")
async def get_stats():
    """Get summary statistics about the data."""
    if not summary_stats:
        raise HTTPException(status_code=503, detail="Data not loaded yet")
    return summary_stats

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint for RAG queries."""
    if not rag_pipeline:
        raise HTTPException(
            status_code=503,
            detail="RAG pipeline not initialized yet"
        )

    try:
        logger.info(f"Received query: {request.message}")

        # Execute RAG pipeline
        response = rag_pipeline.query(
            user_query=request.message,
            conversation_history=request.conversation_history
        )

        return ChatResponse(
            answer=response["answer"],
            sources=response["sources"],
            relevant_context=response["relevant_context"]
        )

    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset")
async def reset_conversation():
    """Reset conversation history"""
    return {"message": "Conversation reset successfully"}

if __name__ == "__main__":
    import uvicorn
    local_ip = get_local_ip()
    print("\n" + "="*60)
    print("🚀 Starting Sugar Commodity AI Chatbot")
    print("="*60)
    print(f"📡 Access the API at:")
    print(f"   Local:   http://localhost:8000")
    print(f"   Network: http://{local_ip}:8000")
    print(f"   Docs:    http://localhost:8000/docs")
    print("="*60 + "\n")

    uvicorn.run(
        app,
        host="0.0.0.0",  # Listen on all network interfaces
        port=8000,
        log_level="info"
    )
