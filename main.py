import argparse
from utils.process import preprocess, postprocess, get_test_data, get_train_data
from language_model import LanguageModel

def calculate_perplexity(model, sentences):    
    with open("output/perplexity_output", "w", encoding='utf-8') as output_file:
        i = 1
        for sentence in sentences:
            test_tokens = sentence.split()
            if len(test_tokens) > 2:
                output_file.write("Sentence {}: {}\n".format(i, postprocess(sentence)))
                output_file.write("Unigram perplexity: {}\n".format(model.unigram_perplexity(test_tokens)))
                output_file.write("Bigram perplexity: {}\n".format(model.bigram_perplexity(test_tokens)))
                output_file.write("Trigram perplexity: {}\n\n".format(model.trigram_perplexity(test_tokens)))  
                i += 1
    print("Perplexity is calculated for the test sentences. You can find it in output/perplexity_output")

def random_sentence_generate(model, rounds=15):
    with open("output/random_sentences_output", "w", encoding='utf-8') as output_file:
        for round_num in range(1, rounds + 1):
            output_file.write(f"Round {round_num}:\n")
            output_file.write(f"Unigram: {model.generate_random_sentence_unigram()}\n")
            output_file.write(f"Bigram: {model.generate_random_sentence_bigram()}\n")
            output_file.write(f"Trigram: {model.generate_random_sentence_trigram()}\n\n")
    
    print("Random sentences with 5 syllables are created. You can find it in output/random_sentences_output")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process corpora based on a given percentage')
    parser.add_argument('--corpora-usage', type=int, help='Percentage of corpora to use (1-100)')
    args = parser.parse_args()
    corpora_percentage = args.corpora_usage
    
    if not (1 <= corpora_percentage <= 100):
        print("Please enter a valid percentage between 1 and 100.")
    else:
        preprocess(percentage=corpora_percentage)
        train_data, test_data = get_train_data(), get_test_data()
        print("Getting tokens from train data...")
        train_tokens = train_data.split()
        print("Getting sentences from test data...")
        sentences = test_data.split(r'</s>')
        language_model = LanguageModel(train_tokens)
        print("Calculating perplexity for test sentencess...")
        calculate_perplexity(language_model, sentences)
        print("Creating random sentences with 5 syllables...")
        random_sentence_generate(language_model)