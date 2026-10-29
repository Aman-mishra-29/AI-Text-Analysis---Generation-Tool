import logging
from functools import lru_cache
from typing import Optional
from transformers import pipeline
from app.config import settings
from app.db.mongo import summaries_collection
from datetime import datetime


MODEL_NAME = settings.SUMMARIZATION_MODEL


# ---------------------------------------------------
# Logger
# ---------------------------------------------------
logger = logging.getLogger("summarizer_service")

# ---------------------------------------------------
# Model Configuration
# ---------------------------------------------------
MODEL_NAME = "facebook/bart-large-cnn"

# ---------------------------------------------------
# Lazy Load Summarization Pipeline (Cached)
# ---------------------------------------------------
@lru_cache(maxsize=1)
def get_summarizer():
    """
    Loads and caches the summarization model.
    Ensures model is loaded only once in memory.
    """
    try:
        logger.info(f"Loading summarization model: {MODEL_NAME}")

        summarizer = pipeline(
            "summarization",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
            framework="pt",   # PyTorch
            device=-1         # CPU (use 0 for GPU)
        )

        logger.info("Summarization model loaded successfully")
        return summarizer

    except Exception as e:
        logger.exception(f"Error loading summarization model: {str(e)}")
        raise RuntimeError("Failed to load summarization model")


# ---------------------------------------------------
# Text Preprocessing
# ---------------------------------------------------
def preprocess_text(text: str) -> str:
    """
    Basic text cleaning before inference
    """
    try:
        text = text.strip()
        text = text.replace("\n", " ")
        text = " ".join(text.split())  # remove extra spaces
        return text

    except Exception as e:
        logger.warning(f"Preprocessing failed: {str(e)}")
        return text


# ---------------------------------------------------
# Chunking for Large Texts
# ---------------------------------------------------
def chunk_text(text: str, max_chunk_size: int = 800) -> list:
    """
    Splits long text into smaller chunks for model processing
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_chunk_size):
        chunk = " ".join(words[i:i + max_chunk_size])
        chunks.append(chunk)

    return chunks


# ---------------------------------------------------
# Core Summarization Function
# ---------------------------------------------------
def summarize_text(
    text: str,
    max_length: Optional[int] = 130,
    min_length: Optional[int] = 30
) -> str:
    """
    Generates summary from input text
    Handles long text via chunking
    """
    try:
        logger.info("Starting summarization process")

        # Preprocess
        from app.utils.preprocessing import normalize_text

        clean_text = normalize_text(text)

        # Load model
        summarizer = get_summarizer()

        # Chunk large text
        chunks = chunk_text(clean_text)

        summaries = []

        for idx, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {idx + 1}/{len(chunks)}")

            # HuggingFace summarization
            result = summarizer(
                chunk,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )

            summary_text = result[0]["summary_text"]
            summaries.append(summary_text)

        # Combine summaries
        final_summary = " ".join(summaries)

        logger.info("Summarization completed successfully")

        try:
            summaries_collection.insert_one({
                "input_text": text,
                "summary": final_summary,
                "created_at": datetime.utcnow()
            })
        except Exception as db_error:
            logger.warning(f"MongoDB insert failed: {db_error}")

        return final_summary

    except Exception as e:
        logger.exception(f"Summarization failed: {str(e)}")
        raise RuntimeError("Error during summarization process")