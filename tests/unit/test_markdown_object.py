import pytest

from obsidian_wrapper.markdown_object import MarkdownObject


@pytest.fixture
def fixture_header(request: int) -> str:
    header_num: int = request.param
    return (
        f"{'#' * header_num} This is a header, if it has less than or equal to 6 #'s",
        header_num,
    )


@pytest.mark.parametrize("fixture_header", [x for x in range(1, 7)], indirect=True)
def test_detect_valid_header(fixture_header):
    markdown_object = MarkdownObject(fixture_header[0], 0)

    assert markdown_object.line == [fixture_header[0]]
    assert markdown_object._index == 0
    assert markdown_object.attribute == f"h{fixture_header[1]}"


@pytest.mark.parametrize("fixture_header", [0, 7, 8, 9, 10], indirect=True)
def test_detect_invalid_header(fixture_header):
    markdown_object = MarkdownObject(fixture_header[0], 0)

    assert markdown_object.line == [fixture_header[0]]
    assert markdown_object._index == 0
    assert markdown_object.attribute == "text"


def test_detect_list():
    markdown_object = MarkdownObject("- This is a list", 0)

    assert markdown_object.line == ["- This is a list"]
    assert markdown_object._index == 0
    assert markdown_object.attribute == "list"


def test_detect_invalid_list():
    markdown_object = MarkdownObject("-This is a list", 0)

    assert markdown_object.line == ["-This is a list"]
    assert markdown_object._index == 0
    assert markdown_object.attribute == "text"


def test_detect_unchecked_checkbox():
    markdown_object = MarkdownObject("- [] This is a checkbox", 0)

    assert markdown_object.line == ["- [] This is a checkbox"]
    assert markdown_object._index == 0
    assert markdown_object.attribute == "checkBox-unchecked"


def test_detect_checked_checkbox():
    markdown_object = MarkdownObject("- [x] This is a checkbox", 0)

    assert markdown_object.line == ["- [x] This is a checkbox"]
    assert markdown_object._index == 0
    assert markdown_object.attribute == "checkBox-checked"
