import os
import json
import pandas as pd
import variables as var
import glob
import csv

# This file is used to convert the raw result data into csv and xlsx files


def write_line(writer, row, places, users):  # function to convert the data to csv
    line = []
    line.append(row['author_id'])
    user = users.loc[users['id'] == line[0]]
    line += user['name'].tolist()
    line += user['username'].tolist()
    line += user['verified'].tolist()
    line.append(row['created_at'])
    line.append(row['id'])
    line.append(row.get('in_reply_to_user_id'))
    line.append(row['public_metrics']['like_count'])
    line.append(row['public_metrics']['quote_count'])
    line.append(row['public_metrics']['reply_count'])
    line.append(row['public_metrics']['retweet_count'])
    if isinstance(row.get('geo'), dict):
        line.append(row['geo'].get('place_id'))
        place = places.loc[places['id'] == line[-1]]
        line += place['country'].tolist()
        line += place['country_code'].tolist()
        line += place['full_name'].tolist()
        line += place['place_type'].tolist()
        if row['geo'].get('coordinates') is not None:
            line.append(row['geo']['coordinates']['coordinates'])
        else:
            line += [None]
    else:
        line += [None, None, None, None, None, None]
    line.append(row['text'])
    writer.writerow(line)


folder_name = var.start[0:10] + "_" + var.end[0:10]  # year-mo-da_year-mo-da
path = var.path + folder_name  # result/year-mo-da_year-mo-da
begin = True
FILENAME = os.path.join(path, folder_name)
with open(FILENAME + '.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['author_id', 'name', 'username', 'verified', 'created_at', 'id', 'in_reply_to_user_id',
                     'like_count', 'quote_count', 'reply_count', 'retweet_count', 'place_id', 'country',
                     'country_code', 'full_name', 'place_type', 'coordinates',
                     'text'])  # headers
    print(path)
    # result/0.txt, result/1.txt, result/2.txt ...
    for filename in glob.glob(path + "/*.txt"):
        print(filename)
        with open(filename) as file:
            data = json.load(file)
        # separate dataframes
        df = pd.DataFrame(data['data'])
        places = pd.DataFrame(data['includes'].get('places'))
        users = pd.DataFrame(data['includes']['users'])
        print(users)
        for index, row in df.iterrows():  # for each row convert dataframes to csv
            write_line(writer, row, places, users)
# Reading the csv file
pcsv = pd.read_csv(FILENAME + '.csv')

# saving xlsx file
excel = pd.ExcelWriter(FILENAME + '.xlsx')
pcsv.to_excel(excel, index=False, engine='xlsxwriter')

excel.save()

print('done')
