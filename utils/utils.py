import csv
import sys

def parse_csv_to_data(file_name, freezer_id):
    X = []
    Y = []

    csv_reader = csv.reader(open(file_name, "r"))
    line_count = 0
    for row in csv_reader:
        line_count += 1
        if line_count == 1:
            continue

        row_id = int(row[0])
        if row_id != freezer_id:
            if row_id > freezer_id: break
            else: continue

        X.append([float(row[2]), int(row[4])]) #, int(row[5]), int(row[6]), int(row[7])])
        Y.append(row[3] == 'True')

    return X, Y

def program_error(message: str):
    print(message)
    sys.exit(0)