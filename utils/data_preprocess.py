import re
from utils.syllabify import syllabify

HTML_TAG_PATTERN = r"<.*?>"
WHITESPACE_PATTERN = r"\s+"
WORD_SPLIT_PATTERN = r'\w+|[^\w\s]'
END_OF_SENTENCE_MARKS = ['.', '!', '?']

def preprocess():
    file_path = "dataset/wiki_00"
    processed_file_path = "dataset/wiki_00_processed"
    file_data = read_input(file_path)
    cleaned_text = clean_text(file_data)
    syllabified_text = syllabify_text(cleaned_text)
    write_output(processed_file_path, syllabified_text)
    print_head_and_tail(syllabified_text, cleaned_text)
    
def read_input(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_output(file_path, processed_text):
    with open(file_path, "w", encoding="utf-8") as processed_file:
        processed_file.write(processed_text)


def clean_text(text):
    clean_text = text.strip()
    clean_text = re.sub(HTML_TAG_PATTERN, "", clean_text)
    clean_text = re.sub(WHITESPACE_PATTERN, " ", clean_text)
    return clean_text

def syllabify_text(text):
    words = re.findall(WORD_SPLIT_PATTERN, text, re.UNICODE)
    syllabified_text = ""
    for word in words:
        if word.isalpha():
            syllables = syllabify(word)
            syllabified_text += syllables + " \w "
        elif word in END_OF_SENTENCE_MARKS:
            syllabified_text += "\s "
    return syllabified_text

def print_head_and_tail(syllabified_text, clean_text):
    head_length = 1000
    tail_length = 500
    print(syllabified_text[:head_length] + "..." + syllabified_text[-tail_length:])
    print("====================================================")
    print(clean_text[:head_length] + "..." + clean_text[-tail_length:])