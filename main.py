import argparse
from language_model import LanguageModel
from utils.process import preprocess, postprocess

def calculate_perplexity(model, sentences):    
    with open("output/perplexity_output.txt", "w", encoding='utf-8') as output_file:
        i = 1
        for sentence in sentences:
            test_tokens = sentence.split()
            if len(test_tokens) > 2:
                output_file.write("Sentence {}: {}\n".format(i, postprocess(sentence)))
                output_file.write("Unigram perplexity: {}\n".format(model.unigram_perplexity(test_tokens)))
                output_file.write("Bigram perplexity: {}\n".format(model.bigram_perplexity(test_tokens)))
                output_file.write("Trigram perplexity: {}\n\n".format(model.trigram_perplexity(test_tokens)))  
                i += 1
    print("Perplexity is calculated for the test sentences. You can find it in output/perplexity_output.txt")

def write_test_data(test_data):
        with open("dataset/test_data", "w", encoding="utf-8") as f:
            f.write(test_data)

def random_sentence_generate(model, rounds=3):
    with open("output/random_sentences_output.txt", "w", encoding='utf-8') as output_file:
        for round_num in range(1, rounds + 1):
            output_file.write(f"Round {round_num}:\n")
            output_file.write(f"Unigram: {model.generate_random_sentence_unigram()}\n")
            output_file.write(f"Bigram: {model.generate_random_sentence_bigram()}\n")
            output_file.write(f"Trigram: {model.generate_random_sentence_trigram()}\n\n")
    
    print("Random sentences with 5 syllables are created. You can find it in output/random_sentences_output.txt")
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process corpora based on a given percentage')
    parser.add_argument('--corpora-usage', type=int, help='Percentage of corpora to use (1-100)')
    args = parser.parse_args()
    corpora_percentage = args.corpora_usage
    
    if not (1 <= corpora_percentage <= 100):
        print("Please enter a valid percentage between 1 and 100.")
    else:
        train_data, test_data = preprocess(percentage=corpora_percentage)
        train_tokens = train_data.split()
        write_test_data(test_data)
        sentences = test_data.split(r'</s>')
        language_model = LanguageModel(train_tokens)
        calculate_perplexity(language_model, sentences)
        random_sentence_generate(language_model)