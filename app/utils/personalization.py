def get_client_prompt_modifier(client_type):
    
    if client_type == "Retail":
        return """
        Use simple, non-technical language.
        Focus on clarity and easy explanation.
        Avoid jargon.
        """
    
    elif client_type == "Institutional":
        return """
        Use professional, technical financial language.
        Include terms like alpha, sector allocation, and macro trends.
        """
    
    return ""