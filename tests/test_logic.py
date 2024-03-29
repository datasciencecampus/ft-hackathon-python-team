from src.hackathon.utils.logic import GREEN, GREY, YELLOW, get_colours


def test_get_colours():
    assert get_colours("WORDS", "PLOWS") == [YELLOW, YELLOW, GREY, GREY, GREEN]
    assert get_colours("LEAVE", "CLOSE") == [YELLOW, GREY, GREY, GREY, GREEN]
    assert get_colours("BABES", "KEBAB") == [YELLOW, YELLOW, GREEN, YELLOW, GREY]
    assert get_colours("KEBAB", "BASTE") == [GREY, YELLOW, YELLOW, YELLOW, GREY]
