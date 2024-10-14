from telegram_betbot.tgbot.lexicon.lexicon import LEXICON_START_MESSAGE


def create_start_message(  # noqa: C901
        response_data: dict, streamer_pari: list, streamer_upx: list,
) -> dict:
    status_pari = response_data.get("status_pari")
    status_upx = response_data.get("status_upx")
    if status_pari == "not_attempted" and status_upx == "not_attempted":
        response_data["middle_text"] = LEXICON_START_MESSAGE["clear_user"]
        state = "clear_user"
    elif not status_pari and status_upx == "not_attempted":
        response_data["middle_text"] = LEXICON_START_MESSAGE[
            "start_with_only_one_pending_bm"
        ].format(
            bookmaker_pending="Pari",
            streamer_pending=streamer_pari[0],
        )
        state = "only_pari_pending"
    elif not status_upx and status_pari == "not_attempted":
        response_data["middle_text"] = LEXICON_START_MESSAGE[
            "start_with_only_one_pending_bm"
        ].format(
            bookmaker_pending="Up-x",
            streamer_pending=streamer_upx[0],
        )
        state = "only_upx_pending"
    elif not status_upx and not status_pari:
        response_data["streamer_pending_upx"] = streamer_upx[0]
        response_data["streamer_pending_pari"] = streamer_pari[0]
        state = "all_pending"
    elif status_pari and status_upx == "not_attempted":
        response_data["middle_text"] = LEXICON_START_MESSAGE[
            "start_with_only_one_confirm_bm"
        ].format(
            bookmaker_confirm="Pari",
            streamer_confirm=streamer_pari[0],
        )
        state = "only_pari_confirm"
    elif status_upx and status_pari == "not_attempted":
        response_data["middle_text"] = LEXICON_START_MESSAGE[
            "start_with_only_one_confirm_bm"
        ].format(
            bookmaker_confirm="Up-x",
            streamer_confirm=streamer_upx[0],
        )
        state = "only_upx_confirm"
    elif status_pari and not status_upx:
        response_data["bookmaker_pending"] = "Up-x"
        response_data["streamer_pending"] = streamer_upx[0]
        response_data["streamer_confirm"] = streamer_pari[0]
        response_data["bookmaker_confirm"] = "Pari"
        state = "confirm_pari_pending_upx"
    elif status_upx and not status_pari:
        response_data["bookmaker_pending"] = "Pari"
        response_data["streamer_pending"] = streamer_pari[0]
        response_data["streamer_confirm"] = streamer_upx[0]
        response_data["bookmaker_confirm"] = "Up-x"
        state = "confirm_upx_pending_pari"
    else:
        response_data["streamer_pari"] = streamer_pari[0]
        response_data["streamer_upx"] = streamer_upx[0]
        state = "all_confirm"

    response_data["current_state_user"] = state
    response_data["one_or_more_not_free"] = state in (
        "all_pending",
        "confirm_pari_pending_upx",
        "confirm_upx_pending_pari",
        "all_confirm",
    )
    return response_data
