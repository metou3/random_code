import json
import string
import random
import time
import pandas as pd
import random
import user_activities


def load_user_database():
    return pd.read_csv("user_database.csv", index_col=0)


def save_user_database(df):
    df.to_csv("user_database.csv")
    return True


def check_user(user_id):
    df = load_user_database()
    if user_id in df["id"].to_list():
        return True
    else:
        return False


def get_user(user_id):
    if check_user(user_id):
        df = load_user_database()
        df_user = df[df["id"] == user_id]
        return df_user.iloc[0]
    else:
        return False


def add_user(user_id, email, name, photo_url, language, pro):
    if check_user(user_id) is False:
        df = load_user_database()
        df = df.append({"id": user_id, "email": email, "name": name, "photo_url": photo_url,
                        "language": language, "pro": pro}, ignore_index=True)
        save_user_database(df)
        return "new_acc_created"
    else:
        return "already_created"


def become_pro(user_id):
    if check_user(user_id) is True:
        df = load_user_database()
        df.loc[df["id"] == user_id, ["pro"]] = 1
        print(df)
        save_user_database(df)
        return "become_pro"
    else:
        return "not_valid_user"


def cancel_pro(user_id):
    if check_user(user_id) is True:
        df = load_user_database()
        df.loc[df["id"] == user_id, ["pro"]] = 0
        print(df)
        save_user_database(df)
        return "cancel_pro"
    else:
        return "not_valid_user"


def is_pro(user_id):
    if check_user(user_id) is True:
        df = load_user_database()
        if df.query("id==@user_id")["pro"].iloc[0] == 1:
            return {"pro": True}
        else:
            return {"pro": False}
    else:
        return "not_valid_user"


