import re
import nltk
from tqdm import tqdm
from utils.syllabify import syllabify
from html2text import html2text
nltk.download('punkt')

WORD_SPLIT_PATTERN = re.compile(r'\w+|[^\w\s]')
END_OF_SENTENCE_MARKS = ['.', '!', '?']
END_OF_SENTENCE = "</s>"
END_OF_WORD = "</w>"
END_OF_WORD_V2 = " </w> "
CORPORA_PATH = "dataset/wiki_00"
TRAIN_PATH = "dataset/train_data"
TEST_PATH = "dataset/test_data"
TOTAL_NUMBER_OF_LINES = 4547965

def preprocess(percentage=100):
    train_number_of_lines, test_number_of_lines = split_train_test(percentage)
    processed_train_data = process_data(TRAIN_PATH, train_number_of_lines, "Preprocessing train data")
    processed_test_data = process_data(TEST_PATH, test_number_of_lines, "Preprocessing test data")
    return processed_train_data, processed_test_data

def process_data(file_path, number_of_lines, description):
    text = ''
    with open(file_path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(tqdm(f, total=number_of_lines, desc=description), 1):
            if line.isspace() or line_number > number_of_lines:
                continue
            
            line = line.strip()
            text += syllabify_text(html2text(line).lower().rstrip())
    
    return text

def split_train_test(corpora_usage_percentage, test_percentage=5):
    total_lines = int(TOTAL_NUMBER_OF_LINES * (corpora_usage_percentage / 100))
    test_lines_count = int(total_lines * test_percentage / 100)
    train_lines_count = total_lines - test_lines_count

    with open(CORPORA_PATH, "r", encoding="utf-8") as file:
        with open(TRAIN_PATH, "w", encoding="utf-8") as train_file:
            with open(TEST_PATH, "w", encoding="utf-8") as test_file:
                for line_number, line in enumerate(file, 1):
                    if line_number <= train_lines_count:
                        train_file.write(line)
                    else:
                        test_file.write(line)
                        if line_number == total_lines:
                            break

    return train_lines_count, test_lines_count
        
def syllabify_text(text):
    words = WORD_SPLIT_PATTERN.findall(text)
    syllabified_text = ''

    for word in words:
        if word.isalpha():
            syllables = syllabify(word)
            syllabified_text += syllables + END_OF_WORD_V2
        elif word in END_OF_SENTENCE_MARKS:
            last_occurrence = syllabified_text.rfind(END_OF_WORD_V2)
            if last_occurrence != -1:
                syllabified_text = syllabified_text[:last_occurrence] + ' ' + END_OF_SENTENCE + ' '

    return syllabified_text

def postprocess(tokens):
    processed_text = ''.join(tokens)
    processed_text = processed_text.replace(' ', '')
    processed_text = processed_text.replace('</s>', '')
    processed_text = processed_text.replace('</w>', ' ')
    return processed_text