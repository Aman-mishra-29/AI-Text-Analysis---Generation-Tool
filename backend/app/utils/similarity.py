import logging
from typing import List
from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Optional semantic similarity
try:
    from sentence_transformers import SentenceTransformer, util
    SBERT_AVAILABLE = True
except Exception:
    SBERT_AVAILABLE = False

# ---------------------------------------------------
# Logger
# ---------------------------------------------------
logger = logging.getLogger("similarity_utils")


# ---------------------------------------------------
# TF-IDF Vectorizer (Cached)
# ---------------------------------------------------
@lru_cache(maxsize=1)
def get_vectorizer():
    """
    Cached TF-IDF vectorizer instance
    """
    try:
        return TfidfVectorizer()
    except Exception as e:
        logger.exception(f"Error initializing vectorizer: {str(e)}")
        raise RuntimeError("Failed to initialize TF-IDF vectorizer")


# ---------------------------------------------------
# Sentence-BERT Model (Cached)
# ---------------------------------------------------
@lru_cache(maxsize=1)
def get_sbert_model():
    """
    Cached SBERT model
    """
    if not SBERT_AVAILABLE:
        raise RuntimeError("SentenceTransformer is not available")

    try:
        logger.info("Loading SBERT model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("SBERT model loaded successfully")
        return model
    except Exception as e:
        logger.exception(f"Error loading SBERT model: {str(e)}")
        raise RuntimeError("Failed to load SBERT model")


# ---------------------------------------------------
# TF-IDF Cosine Similarity
# ---------------------------------------------------
def compute_tfidf_similarity(
    input_text: str,
    comparison_texts: List[str]
) -> List[float]:
    """
    Computes cosine similarity using TF-IDF
    """
    try:
        corpus = [input_text] + comparison_texts

        vectorizer = get_vectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)

        similarities = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:]
        ).flatten()

        return similarities.tolist()

    except Exception as e:
        logger.exception(f"TF-IDF similarity failed: {str(e)}")
        return [0.0] * len(comparison_texts)


# ---------------------------------------------------
# Sentence-BERT Similarity
# ---------------------------------------------------
def compute_sbert_similarity(
    input_text: str,
    comparison_texts: List[str]
) -> List[float]:
    """
    Computes semantic similarity using Sentence-BERT
    """
    try:
        model = get_sbert_model()

        embeddings = model.encode(
            [input_text] + comparison_texts,
            convert_to_tensor=True
        )

        similarities = util.cos_sim(
            embeddings[0],
            embeddings[1:]
        )

        return similarities[0].cpu().tolist()

    except Exception as e:
        logger.warning(f"SBERT failed: {str(e)}")
        return compute_tfidf_similarity(input_text, comparison_texts)


# ---------------------------------------------------
# Hybrid Similarity (Smart Selection)
# ---------------------------------------------------
def compute_similarity(
    input_text: str,
    comparison_texts: List[str],
    use_semantic: bool = True
) -> List[float]:
    """
    Wrapper function to choose similarity method
    """
    try:
        if use_semantic and SBERT_AVAILABLE:
            return compute_sbert_similarity(input_text, comparison_texts)
        else:
            return compute_tfidf_similarity(input_text, comparison_texts)

    except Exception as e:
        logger.exception(f"compute_similarity failed: {str(e)}")
        return [0.0] * len(comparison_texts)


# ---------------------------------------------------
# Pairwise Similarity (Advanced)
# ---------------------------------------------------
def pairwise_similarity(texts: List[str]) -> List[List[float]]:
    """
    Computes similarity matrix between multiple texts
    """
    try:
        if not texts:
            return []

        vectorizer = get_vectorizer()
        tfidf_matrix = vectorizer.fit_transform(texts)

        matrix = cosine_similarity(tfidf_matrix)

        return matrix.tolist()

    except Exception as e:
        logger.exception(f"pairwise_similarity failed: {str(e)}")
        return []


# ---------------------------------------------------
# Find Most Similar Text
# ---------------------------------------------------
def find_most_similar(
    input_text: str,
    comparison_texts: List[str],
    use_semantic: bool = True
):
    """
    Returns the most similar text with score
    """
    try:
        scores = compute_similarity(
            input_text,
            comparison_texts,
            use_semantic
        )

        if not scores:
            return None

        max_index = scores.index(max(scores))

        return {
            "text": comparison_texts[max_index],
            "score": round(scores[max_index] * 100, 2)
        }

    except Exception as e:
        logger.exception(f"find_most_similar failed: {str(e)}")
        return None