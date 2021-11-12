import csv
import sys
import requests
from requirements import positive_negative_wordlists as ps
import pandas as pd
from requirements import cleaning_text
from requirements import sentence_count as sc
from requirements import uncertainty_and_constraining as uc


def get_final_url(path):
    # path means the row content in "secfname" column.
    base_url = "https://www.sec.gov/Archives/"
    final_string = base_url + path
    return final_string


def get_file_contents(url):
    x = requests.get(url)
    return x.text


def master_function(input_file):  # any excel file is given as input.
    # entire excel file is saved into dataframe format.
    df = pd.read_excel(input_file, engine='openpyxl', dtype=object, header=None)
    full_list = df.values.tolist()  # every row is converted to a list and these rows are put into another list.

    body = []  # except the fields row, this list contains all the lists of rows. It is a list of lists.
    row_count = 1
    header_row = []

    # loop through the list of rows.
    for row in full_list:
        if row_count == 1:  # row contains fields.
            header_row = row[:]
            header_row.append("POSITIVE SCORE")
            header_row.append("NEGATIVE SCORE")
            header_row.append("POLARITY SCORE")
            header_row.append("SUBJECTIVITY SCORE")
            header_row.append("AVERAGE SENTENCE LENGTH")
            header_row.append("PERCENTAGE OF COMPLEX WORDS")
            header_row.append("FOG INDEX")
            header_row.append("COMPLEX WORD COUNT")
            header_row.append("WORD COUNT")
            header_row.append("UNCERTAINTY SCORE")
            header_row.append("CONSTRAINING SCORE")
            header_row.append("POSITIVE WORD PROPORTION")
            header_row.append("NEGATIVE WORD PROPORTION")
            header_row.append("UNCERTAINTY WORD PROPORTION")
            header_row.append("CONSTRAINING WORD PROPORTION")
            header_row.append("TOTAL NUMBER OF CONSTRAINING WORDS FOR WHOLE REPORT")

        else:
            # obtaining the full url.
            secf_name = row[-1]  # content of secfname column.
            full_url = get_final_url(secf_name)

            # keep the content of the web page.
            text_data = get_file_contents(full_url)

            # clean the text file and gives a list of words.
            cleaned_text = cleaning_text.clean_text(text_data)  # cleaned_text is a list with filtered words.
            word_count = len(cleaned_text)

            # add the variable values to the result list one by one.
            positive_score = ps.positive_score_returner(cleaned_text)
            negative_score = ps.negative_score_returner(cleaned_text)
            polarity_score = ps.polarity_score_returner(positive_score, negative_score)
            subjectivity_score = ps.subjectivity_score_returner(positive_score, negative_score, word_count)
            average_sentence_length = sc.average_sentence_length(text_data)
            percentage_of_complex_words = sc.percentage_of_complex_words(text_data)
            fog_index = sc.fog_index_returner(text_data)
            complex_word_count = sc.complex_word_count_returner(text_data)
            uncertainty_score = uc.uncertainty_score_returner(cleaned_text)
            constraining_score = uc.constraining_score_returner(cleaned_text)
            positive_word_proportion = ps.positive_word_proportion(text_data)
            negative_word_proportion = ps.negative_word_proportion(text_data)
            uncertainty_word_proportion = uc.uncertainty_word_proportion(text_data)
            constraining_word_proportion = uc.constraining_word_proportion(text_data)

            row_updated = row[:]  # copy of the list "row".
            body.append(row_updated + [positive_score] + [negative_score] +
                        [polarity_score] + [subjectivity_score] + [average_sentence_length] +
                        [percentage_of_complex_words] + [fog_index] + [complex_word_count] + [word_count] +
                        [uncertainty_score] + [constraining_score] + [positive_word_proportion] +
                        [negative_word_proportion] + [uncertainty_word_proportion] +
                        [constraining_word_proportion])

        # if row_count == 5:
        #     break
        print(f"processing row - {row_count}")
        row_count += 1

    # final list contains all the rows as lists.
    final_list = [header_row] + body
    return final_list


if __name__ == "__main__":
    input_filepath = sys.argv[1]  # user gives the file path as an argument.

    complete_list = master_function(input_filepath)

    # writing all the data into a csv file.
    fields = complete_list[0]
    rows = complete_list[1:]

    output_filename = "assignment.csv"

    with open(output_filename, "w") as csvfile:  # csvfile is the file pointer
        csvwriter = csv.writer(csvfile)  # creating a csv writer object

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)
