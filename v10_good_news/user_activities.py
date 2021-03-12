import pandas as pd


# def init_df():
#     df = pd.DataFrame(columns=["user_id", "action", "time", "post_id", "comment_id", "reply_comment_id", "comment"])
#     save_df(df)


def load_df():
    return pd.read_csv("user_activities.csv", index_col=0)


def save_df(df):
    df.to_csv("user_activities.csv")


def view_post(d):
    df = load_df()
    df = df.append({
        "user_id": d["user_id"],
        "action": "view_post",
        "time": d["time"],
        "post_id": d["post_id"]
    }, ignore_index=True)
    save_df(df)
    del df


def share_post(d):
    df = load_df()
    df = df.append({
        "user_id": d["user_id"],
        "action": "share_post",
        "time": d["time"],
        "post_id": d["post_id"]
    }, ignore_index=True)
    save_df(df)
    del df


def like_post(d):
    df = load_df()
    df = df.append({
        "user_id": d["user_id"],
        "action": "like_post",
        "time": d["time"],
        "post_id": d["post_id"]
    }, ignore_index=True)
    save_df(df)
    del df


def dislike_post(d):
    df = load_df()
    df = df.append({
        "user_id": d["user_id"],
        "action": "dislike_post",
        "time": d["time"],
        "post_id": d["post_id"]
    }, ignore_index=True)
    save_df(df)
    del df


def comment_post(d):
    df = load_df()
    df = df.append({
        "user_id": d["user_id"],
        "action": "comment_post",
        "time": d["time"],
        "post_id": d["post_id"],
        "comment_id": d["comment_id"],
        "comment": d["comment"]
    }, ignore_index=True)
    save_df(df)
    del df


def like_comment_post(d):
    df = load_df()
    df = df.append({
        "user_id": d["user_id"],
        "action": "like_comment_post",
        "time": d["time"],
        "post_id": d["post_id"],
        "comment_id": d["comment_id"]
    }, ignore_index=True)
    save_df(df)
    del df


def dislike_comment_post(d):
    df = load_df()
    df = df.append({
        "user_id": d["user_id"],
        "action": "dislike_comment_post",
        "time": d["time"],
        "post_id": d["post_id"],
        "comment_id": d["comment_id"]
    }, ignore_index=True)
    save_df(df)
    del df


def reply_comment(d):
    df = load_df()
    df = df.append({
        "user_id": d["user_id"],
        "action": "reply_comment",
        "time": d["time"],
        "post_id": d["post_id"],
        "comment_id": d["comment_id"],
        "reply_comment_id": d["reply_comment_id"],
        "comment": d["comment"]
    }, ignore_index=True)
    save_df(df)
    del df


def like_reply_comment(d):
    df = load_df()
    df = df.append({
        "user_id": d["user_id"],
        "action": "like_reply_comment",
        "time": d["time"],
        "post_id": d["post_id"],
        "comment_id": d["comment_id"],
        "reply_comment_id": d["reply_comment_id"]
    }, ignore_index=True)
    save_df(df)
    del df


def dislike_reply_comment(d):
    df = load_df()
    df = df.append({
        "user_id": d["user_id"],
        "action": "dislike_reply_comment",
        "time": d["time"],
        "post_id": d["post_id"],
        "comment_id": d["comment_id"],
        "reply_comment_id": d["reply_comment_id"]
    }, ignore_index=True)
    save_df(df)
    del df
