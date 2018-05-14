# coding:utf-8 
# import tablib

# zero-based indexing: 0-25, 0-29
ROWNUM = 26
COLUMN = 30

def load_data(file_name = 'script1.csv'):
    data = []
    file = open(file_name, 'r')
    all_lines = file.readlines()
    for line in all_lines:
        tmp = line.strip().split(',')
        data.append(tmp)     
    return data

if __name__ == "__main__":
    # load landform - a 26*30 matrix
    landform = load_data(file_name = 'script1.csv')