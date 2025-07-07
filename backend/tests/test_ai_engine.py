from app.services.ai_engine import analyze_text_with_ai

def test_ai_mock_response():
    sample_text = "This is a legal contract between two parties..."
    result = analyze_text_with_ai(sample_text)

    assert result.summary != ""
    assert isinstance(result.clauses, list)
    assert isinstance(result.red_flags, list)
