from src.utils.nlp_utils import clean_raw_lyrics, load_nlp_model, extract_lemmas

def test_clean_raw_lyrics_headers_and_embed() -> None:
    """Verify headers and Genius artifacts are removed."""
    raw_text = "[Chorus]\nWake up\nGrab a brush 123Embed"
    expected = "Wake up\nGrab a brush"
    assert clean_raw_lyrics(raw_text) == expected

def test_clean_raw_lyrics_genius_ads_and_bios() -> None:
    """Verify contributor tags, read more bios, and live ads are stripped."""
    raw_text = (
        "29 ContributorsTranslationsEspañolDeutschShimmy Lyrics“Shimmy” talks about stuff.\n"
        "… Read More \n"
        "Education, fornication, in you are; go\n"
        "See System of a Down LiveGet tickets as low as $100You might also like\n"
        "Don't be late"
    )
    expected = "Education, fornication, in you are; go\n \nDon't be late"
    assert clean_raw_lyrics(raw_text) == expected

def test_extract_lemmas() -> None:
    """Verify stop words are removed and structural words are lemmatized."""
    nlp = load_nlp_model()
    doc = nlp("The quickly running foxes jumped over the fences.")
    lemmas = extract_lemmas(doc)
    expected =["quickly", "run", "fox", "jump", "fence"]
    assert lemmas == expected