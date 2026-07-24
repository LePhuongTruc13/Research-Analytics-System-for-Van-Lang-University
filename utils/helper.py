def extract_openalex_id(url):
    if not url:
        return None

    return url.rsplit("/", 1)[-1]