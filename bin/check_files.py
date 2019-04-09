import csv
import os


def check_files():
    print('Checking files')

    with open('output/races.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if(not(os.path.isfile(row['filename']))):
                print(row)


if __name__ == "__main__":
    check_files()
