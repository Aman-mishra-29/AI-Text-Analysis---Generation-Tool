import logging
from typing import Dict, List
from app.db.mongo import autocorrect_collection
from datetime import datetime
from transformers import pipeline
import nltk

# LanguageTool for grammar correction
import language_tool_python


# ---------------------------------------------------
# Logger
# ---------------------------------------------------
logger = logging.getLogger("autocorrect_service")

# Load once (global)
grammar_corrector = pipeline(
    "text2text-generation",
    model="vennify/t5-base-grammar-correction"
)

def apply_ai_correction(text: str):
    result = grammar_corrector(
        "grammar: " + text,
        max_length=256
    )

    corrected = result[0]["generated_text"]

    return corrected, [{
        "original": text,
        "corrected": corrected,
        "message": "AI-based grammar correction"
    }]

# ---------------------------------------------------
# Initialize LanguageTool (Singleton)
# ---------------------------------------------------
_tool = None

def get_tool():
    global _tool
    if _tool is None:
        logger.info("Loading LanguageTool...")
        _tool = language_tool_python.LanguageTool('en-US')
        logger.info("LanguageTool loaded successfully")
    return _tool

# ---------------------------------------------------
# Preprocessing
# ---------------------------------------------------
def preprocess(text: str) -> str:
    return " ".join(text.strip().split())

def fix_capitalization(text: str) -> str:
    sentences = nltk.sent_tokenize(text)
    return " ".join(s.capitalize() for s in sentences)

# ---------------------------------------------------
# Apply Grammar Corrections
# ---------------------------------------------------
def apply_languagetool(text: str):
    tool = get_tool()
    matches = tool.check(text)

    corrected_text = language_tool_python.utils.correct(text, matches)
    corrected_text = corrected_text.capitalize()
    
    corrected_text = fix_capitalization(corrected_text)
    
    corrections = []
    
    autocorrect_collection.insert_one({
        "input_text": text,
        "corrected_text": corrected_text,
        "created_at": datetime.utcnow()
    })

    for match in matches:
        corrections.append({
            "original": text[match.offset: match.offset + match.errorLength],
            "corrected": match.replacements[0] if match.replacements else "",
            "message": match.message
        })
    
    return corrected_text, corrections


# ---------------------------------------------------
# Main Function
# ---------------------------------------------------
def correct_text(text: str) -> Dict:
    """
    Performs grammar + spelling correction
    """

    try:
        logger.info("Starting autocorrect process")

        from app.utils.preprocessing import clean_text

        text = clean_text(text)

        try:
            corrected_text, corrections = apply_ai_correction(text)

            if not corrections:
                logger.info("No corrections needed")

                autocorrect_collection.insert_one({
                    "input_text": text,
                    "corrected_text": text,
                    "created_at": datetime.utcnow()
                })
                corrected_text = fix_capitalization(corrected_text)
                
                return {
                    "corrected_text": text,
                    "corrections": []
                }

        except Exception as e:
            logger.warning(f"AI failed, fallback to LanguageTool: {str(e)}")
            corrected_text, corrections = apply_languagetool(text)

        corrected_text = fix_capitalization(corrected_text)
        
        logger.info("Autocorrect completed")

        # ✅ SAVE TO DB HERE (MAIN CASE)

        autocorrect_collection.insert_one({
            "input_text": text,
            "corrected_text": corrected_text,
            "created_at": datetime.utcnow()
        })

        logger.info("Autocorrect completed")

        return {
            "corrected_text": corrected_text,
            "corrections": corrections
        }

    except Exception as e:
        logger.exception(f"Autocorrect failed: {str(e)}")
        raise RuntimeError("Error in autocorrect engine")