def slugify(text):
    """
        Simply return the text lowercase and replace special characters and spaces with "-"
    """
    text = text.replace(" ", "-")
    text = text.replace(",", "-")
    text = text.replace("(", "-")
    text = text.replace(")", "")
    text = text.replace("؟", "")
    text = text.replace("?", "")
    text = text.replace("/", "")
    text = text.replace("!", "")
    text = text.replace(".", "")
    text = text.replace("،", "")
    text = text.replace(";", "")

    if text[len(text) - 1] == "-":
        text = text[:len(text) - 1]
    return text.lower()
