def validate_niche_input(niche):
    if not niche or not niche.replace(" ","").isalnum():
        raise ValueError("Niche input must be a non-empty alphanumeric string.")
    return niche


def handle_api_error(error):
    return {"error": str(error), "message": "Something went wrong with the API call."}
