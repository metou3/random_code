import requests
import pandas as pd


df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                    'B': ['B0', 'B1', 'B2', 'B3'],
                    'C': ['C0', 'C1', 'C2', 'C3'],
                    'D': ['D0', 'D1', 'D2', 'D3']},
                   index=[0, 1, 2, 3])

df2 = pd.DataFrame({'A': ['A3', 'A5', 'A6', 'A7'],
                    'B': ['B3', 'B3', 'B6', 'B7'],
                    'C': ['C3', 'C5', 'C6', 'C7'],
                    'D': ['D3', 'D5', 'D6', 'D7']},
                   index=[4, 5, 6, 7])


def post_df_update(file_name):
    urls = ["http://192.168.0.26:5006/upload"]
    for url in urls:
        fin = open(file_name, 'rb')
        files = {'file': fin}
        try:
            r = requests.post(url, files=files)
            # print(r.text)
        finally:
            fin.close()
            # os.remove(df_file_name)


file_name = "aaatest.csv"

df2.to_csv(file_name, sep="#")

post_df_update(file_name)
# print(pd.read_csv(file_name, sep="#", index_col=0))