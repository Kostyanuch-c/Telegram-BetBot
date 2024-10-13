def admin_check_confirmed_refs_id_validator(text: str) -> str:
    """Todo сделать проверку на ввод списка реферальны id которые успешно прошли проверку"""
    if isinstance(text, str) and len(text.strip()) > 1:
        return text
    raise ValueError()
