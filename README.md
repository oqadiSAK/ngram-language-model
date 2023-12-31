# Introduction

The project is developed using Python. To run the program, you need to
install the requirements. You can install them with the command:

    $ pip install -r requirements.txt

After installation, you can run the program as follows:

    $ python main.py --corpora-usage [1-100]

Note that you need to provide the corpora usage percentage as a program
argument and the corpora file \"wiki_00\" under the data folder in the
project. It accepts numbers between 1 and 100. After running the
program, you can find the related outputs under the output folder:

-   Processed versions of the train and test data.

-   Perplexity calculations for each sentence in the test data.

-   Randomly generated sentences with 5 syllables.

-   Unigram, bigram, and trigram tables. These tables represent
    frequency counts after applying Good-Turing smoothing.

-   The n-gram tables are stored as dictionaries. Whenever the 'UNK'
    element is encountered in the test data, a zero-count probability is
    utilized.

# Data and Data Processing

## Data

The dataset utilized for this project is available on Kaggle at the
following URL:
<https://www.kaggle.com/datasets/mustfkeskin/turkish-wikipedia-dump>. To
proceed with the project, download the dataset and place the file named
`wiki_00` within the designated data folder. Here is the head of the
data:

    <doc id="10" url="https://tr.wikipedia.org/wiki?curid=10" title="Cengiz Han">
    Cengiz Han

    Cengiz Han ("Cenghis Khan", "Çinggis Haan" ya da doğum adıyla Temuçin
    ...

## Data Preprocessing

The dataset preprocessing involves several steps:

-   **HTML Tag Removal:** Utilizing the `html2text` library, HTML tags
    within the dataset are removed, ensuring clean text for analysis.

-   **Text Syllabification:** The text undergoes syllabification using
    custom functions and regex patterns to convert words into syllables.
    Also used some special tokens to represents spaces between words and
    end of the sentences.

    -   **`</w>`:** Represents a space between words.

    -   **`</s>`:** Represents the end of a sentence.

-   **Train-Test Split:** The dataset is split into training and test
    sets based on a given percentage, enabling model training and
    evaluation.

# Ngrams

While constructing ngrams, the NLTK library was utilized to generate
these sequences from the provided tokens. The ngrams are maintained in a
dictionary structure owing to numerous empty entries in both bigrams and
trigrams.

To optimize storage and computational efficiency, the ngram tables were
organized as dictionaries. In cases where a specific pair did not exist
within the dictionary, a zero count probability was assigned.

The approach involved three distinct functions to handle unigrams,
bigrams, and trigrams:

## Unigrams

The unigram data was created by tokenizing the input and employing NLTK
to generate these single-word sequences. After obtaining the unigrams,
occurrences were counted, and a smoothing technique was applied to
handle instances of zero counts. The resulting frequencies were written
to an output file named `unigram_frequencies`.

## Bigrams

Similar to unigrams, bigrams were generated from the provided tokens.
Counting occurrences and applying smoothing were performed to handle any
zero-count instances in the bigram data. The frequencies were then
written to the output file named `bigram_frequencies`.

## Trigrams

Trigrams were generated by NLTK using the tokenized input. Similar steps
were taken for counting occurrences, applying smoothing to handle
potential zero counts, and storing the resulting frequencies in the
output file `trigram_frequencies`.

# Smoothing

For smoothing, the Good-Turing algorithm is utilized. In practice, we
can assume that large counts (i.e., counts greater than some threshold
$k$) are reliable. Making tihs assumption below formula is used:

$$\begin{aligned}
c^* &= \begin{cases}
c & \text{for } c > k \\
\frac{k+1}{N_k + 1} \cdot \frac{1}{1 - \frac{k+1}{N_k + 1}} & \text{for } 1 < c \leq k
\end{cases}
\end{aligned}$$

where $N_k$ is the total number of counts up to and including $k$.

# Probability of Spell and Markov Assumption

The probabilities of syllables are calculated using Bayes' theorem in
the following manner:

For unigrams, the probability of a syllable $s$ occurring is computed
as:
$$P(s) = \frac{{\text{{frequency of }} s}}{{\text{{total number of unigrams}}}}$$

For bigrams, given the previous syllable $p$ and the current syllable
$c$, the probability is calculated as:
$$P(c|p) = \frac{{\text{{frequency of }} (p, c)}}{{\text{{frequency of }} p}}$$

For trigrams, considering the two previous syllables $p_1$ and $p_2$ and
the current syllable $c$, the probability is determined as:
$$P(c|p_1,p_2) = \frac{{\text{{frequency of }} (p_1, p_2, c)}}{{\text{{frequency of }} (p_1, p_2)}}$$

Sentence probabilities are calculated using the Markov assumption, which
makes simplifying assumptions about the dependence between syllables to
enable efficient computation. To prevent underflow during these
calculations, the sum of logs is used.

# Perplexity

## Unigram Perplexity

The unigram perplexity, which considers only the individual syllables,
is calculated as follows:

$$\text{Perplexity} = \exp\left(-\frac{1}{N} \sum_{i=1}^N \log P(s_i)\right)$$

where:

$N$ is the number of syllables in the sequence.

$s_i$ is the $i$th syllable in the sequence.

$P(s_i)$ is the probability of the $i$th syllable occurring.

## Bigram Perplexity

The bigram perplexity considers the previous syllable when predicting
the next syllable. It is calculated as follows:

$$\text{Perplexity} = \exp\left(-\frac{1}{N-1} \sum_{i=2}^N \log P(s_i | s_{i-1})\right)$$

where:

$N$ is the number of syllables in the sequence.

$s_i$ is the $i$th syllable in the sequence.

$s_{i-1}$ is the $(i-1)$th syllable in the sequence.

$P(s_i | s_{i-1})$ is the probability of the $i$th syllable occurring
given the $(i-1)$th syllable.

## Trigram Perplexity

The trigram perplexity considers the two previous syllables when
predicting the next syllable. It is calculated as follows:

$$\text{Perplexity} = \exp\left(-\frac{1}{N-2} \sum_{i=3}^N \log P(s_i | s_{i-1}, s_{i-2})\right)$$

where:

$N$ is the number of syllables in the sequence.

$s_i$ is the $i$th syllable in the sequence.

$s_{i-1}$ is the $(i-1)$th syllable in the sequence.

$s_{i-2}$ is the $(i-2)$th syllable in the sequence.

$P(s_i | s_{i-1}, s_{i-2})$ is the probability of the $i$th syllable
occurring given the $(i-1)$th and $(i-2)$th syllables.

# Results

## Ngram Frequencies Table
First 20 Entries of Unigram, Bigram, and Trigram Frequencies

| Unigram       | Bigram             | Trigram                   |
|---------------|--------------------|----------------------------|
| cen: 72985    | cen, giz: 1781     | cen, giz, `</w>`: 1728    |
| giz: 11010    | giz, `</w>`: 2213  | giz, `</w>`, han: 712     |
| `</w>`: 45631791 | `</w>`, han: 18565 | `</w>`, han, `</w>`: 7209 |
| han: 60574    | han, `</w>`: 29502 | han, `</w>`, cen: 22      |
| ceng: 22      | `</w>`, cen: 46187 | `</w>`, cen, giz: 1350    |
| his: 12966    | `</w>`, ceng: 20   | han, `</w>`, ceng: 0.366  |
| khan: 522     | ceng, his: 0.414   | `</w>`, ceng, his: 0.366  |
| çing: 152     | his, `</w>`: 2685 | ceng, his, `</w>`: 0.366 |
| gis: 1534     | `</w>`, khan: 478  | his, `</w>`, khan: 4.292  |
| ha: 683736    | khan, `</w>`: 470  | `</w>`, khan, `</w>`: 428 |
| an: 358369    | `</w>`, çing: 99   | khan, `</w>`, çing: 0.366 |
| ya: 1985060   | çing, gis: 1.243   | `</w>`, çing, gis: 1.262  |
| da: 2570363   | gis, `</w>`: 536  | çing, gis, `</w>`: 1.262 |
| do: 244733    | `</w>`, ha: 360493 | gis, `</w>`, ha: 3.284    |
| ğum: 10921    | ha, an: 47        | `</w>`, ha, an: 16        |
| a: 2106725    | an, `</w>`: 38434 | ha, an, `</w>`: 44       |
| dıy: 20423    | `</w>`, ya: 944971 | an, `</w>`, ya: 230      |
| la: 3067824   | ya, `</w>`: 704732 | `</w>`, ya, `</w>`: 112035 |
| te: 1103320   | `</w>`, da: 798956 | ya, `</w>`, da: 96060    |
| mu: 169417    | da, `</w>`: 1835246 | `</w>`, da, `</w>`: 448995 |


### Perplexity
You can find the perplexity results of below sentences in the Table:

1. yerine kukla konumunda kalacak sultan musa han geçti
2. kotlin kotlin java sanal makinesi jvm üzerinde çalışan ve ayrıca javascript kaynak koduna derlenebilir statik tipli bir programlama dilidir
3. kotlin apple ın swift diline benzemektedir
4. yarışmadan önce mevcut dünya ve şampiyona rekorları aşağıdaki gibiydi
5. eleme serileri temmuz da saat da gerçekleştirildi
6. kalem harici olarak bir kapaklı silindirik bir kapta saklanır
7. windows marketplace nin mobil versiyonu olan windows marketplace for mobile uygulamalar mağazası vardır
8. ekim de piyasaya çıktı
9. bloğu ikinci bitiren takımlar finaliste karar verilmesi için yarı finale kalmıştır
10. aynı zamanda üç roman filmin üç konusuna da odaklanmaktadır
11. soğan kubbesi sadece rus mimarisinde değil aynı zamanda yaygın olarak hint gotik mimarisini etkilemeye devam eden babür mimarisinde de kullanılmıştır
12. yahudiler ortalığı karıştırmak adına sünnetli olan türkleri almanlara ihbar eder
13. böylelikle yahudiler den sonra türkler de katliama uğrar
14. bunu takiben ödül için beş aday belirlemek için gizli oy kullanılır

#### Perplexities for Sample Sentences

| Sentence | Unigram Perplexity   | Bigram Perplexity | Trigram Perplexity |
|----------|----------------------|-------------------|---------------------|
| 1        | 332771925.7920939    | 29.989            | 19.483              |
| 2        | 332771925.79210925   | 36.118            | 16.964              |
| 3        | 332771925.79210925   | 36.637            | 20.396              |
| 4        | 332771925.7920939    | 17.705            | 8.446               |
| 5        | 332771925.7920939    | 13.616            | 8.024               |
| 6        | 332771925.79210097   | 34.024            | 14.967              |
| 7        | 332771925.79210216   | 31.842            | 13.499              |
| 8        | 332771925.7921057    | 24.965            | 5.422               |
| 9        | 332771925.79210806   | 16.766            | 10.761              |
| 10       | 332771925.79210806   | 16.638            | 9.919               |
| 11       | 332771925.79210454   | 22.375            | 9.463               |
| 12       | 332771925.7920939    | 25.364            | 14.990              |
| 13       | 332771925.7920939    | 25.689            | 12.547              |
| 14       | 332771925.7920939    | 23.140            | 11.158              |

### Random Sentence Generation

Randomly generated sentences using 5 syllables and weighted probabilities can be found in the Table

#### Generated Sentences and Postprocessed Versions

| Type    | Sentence                               | Postprocessed        |
|---------|----------------------------------------|----------------------|
| Unigram | `</s> o da ma çe i </s>`               | "odamaçei"          |
| Bigram  | `</s> se çim de </w> tu </s>`          | "seçimde tu"        |
| Trigram | `</s> nin sun </w> si cil </s>`        | "ninsun sicil"      |
| Unigram | `</s> sın son bey al lı </s>`          | "sınsonbeyallı"     |
| Bigram  | `</s> müs lü </w> do </w> </s>`       | "müslü do "         |
| Trigram | `</s> tü ke ti </w> ve </s>`          | "tüketi ve"         |
| Unigram | `</s> şiş bi kap di ra </s>`          | "şişbikapdira"      |
| Bigram  | `</s> sa ray lar da nır </s>`         | "saraylardanır"     |
| Trigram | `</s> sert tir </w> ve </w> </s>`    | "serttir ve"        |
| Unigram | `</s> yaş rül zı rı ya </s>`          | "yaşrülzırıya"      |
| Bigram  | `</s> meş hur baş la rak </s>`       | "meşhurbaşlarak"    |
| Trigram | `</s> mes cit </w> dö nem </s>`      | "mescit dönem"      |
| Unigram | `</s> tüm pı nın sı ma </s>`         | "tümpınınsıma"      |
| Bigram  | `</s> bod rum la rı </w> </s>`      | "bodrumları "       |
| Trigram | `</s> sü rün gen ler den </s>`       | "sürüngenlerden"    |
