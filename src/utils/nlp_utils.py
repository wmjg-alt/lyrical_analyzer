import re
import spacy
from spacy.language import Language
from spacy.tokens import Token

def load_nlp_model() -> Language:
    """Load the English SpaCy model (Large for better word vectors)."""
    return spacy.load("en_core_web_lg")

def clean_raw_lyrics(text: str) -> str:
    """Remove Genius artifacts, headers, bios, and inline ads."""
    # 1. Remove Top Header (e.g., '29 ContributorsTranslations...Lyrics')
    # Use non-greedy .*? to stop at the FIRST instance of "Lyrics"
    text = re.sub(r"^\s*\d*\s*Contributors.*?Lyrics", "", text, flags=re.IGNORECASE | re.DOTALL)
    
    # 2. Remove Top Bio (if it truncates with '... Read More')
    text = re.sub(r"^.*?…\s*Read More\s*\n+", "", text, flags=re.IGNORECASE | re.DOTALL)
    
    # 3. Remove inline Ticket Ads
    text = re.sub(r"See\s.*?LiveGet tickets.*?You might also like", " ", text, flags=re.IGNORECASE | re.DOTALL)
    
    # 4. Remove section headers if they exist (e.g.[Chorus])
    text = re.sub(r"\[.*?\]", " ", text)
    
    # 5. Remove trailing 'Embed' artifact
    text = re.sub(r"\d*Embed$", "", text)
    
    return text.strip()

def is_valid_token(token: Token) -> bool:
    """Check if a token is a valid, non-stopword content word."""
    valid_pos = {"NOUN", "VERB", "ADJ", "ADV"}
    return token.is_alpha and not token.is_stop and token.pos_ in valid_pos

def extract_lemmas(doc: spacy.tokens.Doc) -> list[str]:
    """Extract valid lowercase lemmas from a SpaCy document."""
    return[token.lemma_.lower() for token in doc if is_valid_token(token)]