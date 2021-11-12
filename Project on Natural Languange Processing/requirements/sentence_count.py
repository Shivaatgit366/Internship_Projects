import spacy
from requirements import cleaning_text
from textstat.textstat import textstatistics

spacy_model_ready = False
nlp = None


def load_spacy_model():
    global nlp, spacy_model_ready
    if not spacy_model_ready:
        nlp = spacy.load("en_core_web_sm")
        spacy_model_ready = True


# split the text into sentences. These sentences will be kept as list items.
def break_into_sentences(text):  # returns a list of sentences.
    global nlp
    load_spacy_model()
    doc = nlp(text)
    return list(doc.sents)


# to find the number of sentences in a text content.
def sentence_count_returner(text):
    sentences_list = break_into_sentences(text)
    return len(sentences_list)


# to find the number of words in a text content.
def word_count_returner(text):
    sentences_list = break_into_sentences(text)  # break down the text into sentences list.
    word_count = 0
    for sentence in sentences_list:  # using the double loop, find the number of words in each sentence.
        tokens_list = []
        for token in sentence:
            tokens_list.append(token)
        word_count = word_count + len(tokens_list)
    return word_count


# to find the average sentence length.
def average_sentence_length(content):
    tags_removed_text = cleaning_text.remove_tags(content)
    number_of_words = word_count_returner(tags_removed_text)
    number_of_sentences = sentence_count_returner(tags_removed_text)
    avg_sentence_length = number_of_words / number_of_sentences
    return avg_sentence_length


# we should find the syllable count for the word.
def syllable_count_returner(word):
    return textstatistics().syllable_count(word)


# to find the number of complex/difficult words present in the text.
def complex_word_count_returner(text):
    global nlp
    load_spacy_model()
    doc = nlp(text)
    cleaned_words_list = cleaning_text.clean_text(text)

    # complex/difficult words are those with syllables >= 2.
    # easy_word_set is provide by "textstat" as a list of common words.

    complex_words_set = set()

    for word in cleaned_words_list:
        syllable_count = syllable_count_returner(word)
        if syllable_count >= 2:
            complex_words_set.add(word)
    # return the number of complex/difficult words.
    return len(complex_words_set)


# Percentage of Complex words = the number of complex words / the number of words.
def percentage_of_complex_words(text):  # for any raw text, this function gives the percent of complex words.
    number_of_complex_words = complex_word_count_returner(text)
    cleaned_words_list = cleaning_text.clean_text(text)
    number_of_words = len(cleaned_words_list)
    percent_of_complex_words = number_of_complex_words / number_of_words
    return percent_of_complex_words


# To find the fog index. Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
def fog_index_returner(content):
    avg_sent_len = average_sentence_length(content)
    percent_complex_words = percentage_of_complex_words(content)
    fog_index = 0.4 * (avg_sent_len + percent_complex_words)
    return fog_index
