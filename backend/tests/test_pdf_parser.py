from app.services.pdf_parser import extract_text_from_pdf

def test_extract_text_from_pdf():
    with open("tests/sample.pdf", "rb") as f:
        content = f.read()
    text = extract_text_from_pdf(content)
    assert len(text) > 20
    assert "Agreement" in text  # example keyword