def id_generator(size=15, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def load_mydict():
    with open("mydict.txt", "r") as f:
        mydict = json.loads(f.read())
    return mydict


def save_mydict(mydict):
    with open("mydict.txt", "w") as f:
        f.write(json.dumps(mydict))
    return "saved"


def add_post_id(post_id):
    mydict = load_mydict()
    if post_id not in mydict.keys():
        t_likes = random.randint(20, 300)
        t_dislikes = int(t_likes * random.randint(1, 10) / 100) + 1
        t_views = int(t_likes*1000/random.randint(3, 100)) + 1
        mydict[post_id] = {
            "likes": [],
            "dislikes": [],
            "comments": {},
            "shares": [],
            "views": [],
            "t_comments": 0,
            "t_likes": t_likes,
            "t_dislikes": t_dislikes,
            "t_views": t_views,
            "t_shares": 0
        }
        save_mydict(mydict)
    else:
        pass


def view_post(d):
    post_id = d["post_id"]
    user_id = d["user_id"]
    epoch_time = time.time()
    add_post_id(post_id)
    mydict = load_mydict()
    data = get_user(user_id)
    views = mydict[post_id]["views"]
    views.append({"user_id": user_id, "time": epoch_time})
    mydict[post_id]["t_views"] = mydict[post_id]["t_views"] + 1
    save_mydict(mydict)
    d["time"] = epoch_time
    user_activities.view_post(d)
    return {"view": mydict[post_id]["t_views"], "like": mydict[post_id]["t_likes"],
            "dislike": mydict[post_id]["t_dislikes"], "time": epoch_time}


def share_post(d):
    post_id = d["post_id"]
    user_id = d["user_id"]
    epoch_time = time.time()
    add_post_id(post_id)
    mydict = load_mydict()
    data = get_user(user_id)
    shares = mydict[post_id]["shares"]
    shares.append({"user_id": user_id, "time": epoch_time})
    mydict[post_id]["t_shares"] = mydict[post_id]["t_shares"] + 1
    save_mydict(mydict)
    d["time"] = epoch_time
    user_activities.share_post(d)
    return {"share": mydict[post_id]["t_shares"], "time": epoch_time}


def like_post(d):
    post_id = d["post_id"]
    user_id = d["user_id"]
    epoch_time = time.time()
    add_post_id(post_id)
    mydict = load_mydict()
    data = get_user(user_id)
    likes = mydict[post_id]["likes"]
    user = True
    if len(likes) > 0:
        for i in range(len(likes)):
            if user_id == likes[i]["user_id"]:
                likes.pop(i)
                mydict[post_id]["t_likes"] -= 1
                user = False
                break
    if user:
        likes.append({"user_id": user_id,
                        "user_email": data["email"],
                        "user_name": data["name"],
                        "user_photo_url": data["photo_url"],
                        "time": epoch_time})
        mydict[post_id]["t_likes"] += 1
    dislikes = mydict[post_id]["dislikes"]
    if len(dislikes) > 0:
        for i in range(len(dislikes)):
            if user_id == dislikes[i]["user_id"]:
                dislikes.pop(i)
                mydict[post_id]["t_dislikes"] -= 1
                break
    print("likes", mydict[post_id]["t_likes"])
    print("dislikes", mydict[post_id]["t_dislikes"])
    save_mydict(mydict)
    d["time"] = epoch_time
    user_activities.like_post(d)
    return {"like": mydict[post_id]["t_likes"], "dislike": mydict[post_id]["t_dislikes"], "user": user, "time": epoch_time}


def dislike_post(d):
    post_id = d["post_id"]
    user_id = d["user_id"]
    epoch_time = time.time()
    add_post_id(post_id)
    mydict=load_mydict()
    data = get_user(user_id)
    dislikes = mydict[post_id]["dislikes"]
    user = True
    if len(dislikes) > 0:
        for i in range(len(dislikes)):
            if user_id == dislikes[i]["user_id"]:
                dislikes.pop(i)
                mydict[post_id]["t_dislikes"] -= 1
                user = False
                break
    if user:
        dislikes.append({"user_id": user_id,
                        "user_email": data["email"],
                        "user_name": data["name"],
                        "user_photo_url": data["photo_url"],
                        "time": epoch_time})
        mydict[post_id]["t_dislikes"] += 1

    likes = mydict[post_id]["likes"]
    if len(likes) > 0:
        for i in range(len(likes)):
            print("user_id",user_id)
            print("check_user_id",likes[i]["user_id"])
            if user_id == likes[i]["user_id"]:
                likes.pop(i)
                mydict[post_id]["t_likes"] -= 1
                break
    print("likes", mydict[post_id]["t_likes"])
    print("dislikes", mydict[post_id]["t_dislikes"])
    save_mydict(mydict)
    d["time"] = epoch_time
    user_activities.dislike_post(d)
    return {"like": mydict[post_id]["t_likes"], "dislike": mydict[post_id]["t_dislikes"], "user": user, "time": epoch_time}


def comment_post(d):
    post_id = d["post_id"]
    user_id = d["user_id"]
    comment = d["comment"]
    add_post_id(post_id)
    mydict = load_mydict()
    data = get_user(user_id)
    epoch_time = time.time()
    comment_id = id_generator()
    if post_id in mydict.keys():
        mydict[post_id]["comments"][comment_id] = {
            "user_id": user_id,
            "user_email": data["email"],
            "user_name": data["name"],
            "user_photo_url": data["photo_url"],
            "time": epoch_time,
            'likes': [], 'dislikes': [], 'comment': comment, 'comments': {}
        }
        save_mydict(mydict)
        d["time"] = epoch_time
        d["comment_id"] = comment_id
        user_activities.comment_post(d)
        return {"time": epoch_time, "id": comment_id}
    else:
        return False


def like_post_comment(d):
    post_id = d["post_id"]
    user_id = d["user_id"]
    comment_id = d["comment_id"]
    epoch_time = time.time()
    add_post_id(post_id)
    mydict=load_mydict()
    data = get_user(user_id)
    likes=mydict[post_id]["comments"][comment_id]["likes"]
    user = True
    for i in range(len(likes)):
        if user_id == likes[i]["user_id"]:
            likes.pop(i)
            user = False
            break
    dislikes=mydict[post_id]["comments"][comment_id]["dislikes"]
    for i in range(len(dislikes)):
        if user_id == dislikes[i]["user_id"]:
            dislikes.pop(i)
            break
    if user:
        likes.append({"user_id": user_id,
                        "user_email": data["email"],
                        "user_name": data["name"],
                        "user_photo_url": data["photo_url"],
                        "time": epoch_time})
    save_mydict(mydict)
    d["time"] = epoch_time
    user_activities.like_comment_post(d)
    return {"like": len(likes), "dislike": len(dislikes), "user": user, "time": epoch_time}


def dislike_post_comment(d):
    post_id = d["post_id"]
    user_id = d["user_id"]
    comment_id = d["comment_id"]
    epoch_time = time.time()
    add_post_id(post_id)
    mydict = load_mydict()
    data = get_user(user_id)
    user = True
    dislikes = mydict[post_id]["comments"][comment_id]["dislikes"]
    for i in range(len(dislikes)):
        if user_id == dislikes[i]["user_id"]:
            dislikes.pop(i)
            user = False
            break
    likes = mydict[post_id]["comments"][comment_id]["likes"]
    for i in range(len(likes)):
        if user_id == likes[i]["user_id"]:
            likes.pop(i)
            break
    if user:
        dislikes.append({"user_id": user_id,
                        "user_email": data["email"],
                        "user_name": data["name"],
                        "user_photo_url": data["photo_url"],
                        "time": epoch_time})
    save_mydict(mydict)
    d["time"] = epoch_time
    user_activities.dislike_comment_post(d)
    return {"like": len(likes), "dislike": len(dislikes), "user": user, "time": epoch_time}


def reply_comment(d):
    post_id = d["post_id"]
    user_id = d["user_id"]
    comment_id = d["comment_id"]
    comment = d["comment"]
    add_post_id(post_id)
    mydict = load_mydict()
    data = get_user(user_id)
    epoch_time = time.time()
    reply_comment_id = id_generator()
    mydict[post_id]["comments"][comment_id]["comments"][reply_comment_id] = {
        "user_id": user_id,
        "user_email": data["email"],
        "user_name": data["name"],
        "user_photo_url": data["photo_url"],
        "time": epoch_time,
        'likes': [], 'dislikes': [], 'comment': comment
    }
    save_mydict(mydict)
    d["time"] = epoch_time
    d["reply_comment_id"] = reply_comment_id
    user_activities.like_comment_post(d)
    return {"time": epoch_time, "id": reply_comment_id}


def like_reply_comment(d):
    post_id = d["post_id"]
    user_id = d["user_id"]
    comment_id = d["comment_id"]
    reply_comment_id = d["reply_comment_id"]
    epoch_time = time.time()
    mydict = load_mydict()
    data = get_user(user_id)
    likes = mydict[post_id]["comments"][comment_id]["comments"][reply_comment_id]["likes"]
    user = True
    for i in range(len(likes)):
        if user_id == likes[i]["user_id"]:
            likes.pop(i)
            user = False
            break
    dislikes=mydict[post_id]["comments"][comment_id]["comments"][reply_comment_id]["dislikes"]
    for i in range(len(dislikes)):
        if user_id == dislikes[i]["user_id"]:
            dislikes.pop(i)
            break
    if user:
        likes.append({"user_id": user_id,
                "user_email" : data["email"],
                "user_name" : data["name"],
                "user_photo_url" : data["photo_url"],
                "time" : epoch_time})
    save_mydict(mydict)
    d["time"] = epoch_time
    user_activities.like_reply_comment(d)
    return {"like": len(likes), "dislike": len(dislikes), "user": user, "time": epoch_time}


def dislike_reply_comment(d):
    post_id = d["post_id"]
    user_id = d["user_id"]
    comment_id = d["comment_id"]
    reply_comment_id = d["reply_comment_id"]
    epoch_time = time.time()
    add_post_id(post_id)
    mydict = load_mydict()
    data =get_user(user_id)
    dislikes = mydict[post_id]["comments"][comment_id]["comments"][reply_comment_id]["dislikes"]
    user = True
    for i in range(len(dislikes)):
        if user_id == dislikes[i]["user_id"]:
            dislikes.pop(i)
            user = False
            break
    likes = mydict[post_id]["comments"][comment_id]["comments"][reply_comment_id]["likes"]
    for i in range(len(likes)):
        if user_id == likes[i]["user_id"]:
            likes.pop(i)
            break
    if user:
        dislikes.append({"user_id": user_id,
                        "user_email": data["email"],
                        "user_name": data["name"],
                        "user_photo_url": data["photo_url"],
                        "time": epoch_time})
    save_mydict(mydict)
    d["time"] = epoch_time
    user_activities.dislike_reply_comment(d)
    return {"like": len(likes), "dislike": len(dislikes), "user": user, "time": epoch_time}
