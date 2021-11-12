import glob
import sys
from tabula import read_pdf
import csv
import os


"""
How to execute the file:-
python pdf_extractor.py /path/to/pdf/folder 

the output csv file will be stored in current working directory.
"""


def file_data_extractor(name_of_file):
    pdf_path = name_of_file
    data_frames = read_pdf(pdf_path, pages="1")
    file_path_csv0 = "0.csv"
    file_path_csv1 = "1.csv"
    data_frames[0].to_csv(file_path_csv0)
    data_frames[1].to_csv(file_path_csv1)

    rows_of_table1 = []

    with open(file_path_csv0, "r") as csvfile0:
        csvreader0 = csv.reader(csvfile0)

        for row_values in csvreader0:
            rows_of_table1.append(row_values)

    resultant_dict1 = dict()

    for row in rows_of_table1:
        if row[2] == "pH":
            resultant_dict1["pH"] = row[3]
        elif row[2] == "Organic Carbon (OC)":
            resultant_dict1["Organic Carbon (OC)"] = row[3]
        elif row[2] == "Available Nitrogen (N)":
            resultant_dict1["Available Nitrogen (N)"] = row[3]
        elif row[2] == "Available Phosphorus (P)":
            resultant_dict1["Available Phosphorus (P)"] = row[3]
        elif row[2] == "Available Potassium (K)":
            resultant_dict1["Available Potassium (K)"] = row[3]

    rows_of_table2 = []

    with open(file_path_csv1, "r") as csvfile1:
        csvreader1 = csv.reader(csvfile1)
        fields_table2 = next(csvreader1)

        for row_values in csvreader1:
            rows_of_table2.append(row_values)

    resultant_dict2 = dict()

    for row in rows_of_table2:
        if row[1] == "Farmer Name":
            resultant_dict2["Farmer Name"] = row[2]
        elif row[1] == "Date of Sample Collection":
            resultant_dict2["Date of Sample Collection"] = row[2]
        elif row[1] == "Geo Position (GPS)":
            lat_long = row[2]
            lat_long_list = lat_long.split()
            for i in range(len(lat_long_list)):
                if lat_long_list[i] == "Latitude":
                    resultant_dict2["Latitude"] = lat_long_list[i + 1]
                elif lat_long_list[i] == "Longitude":
                    resultant_dict2["Longitude"] = lat_long_list[i + 1]

    resultant_dict2["file name"] = pdf_path
    resultant_dict2.update(resultant_dict1)
    os.remove(file_path_csv0)
    os.remove(file_path_csv1)
    return resultant_dict2


if __name__ == '__main__':

    # sys.argv() gives a list of those values which are actually the arguments entered by the user in the command line.

    folder_path = sys.argv[1]
    all_pdf_files = []

    for pdf_file in glob.glob(folder_path + "/*.pdf"):  # gives the list of files in the folder.
        all_pdf_files.append(pdf_file)
    print(all_pdf_files)

    result_list = []

    for index, file_name in enumerate(all_pdf_files, 1):
        result = file_data_extractor(file_name)  # result should be a dictionary with required keys and values.
        result["Sr.No"] = index
        result_list.append(result)
    print(result_list)

    fields = ["Sr.No", "file name", "Farmer Name", "pH", "Organic Carbon (OC)", "Available Nitrogen (N)",
              "Available Phosphorus (P)", "Available Potassium (K)",
              "Latitude", "Longitude", "Date of Sample Collection"]

    cwd = os.getcwd()
    filepath_csv = cwd + os.path.sep + "result.csv"  # os.path.sep gives path separator as per the OS.

    with open(filepath_csv, "w") as final_csv:
        writer = csv.DictWriter(final_csv, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result_list)

