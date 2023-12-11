SMOOTHING_UPPER_BOUND = 5

def smoothing(count_occurrences, table):
    smoothed_table = {}
    k = SMOOTHING_UPPER_BOUND
    
    N_k_plus_1 = count_occurrences.get(k + 1, 1)
    N_1 = count_occurrences.get(1, 1)
    
    normalization_factor  = 1 - (((k + 1) * N_k_plus_1) / N_1)
    
    for gram, count_ngram in table.items():
        if count_ngram > k:
            smoothed_table[gram] = count_ngram
        else:
            N_c = count_occurrences.get(count_ngram, 1)
            N_c_plus_1 = count_occurrences.get(count_ngram + 1, 1)
            smoothed_count  = (((count_ngram + 1) * N_c_plus_1) / N_c) - ((count_ngram * (k + 1) * N_k_plus_1) / N_1)
            smoothed_table[gram] = smoothed_count  / normalization_factor 
    
    return smoothed_table, N_1/sum(count_occurrences.values())

def count_occurrences(table):
    count_occurrences = {}
    for i in table:
        if table[i] in count_occurrences:
            count_occurrences[table[i]] += 1
        else:
            count_occurrences[table[i]] = 1
    return count_occurrences