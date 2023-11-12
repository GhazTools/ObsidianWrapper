import pytest

from obsidian_wrapper_plus.markdown_object import MarkdownObject


@pytest.fixture
def fixture_header(request: int) -> str:
    header_num: int = request.param
    return (
        f"{'#' * header_num} This is a header, if it has less than or equal to 6 #'s",
        str(header_num),
    )


@pytest.mark.parametrize("fixture_header", [x for x in range(1, 7)], indirect=True)
def test_detect_valid_header(fixture_header):
    markdown_object = MarkdownObject(fixture_header[0], 0, None)

    assert markdown_object.line == fixture_header[0]
    assert markdown_object._index == 0
    assert markdown_object.attribute == f"h"
    assert markdown_object.information == fixture_header[1]
    


@pytest.mark.parametrize("fixture_header", [0, 7, 8, 9, 10], indirect=True)
def test_detect_invalid_header(fixture_header):
    markdown_object = MarkdownObject(fixture_header[0], 0, None)

    assert markdown_object.line == fixture_header[0]
    assert markdown_object._index == 0
    assert markdown_object.attribute == "text"


def test_detect_list():
    markdown_object = MarkdownObject("- This is a list", 0, None)

    assert markdown_object.line == "- This is a list"
    assert markdown_object._index == 0
    assert markdown_object.attribute == "list"


def test_detect_invalid_list():
    markdown_object = MarkdownObject("-This is a list", 0, None)

    assert markdown_object.line == "-This is a list"
    assert markdown_object._index == 0
    assert markdown_object.attribute == "text"


def test_detect_unchecked_checkbox():
    markdown_object = MarkdownObject("- [] This is a checkbox", 0, None)

    assert markdown_object.line == "- [] This is a checkbox"
    assert markdown_object._index == 0
    assert markdown_object.attribute == "checkBox"
    assert markdown_object.information == "unchecked"



def test_detect_checked_checkbox():
    markdown_object = MarkdownObject("- [x] This is a checkbox", 0, None)

    assert markdown_object.line == "- [x] This is a checkbox"
    assert markdown_object._index == 0
    assert markdown_object.attribute == "checkBox"
    assert markdown_object.information == "checked"
    

def test_detect_codeblock():
    markdown_object = MarkdownObject("```python", 0, None)

    assert markdown_object.line == "```python"
    assert markdown_object._index == 0
    assert markdown_object.attribute == "code-block"
    assert markdown_object.information == "python"
    
    markdown_object = MarkdownObject("print(test)", 1, "code-block")
    
    assert markdown_object.line == "print(test)"
    assert markdown_object._index == 1
    assert markdown_object.attribute == "code-block-line"
    assert markdown_object.information == ""
    
    
    markdown_object = MarkdownObject("```", 2, "code-block-line")
    
    assert markdown_object.line == "```"
    assert markdown_object._index == 2
    assert markdown_object.attribute == "code-block-end"
    assert markdown_object.information == ""
