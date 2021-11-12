import pandas as pd
from requirements import cleaning_text as ct

full_positive_list = []
full_negative_list = []


def fill_positive_negative_list():
    global full_positive_list, full_negative_list

    # if not full_positive_list or not full_negative_list, then replace the variables.
    if bool(full_positive_list) == False or bool(full_negative_list) == False:
        filepath = "LoughranMcDonald_MasterDictionary_2020.csv"

        dataframe = pd.read_csv(filepath)

        dataframe.drop(["Seq_num", "Word Count", "Word Proportion", "Average Proportion", "Std Dev", "Doc Count",
                        "Uncertainty", "Litigious", "Strong_Modal",
                        "Weak_Modal", "Constraining", "Complexity", "Syllables", "Source"], axis=1, inplace=True)
        dataframe_new = dataframe[dataframe["Positive"] == 2009]
        dataframe_new2 = dataframe[dataframe["Negative"] == 2009]

        full_positive_list = dataframe_new["Word"].tolist()
        full_negative_list = dataframe_new2["Word"].tolist()


def positive_score_returner(content_list):
    fill_positive_negative_list()
    positive_word_count = 0
    for word in content_list:
        if word.upper() in full_positive_list:
            positive_word_count = positive_word_count + 1
    return positive_word_count


def negative_score_returner(content_list):
    fill_positive_negative_list()
    negative_word_count = 0
    for word in content_list:
        if word.upper() in full_negative_list:
            negative_word_count = negative_word_count + 1
    return negative_word_count


def polarity_score_returner(p_score, n_score):
    polarity_score = (p_score - n_score) / ((p_score + n_score) + 0.000001)
    return polarity_score


def subjectivity_score_returner(p_score, n_score, wordcount):
    subjectivity_score = (p_score + n_score) / (wordcount + 0.000001)
    return subjectivity_score


def positive_word_proportion(text):
    cleaned_text_list = ct.clean_text(text)
    word_count = len(cleaned_text_list)
    p_score = positive_score_returner(cleaned_text_list)
    pos_word_proportion = p_score / word_count
    return pos_word_proportion


def negative_word_proportion(text):
    cleaned_text_list = ct.clean_text(text)
    word_count = len(cleaned_text_list)
    n_score = negative_score_returner(cleaned_text_list)
    neg_word_proportion = n_score / word_count
    return neg_word_proportion


if __name__ == '__main__':
    list_of_words = ['ABUNDANCE', 'ABUNDANT', 'ACCLAIMED', 'ACCOMPLISH', 'ACCOMPLISHED',
                     'ACCOMPLISHES', 'AGGRAVATION', 'AGGRAVATIONS']
    print(positive_score_returner(list_of_words))
    print(full_positive_list)
    print(negative_score_returner(list_of_words))
    print(full_negative_list)
