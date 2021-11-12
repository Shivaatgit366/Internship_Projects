import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stopwords_ready = False
punkwords_ready = False


def download_stopwords_punkwords():
    global stopwords_ready, punkwords_ready
    if stopwords_ready == False or punkwords_ready == False:
        nltk.download("stopwords")
        nltk.download("punkt")
        stopwords_ready = True
        punkwords_ready = True


def remove_tags(html_content):
    # parse html content
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()
    # for data in soup(["style", "script"]):
    #     # remove tags
    #     data.decompose()
    # return "".join(soup.stripped_strings)


def stop_words_remover(text_content):  # returns a list of filtered words.
    # download stopwords data
    download_stopwords_punkwords()

    # to keep all the stopwords in a set.
    stop_words_set = set(stopwords.words("english"))

    # to get every word in a list.
    word_tokens = word_tokenize(text_content)

    # all words present in "word tokens" which are not in "stopwords" are the filtered words.
    filtered_content = []

    for word in word_tokens:
        if word.lower() not in stop_words_set:
            filtered_content.append(word)
    return filtered_content


def punc_remover_string(content):
    punc_string = """!#$%&\'()*+,"-./:;<=>?@[\\]’^_`{|}~"""
    for char in content:
        if char in punc_string:
            content = content.replace(char, "")
    return content


def punc_remover_list(content_list):
    filtered_list = []
    for item in content_list:
        filtered_list.append(punc_remover_string(item))  # to filter punctuations from every list item.
    filtered_list = [i for i in filtered_list if i]  # to remove empty string items from a list.
    return filtered_list


def clean_text(content):  # returns a list with filtered words.
    tags_removed_text = remove_tags(content)
    cleaned_list = stop_words_remover(tags_removed_text)
    final_list = punc_remover_list(cleaned_list)
    return final_list


if __name__ == '__main__':
    y = """As shown in the output images, the new output doesn’t have the passed columns. Those values were
        dropped since axis was set equal to 1 and the changes were made in the original data frame since
        inplace was True."""
    print(clean_text(y))

