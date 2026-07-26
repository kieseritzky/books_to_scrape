def clean_key(raw_key):
    return raw_key.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "").replace("#", "")

def clean_text(raw_text):
    if raw_text:
        return raw_text.strip()
    return ""