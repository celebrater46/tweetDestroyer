import tweepy
import pandas as pd
import re
import time

# https://hackmd.io/@drsenri/ry7ohj_rL

# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

consumer_key='**************'
consumer_secret='**************'
access_token_key='**************'
access_token_secret='**************'
data_folder = './twitter_data'

# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.

def destroyTweets(path):
    with open(path) as f:
        datalines = f.readlines()

    regexes = [r'    \"source\".*',
               r'    \"id_str\".*',
               r'    \"created_at\".*',
               r'    \"full_text\".*'
               ]

    colname = ['source', 'id', 'created_at', 'full_text']
    df = pd.DataFrame([], columns=colname)

    for i, regex in enumerate(regexes):
        L = []
        for line in datalines:
            match_obj = re.match(regex, line)
            if match_obj:
                L.append(match_obj.group())
        df[colname[i]] = pd.Series(L)

    # データ型の整形
    df["created_at"] = df["created_at"].str.replace('"created_at" : ', '').str.replace('"', '').str.replace(',$', '').astype(str)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["id"] = df["id"].str.replace('"id_str" : ', "").str.replace('"', '').str.replace(' ', '').str.replace(',', '').astype(str)

    return df

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    hoge = destroyTweets(f"{data_folder}/tweet.js")
    fuga = destroyTweets(f"{data_folder}/tweet-part1.js")
    df = pd.concat([hoge, fuga])
    # Extract tweets to be erased
    since = (df["created_at"].apply(lambda x: x.year) >= 2010)
    until = (df["created_at"].apply(lambda x: x.year) <= 2018) & (df["created_at"].apply(lambda x: x.month) <= 6)
    df_del = df.loc[since & until, :]

    deleted_id = []
    for id_ in df_del["id"]:
        print("Destroying status:", id_)
        try:
            api.get_status(id_)
        except:
            print("No status for", id_)
        else:
            api.destroy_status(id_)
            print("successed")
        time.sleep(5.2)
        deleted_id.append(id_)

    with open("./output/deleted_id4.txt", "w") as f:
        f.writelines("\n".join(deleted_id))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
