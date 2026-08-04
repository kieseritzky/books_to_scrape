from scraper.parsers import clean_key, clean_text

def test_clean_key():
    assert clean_key("Hello World") == "hello_world"

def test_clean_key_lower_case():
    assert clean_key("python") == "python"

def test_clean_key_uppercase():
    assert clean_key("PYTHON") == "python"

def test_clean_key_with_spaces():   # failed: need to add .strip to the clean key
    assert clean_key("  Python Dic  ") == "python_dic"

def test_clean_text():
    assert clean_text(" Hello World ") == "Hello World"

def test_clean_text_empty():
    assert clean_text("") == ""
    
def test_clean_text_spaces():
    assert clean_text("     ") == ""

def test_clean_text_tabs():
    assert clean_text("             ") == ""

def test_clean_text_new_line():
    assert clean_text("\n") == ""

def test_clean_text_numbers():
    assert clean_text("  asdf12  ") == "asdf12"

def test_clean_text_symbols():
    assert clean_text(" asdf 123 @#$ ") == "asdf 123 @#$"