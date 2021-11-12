import pandas as pd
from requirements import cleaning_text as ct


uncertainty_words_list = []
constraining_words_list = []


def fill_uncertainty_constraining_lists():
    global uncertainty_words_list, constraining_words_list

    # if not uncertainty_words_list or not constraining_word_list, then replace the variables.
    if bool(uncertainty_words_list) == False or bool(constraining_words_list) == False:
        filepath_uncertainty = "uncertainty_dictionary.xlsx"
        filepath_constraining = "constraining_dictionary.xlsx"

        dataframe_for_uncertainty = pd.read_excel(filepath_uncertainty)
        dataframe_for_constraining = pd.read_excel(filepath_constraining)

        uncertainty_words_list = dataframe_for_uncertainty["Word"].tolist()
        constraining_words_list = dataframe_for_constraining["Word"].tolist()


def uncertainty_score_returner(content_list):
    fill_uncertainty_constraining_lists()
    uncertainty_word_count = 0
    for word in content_list:
        if word.upper() in uncertainty_words_list:
            uncertainty_word_count = uncertainty_word_count + 1
    return uncertainty_word_count


def constraining_score_returner(content_list):
    fill_uncertainty_constraining_lists()
    constraining_word_count = 0
    for word in content_list:
        if word.upper() in constraining_words_list:
            constraining_word_count = constraining_word_count + 1
    return constraining_word_count


def uncertainty_word_proportion(text):
    cleaned_text_list = ct.clean_text(text)
    word_count = len(cleaned_text_list)
    uncertainty_score = uncertainty_score_returner(cleaned_text_list)
    uncertain_word_proportion = uncertainty_score / word_count
    return uncertain_word_proportion


def constraining_word_proportion(text):
    cleaned_text_list = ct.clean_text(text)
    word_count = len(cleaned_text_list)
    constrain_score = constraining_score_returner(cleaned_text_list)
    constrain_word_proportion = constrain_score / word_count
    return constrain_word_proportion

