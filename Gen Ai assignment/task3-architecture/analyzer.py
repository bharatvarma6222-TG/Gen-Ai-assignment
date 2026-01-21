from templates import TEMPLATES

def analyze_requirement(text: str):
    text = text.lower()

    if "chatbot" in text or "chat" in text:
        return TEMPLATES["chatbot"]

    if "ecommerce" in text or "shopping" in text:
        return TEMPLATES["ecommerce"]

    return {
        "modules": ["Frontend", "Backend", "Database"],
        "apis": ["POST /api"],
        "database": ["GenericTable(id, data)"],
        "pseudocode": ["Process request", "Return response"]
    }
