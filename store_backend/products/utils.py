def arabic_slugify(text):
    text = text.replace(" ", "-")
    text = text.replace(",", "-")
    text = text.replace("(", "-")
    text = text.replace(")", "")
    text = text.replace("؟", "")
    return text.lower()
