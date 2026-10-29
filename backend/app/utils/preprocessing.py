import re
import logging
from typing import List

# ---------------------------------------------------
# Logger
# ---------------------------------------------------
logger = logging.getLogger("preprocessing_utils")


# ---------------------------------------------------
# Basic Text Cleaning
# ---------------------------------------------------
def clean_text(text: str) -> str:
    """
    Cleans raw text:
    - Removes extra spaces
    - Normalizes whitespace
    - Removes unwanted characters (optional safe cleaning)
    """
    try:
        if not text:
            return ""

        text = text.strip()

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)

        return text

    except Exception as e:
        logger.warning(f"clean_text failed: {str(e)}")
        return text


# ---------------------------------------------------
# Lowercase Conversion
# ---------------------------------------------------
def to_lower(text: str) -> str:
    try:
        return text.lower()
    except Exception as e:
        logger.warning(f"to_lower failed: {str(e)}")
        return text


# ---------------------------------------------------
# Remove Special Characters
# ---------------------------------------------------
def remove_special_characters(text: str) -> str:
    """
    Keeps only alphabets, numbers, and basic punctuation
    """
    try:
        return re.sub(r"[^a-zA-Z0-9\s.,!?']", "", text)
    except Exception as e:
        logger.warning(f"remove_special_characters failed: {str(e)}")
        return text


# ---------------------------------------------------
# Sentence Tokenization (Simple)
# ---------------------------------------------------
def split_sentences(text: str) -> List[str]:
    """
    Splits text into sentences using regex
    """
    try:
        sentences = re.split(r'(?<=[.!?]) +', text)
        return [s.strip() for s in sentences if s.strip()]
    except Exception as e:
        logger.warning(f"split_sentences failed: {str(e)}")
        return [text]


# ---------------------------------------------------
# Word Tokenization
# ---------------------------------------------------
def tokenize_words(text: str) -> List[str]:
    try:
        return text.split()
    except Exception as e:
        logger.warning(f"tokenize_words failed: {str(e)}")
        return []


# ---------------------------------------------------
# Remove Stopwords (Optional)
# ---------------------------------------------------
DEFAULT_STOPWORDS = set([
    "the", "is", "in", "and", "to", "of", "a", "on", "for", "with", "as", "by", "an"
])

def remove_stopwords(text: str, stopwords: set = DEFAULT_STOPWORDS) -> str:
    try:
        words = text.split()
        filtered = [w for w in words if w.lower() not in stopwords]
        return " ".join(filtered)
    except Exception as e:
        logger.warning(f"remove_stopwords failed: {str(e)}")
        return text


# ---------------------------------------------------
# Normalize Text (Full Pipeline)
# ---------------------------------------------------
def normalize_text(
    text: str,
    lower: bool = True,
    remove_special: bool = False,
    remove_stop_words: bool = False
) -> str:
    """
    Full preprocessing pipeline
    """
    try:
        text = clean_text(text)

        if lower:
            text = to_lower(text)

        if remove_special:
            text = remove_special_characters(text)

        if remove_stop_words:
            text = remove_stopwords(text)

        return text

    except Exception as e:
        logger.exception(f"normalize_text failed: {str(e)}")
        return text


# ---------------------------------------------------
# Text Length Validation
# ---------------------------------------------------
def validate_text_length(text: str, min_words: int = 1, max_words: int = 10000) -> bool:
    try:
        word_count = len(text.split())
        return min_words <= word_count <= max_words
    except Exception as e:
        logger.warning(f"validate_text_length failed: {str(e)}")
        return False


# ---------------------------------------------------
# Chunk Text (Reusable Utility)
# ---------------------------------------------------
def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """
    Splits text into chunks of N words
    """
    try:
        words = text.split()
        return [
            " ".join(words[i:i + chunk_size])
            for i in range(0, len(words), chunk_size)
        ]
    except Exception as e:
        logger.warning(f"chunk_text failed: {str(e)}")
        return [text]


# ---------------------------------------------------
# Highlight Matching Words (For Plagiarism UI)
# ---------------------------------------------------
def highlight_overlap(text1: str, text2: str) -> List[str]:
    """
    Returns overlapping words between two texts
    (basic version for UI highlighting)
    """
    try:
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        overlap = words1.intersection(words2)

        return list(overlap)

    except Exception as e:
        logger.warning(f"highlight_overlap failed: {str(e)}")
        return []