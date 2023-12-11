import nltk
import math
import random
from utils.smoothing import smoothing, count_occurrences
from collections import Counter
from utils.process import END_OF_SENTENCE, END_OF_WORD

class LanguageModel():
    def __init__(self, tokens):
        self._init_unigram(tokens)
        self._init_bigram()
        self._init_trigram()
        
    def _init_unigram(self, tokens):
        self.tokens = tokens
        self.unigrams = list((nltk.ngrams(self.tokens, 1)))
        self.unigram_table = Counter(self.unigrams)
        self.unigram_count_occurrences = count_occurrences(self.unigram_table)
        self.unigram_frequencies, self.unigram_zero_counts = smoothing(self.unigram_count_occurrences, self.unigram_table)
        with open('output/unigram_frequencies.txt', 'w', encoding='utf-8') as file:
            for key, value in self.unigram_frequencies.items():
                key_str = ', '.join(key)  
                file.write(f'{key_str}: {value}\n')
    
    def _init_bigram(self):
        self.bigrams = list((nltk.ngrams(self.tokens, 2)))
        self.bigram_table = Counter(self.bigrams)
        self.bigram_count_occurrences = count_occurrences(self.bigram_table)
        self.bigram_frequencies, self.bigram_zero_counts = smoothing(self.bigram_count_occurrences, self.bigram_table)
        with open('output/bigram_frequencies.txt', 'w', encoding='utf-8') as file:
            for key, value in self.bigram_frequencies.items():
                key_str = ', '.join(key)  
                file.write(f'{key_str}: {value}\n')
    
    def _init_trigram(self):
        self.trigrams = list((nltk.ngrams(self.tokens, 3)))
        self.trigram_table = Counter(self.trigrams)
        self.trigram_count_occurrences = count_occurrences(self.trigram_table)
        self.trigram_frequencies, self.trigram_zero_counts = smoothing(self.trigram_count_occurrences, self.trigram_table)
        with open('output/trigram_frequencies.txt', 'w', encoding='utf-8') as file:
            for key, value in self.trigram_frequencies.items():
                key_str = ', '.join(key)  
                file.write(f'{key_str}: {value}\n')
                        
    def unigram_probability(self, syllable):
        numerator = self.unigram_frequencies.get(syllable, self.unigram_zero_counts)
        denominator = len(self.unigrams)
        return float(numerator) / float(denominator)
    
    def bigram_probability(self, prev, curr):
        numerator = self.bigram_frequencies.get((prev, curr), self.bigram_zero_counts)
        denominator = self.unigram_frequencies.get((prev,), self.unigram_zero_counts)
        return float(numerator) / float(denominator)

    def trigram_probability(self, prev1, prev2, curr):
        numerator = self.trigram_frequencies.get((prev1, prev2, curr), self.trigram_zero_counts)
        denominator = self.bigram_frequencies.get((prev1, prev2), self.bigram_zero_counts)
        return float(numerator) / float(denominator)
    
    def unigram_perplexity(self, tokens):
        number_of_tokens = len(tokens)
        if number_of_tokens < 1:
            return 0 
        
        prob_sum_logs = 0
        for syllable in tokens:
            syllable_probability = self.unigram_probability(syllable)
            prob_sum_logs += math.log(syllable_probability)

        perplexity = math.exp(-(prob_sum_logs / number_of_tokens))
        return perplexity

    def bigram_perplexity(self, tokens):
        number_of_tokens = len(tokens)
        if number_of_tokens < 2:
            return 0 
        
        prob_sum_logs = 0
        prev = None
        for curr in tokens:
            if prev is not None:
                syllable_probability = self.bigram_probability(prev, curr)
                prob_sum_logs += math.log(syllable_probability)
            prev = curr
        
        perplexity = math.exp(-(prob_sum_logs / (number_of_tokens - 1)))
        return perplexity
    
    def trigram_perplexity(self, tokens):
        number_of_tokens = len(tokens)
        if number_of_tokens < 3:
            return 0 
        
        prob_sum_logs = 0
        prev1, prev2 = None, None
        
        for curr in tokens:
            if prev1 is not None and prev2 is not None:
                syllable_probability = self.trigram_probability(prev1, prev2, curr)
                prob_sum_logs += math.log(syllable_probability) 
            prev1, prev2 = prev2, curr

        perplexity = math.exp(-(prob_sum_logs / (number_of_tokens - 2)))
        return perplexity
    
    def generate_random_sentence_unigram(self, n=5):
        sentence = []
        start_word = END_OF_SENTENCE
        sentence.append(start_word)

        total_frequency = sum(value for key, value in self.unigram_frequencies.items() if key[0] not in [END_OF_SENTENCE, END_OF_WORD])
        words = [key[0] for key in self.unigram_frequencies.keys() if key[0] not in [END_OF_SENTENCE, END_OF_WORD]]
        weights = [value / total_frequency for key, value in self.unigram_frequencies.items() if key[0] not in [END_OF_SENTENCE, END_OF_WORD]]

        for _ in range(n):
            next_word = random.choices(
                words,
                weights=weights,
                k=1
            )[0]
            sentence.append(next_word)
            
        sentence.append(END_OF_SENTENCE)
        return ' '.join(sentence)

    def generate_random_sentence_bigram(self, n=5):
        sentence = []
        start_word = END_OF_SENTENCE
        sentence.append(start_word)

        for _ in range(n):
            next_word_choices = [key[1] for key in self.bigram_frequencies.keys() if key[0] == start_word]
            weights = [self.bigram_frequencies[key] for key in self.bigram_frequencies.keys() if key[0] == start_word]

            if not next_word_choices:
                break

            next_word = random.choices(
                next_word_choices,
                weights=weights,
                k=1
            )[0]

            sentence.append(next_word)
            start_word = next_word

        sentence.append(END_OF_SENTENCE)
        return ' '.join(sentence)

    def generate_random_sentence_trigram(self, n=5):
        sentence = []
        start_words = random.choice([key for key in self.trigram_frequencies.keys() if key[0] == END_OF_SENTENCE and key[1] != END_OF_SENTENCE])
        sentence.extend(start_words)

        for _ in range(n - 2):
            prev_words = tuple(sentence[-2:])
            next_word_choices = [word[2] for word in self.trigram_frequencies.keys() if word[:2] == prev_words and word[2] != END_OF_SENTENCE]
            weights = [self.trigram_frequencies[word] for word in self.trigram_frequencies.keys() if word[:2] == prev_words and word[2] != END_OF_SENTENCE]

            if next_word_choices:
                next_word = random.choices(
                    next_word_choices,
                    weights=weights,
                    k=1
                )[0]
                sentence.append(next_word)
            else:
                break

        sentence.append(END_OF_SENTENCE)
        return ' '.join(sentence)