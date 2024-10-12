def admin_check_type_validator(text: str) -> str:
    if isinstance(text, str) and len(text.strip()) > 1:
        return text
    raise ValueError
