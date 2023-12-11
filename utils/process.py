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
TOTAL_NUMBER_OF_LINES = 4547965

def preprocess(percentage=100):
    print("Preprocessing corpora...")
    sentences = []
    USED_NUMBER_OF_LINES = int((percentage / 100) * TOTAL_NUMBER_OF_LINES)
    print("Total lines in file:", TOTAL_NUMBER_OF_LINES)
    print("Used lines in file:", USED_NUMBER_OF_LINES)
    
    with open(CORPORA_PATH, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(tqdm(f, total=USED_NUMBER_OF_LINES), 1):
            if line.isspace():
                continue
            
            if line_number > USED_NUMBER_OF_LINES:
                break
            
            line = line.strip()
            text = html2text(line).lower()
            text = text.rstrip()
            sentences.extend(nltk.sent_tokenize(text))  
    
    return split_data(sentences)

def split_data(sentences):
    total_sentences = len(sentences)
    test_sentences_count = max(1, total_sentences // 20)  

    test_sentences = sentences[-test_sentences_count:]  
    train_sentences = sentences[:-test_sentences_count]  

    train_text = ''.join(train_sentences)
    test_text = ''.join(test_sentences)
    
    train_syllabified = syllabify_text(train_text, process_name="Syllabifying train text")
    test_syllabified = syllabify_text(test_text, process_name="Syllabifying test text")
    
    # print_head_and_tail(train_syllabified, train_text)
    
    return train_syllabified, test_syllabified
    
def syllabify_text(text, process_name="Processing"):
    words = WORD_SPLIT_PATTERN.findall(text)
    syllabified_text = END_OF_SENTENCE + ' '
    total_words = len(words)
    
    with tqdm(total=total_words, desc=process_name) as pbar:
        for word in words:
            if word.isalpha():
                syllables = syllabify(word)
                syllabified_text += syllables + END_OF_WORD_V2
            elif word in END_OF_SENTENCE_MARKS:
                last_occurrence = syllabified_text.rfind(END_OF_WORD_V2)
                if last_occurrence != -1:
                    syllabified_text = syllabified_text[:last_occurrence] + ' ' + END_OF_SENTENCE + ' '
            
            pbar.update(1)
    
    return syllabified_text

def postprocess(tokens):
    processed_text = ''.join(tokens)
    processed_text = processed_text.replace(' ', '')
    processed_text = processed_text.replace('</s>', '')
    processed_text = processed_text.replace('</w>', ' ')
    return processed_text

    
def print_head_and_tail(syllabified_text, clean_text):
    head_length = 1000
    tail_length = 500
    print(syllabified_text[:head_length] + "..." + syllabified_text[-tail_length:])
    print("====================================================")
    print(clean_text[:head_length] + "..." + clean_text[-tail_length:])