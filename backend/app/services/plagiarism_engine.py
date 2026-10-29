import logging
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.preprocessing import normalize_text
from app.utils.similarity import compute_similarity
from app.db.mongo import plagiarism_collection
from datetime import datetime

# Optional advanced model
try:
    from sentence_transformers import SentenceTransformer, util
    SBERT_AVAILABLE = True
except:
    SBERT_AVAILABLE = False

# ---------------------------------------------------
# Logger
# ---------------------------------------------------
logger = logging.getLogger("plagiarism_service")

# ---------------------------------------------------
# Preprocessing
# ---------------------------------------------------
def preprocess(text: str) -> str:
    return " ".join(text.strip().lower().split())

# ---------------------------------------------------
# TF-IDF Similarity (Fast Method)
# ---------------------------------------------------
def tfidf_similarity(text1: str, texts: List[str]) -> List[float]:
    try:
        corpus = [text1] + texts

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)

        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        return similarities.tolist()

    except Exception as e:
        logger.exception(f"TF-IDF similarity error: {str(e)}")
        return [0.0] * len(texts)

# ---------------------------------------------------
# SBERT Similarity (Advanced)
# ---------------------------------------------------
def sbert_similarity(text1: str, texts: List[str]) -> List[float]:
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')

        embeddings = model.encode([text1] + texts, convert_to_tensor=True)

        similarities = util.cos_sim(embeddings[0], embeddings[1:])

        return similarities[0].cpu().tolist()

    except Exception as e:
        logger.warning(f"SBERT failed, fallback to TF-IDF: {str(e)}")
        return tfidf_similarity(text1, texts)

# ---------------------------------------------------
# Main Function
# ---------------------------------------------------
def check_plagiarism(
    input_text: str,
    comparison_texts: List[str],
    use_semantic: bool = True
) -> Dict:
    """
    Returns similarity scores between input_text and list of texts
    """

    try:
        logger.info("Starting plagiarism detection")

        input_text = normalize_text(input_text)
        comparison_texts = [normalize_text(t) for t in comparison_texts]
        
        # Choose method
        if use_semantic and SBERT_AVAILABLE:
            scores = sbert_similarity(input_text, comparison_texts)
        else:
            scores = compute_similarity(
                input_text,
                comparison_texts,
                use_semantic=use_semantic
            )

        matches = []
        total_score = 0

        for compared_text, score in zip(comparison_texts, scores):
            similarity = round(float(score) * 100, 2)

            matches.append({
                "compared_text": compared_text,
                "similarity_score": similarity
            })

            total_score += similarity

        overall_similarity = round(total_score / len(scores), 2) if scores else 0.0

        logger.info("Plagiarism detection completed")

        result = {
            "overall_similarity": overall_similarity,
            "matches": matches
        }

        try:
            plagiarism_collection.insert_one({
                "input_text": input_text,
                "results": result,
                "created_at": datetime.utcnow()
            })
        except Exception as db_error:
            logger.warning(f"MongoDB insert failed: {db_error}")

        return result

    except Exception as e:
        logger.exception(f"Plagiarism detection failed: {str(e)}")
        raise RuntimeError("Error in plagiarism engine")