import time
import interaction
import json
import pandas as pd

from dynamic_web import get_df_goodnews
import my_data_adapter


def get_config(l_tag):
    with open('jsconfig/config_'+l_tag+'.json') as json_file:
        data = json.load(json_file)
        return data


def get_basic_list(list_post_id):
    for i in list_post_id:
        interaction.add_post_id(i)
    mydict = interaction.load_mydict()
    data = {}
    for i in list_post_id:
        if i in list(mydict.keys()):
            data[i] = {
                    "t_likes": mydict[i]["t_likes"],
                    "t_dislikes": mydict[i]["t_dislikes"],
                    "t_views": mydict[i]["t_views"],
                    "t_shares": mydict[i]["t_shares"],
                    "t_comments": mydict[i]["t_comments"]
                    }
    return data


def get_notifications_for(user_id):
    with open("notifications.txt", "r") as f:
        n = json.loads(f.read())
        # print("load_done")
        # print(n)
    if user_id in n.keys():
        return n[user_id]
    else:
        return "shit"


def get_comments_of(d):
    post_id = d["post_id"]
    return interaction.load_mydict()[post_id]["comments"]


def add_reaction_to_df(df):
    t_likes = "t_likes"
    t_dislikes = "t_dislikes"
    t_views = "t_views"
    t_shares = "t_shares"
    t_comments = "t_comments"
    cl = list(df.columns)
    list_data = df["url"].to_list()
    # print(df)
    # print(cl)
    # print(list_data)
    basic_list = my_data_adapter.get_basic_list(list_data)
    # print(basic_list)
    list_react = []
    de_columns = [t_likes, t_dislikes, t_views, t_shares, t_comments]
    de = pd.DataFrame(index=range(0, len(df)), columns=de_columns).fillna(0)

    df = pd.concat([df, de], axis=1)
    # print(df.columns)
    # print(df.iloc[10]["likes"])
    for i in range(len(df["url"].to_list())):
        # print(i)
        url = df["url"].iloc[i]
        e = basic_list[url]
        df.at[i, t_likes] = e[t_likes]
        df.at[i, t_dislikes] = e[t_dislikes]
        df.at[i, t_views] = e[t_views]
        df.at[i, t_shares] = e[t_shares]
        df.at[i, t_comments] = e[t_comments]

    return df