import interaction
import pandas as pd
import json
import os


def load_notifications():
    with open("notifications.txt", "rb") as f:
        return json.load(f)


def save_notifications(file):
    with open("notifications.txt", "w") as f:
        f.write(json.dumps(file))


def is_duplicated_notification(epoch_time):
    if str(epoch_time) in str(load_notifications()):
        return True
    else:
        return False


def get_all_users(from_this):
    new_list = str(from_this).split(",")
    # print("new_list",new_list)
    try:
        # print(new_list)
        list_user = list(
            set([i.split("user_id")[1].replace("'", "").replace(":", "").strip() for i in new_list if "user_id" in i]))
        return list_user
    except Exception as e:
        print(e)
        return None


def people_like_same_post_with(user_id, post_id):
    mydict = interaction.load_mydict()
    likes = mydict[post_id]["likes"]
    if user_id in str(likes):
        # print("likes",likes)
        list_users = get_all_users(mydict[post_id]["likes"])
        # print("list_users",list_users)
        list_users = [i for i in list_users if i != user_id]
        # print("list_users",list_users,len(list_users))
        if len(list_users) > 0:
            return list_users
        else:
            return None
            print("no one like this post, only you are crazy lol")
    else:
        return None
        print("user never liked this post")


def people_comment_same_post_with(user_id, post_id):
    mydict = interaction.load_mydict()
    likes = mydict[post_id]["comments"]
    if user_id in str(likes):
        print("comments", likes)
        list_users = get_all_users(mydict[post_id]["comments"])
        # print("list_users",list_users)
        list_users = [i for i in list_users if i != user_id]
        print("list_users", list_users, len(list_users))
        if len(list_users) > 0:
            return list_users
        else:
            print("no one comments this post, only you are crazy lol")
    else:
        print("user never commented this post")


def people_mention_you(user_id):
    my_dict = interaction.load_mydict()
    tag_user = "@" + user_id
    text = str(my_dict)
    list_mention = []
    if text.find(tag_user) != -1:
        del text
        k = list(my_dict.keys())
        for i in k:
            if str(my_dict[i]).find(tag_user) != -1:
                comments = my_dict[i]["comments"]
                k1 = comments.keys()
                for j in k1:
                    if tag_user in str(comments[j]["comment"]):
                        list_mention.append(comments[j])
        return list_mention
    else:
        return None


# people like your comments
def people_like_your_comments(user_id):
    user_list = []
    my_dict = interaction.load_mydict()
    k = list(my_dict.keys())
    comments = my_dict[k[0]]["comments"]
    k1 = list(comments.keys())
    for i in k:
        comments = my_dict[i]["comments"]
        k1 = comments.keys()
        for j in k1:
            if len(comments[j]) > 0:
                if comments[j]["user_id"] == user_id:
                    likes = comments[j]["likes"]
                    if len(likes) > 0:
                        print("\n", comments[j]["user_id"], ":", comments[j]["comment"], "\n")
                        print("liked by:")
                        for l in range(len(likes)):
                            user = likes[l]["user_id"]
                            epoch_time = likes[l]["time"]
                            user_list.append({"post_id": i, "liked_by": user, "time": epoch_time})
                            print(user)
                reply_of_comment = comments[j]["comments"]
                for m in list(reply_of_comment.keys()):
                    if reply_of_comment[m]["user_id"] == user_id:
                        likes = reply_of_comment[m]["likes"]
                        if len(likes) > 0:
                            print("\n", user_id, ":", reply_of_comment[m]["comment"], "\n")
                            print("liked by:")
                            for l in range(len(likes)):
                                user = likes[l]["user_id"]
                                epoch_time = likes[l]["time"]
                                user_list.append({"post_id": i, "liked_by": user, "time": epoch_time})
                                print(user)
    if len(user_list) > 0:
        return user_list
    else:
        return None


# people like your comment
# people cm same post
# people mention you


def get_users(df, user_id):
    return [i for i in list(set(df["user_id"])) if i != user_id]


def get_user_photo_url(user_id):
    if interaction.check_user(user_id):
        return interaction.load_user_database().query('id == @user_id')['photo_url'].iat[0]
    else:
        return ""


def get_notifications():
    n = load_notifications()
    df = pd.read_csv("user_activities.csv", index_col=0)
    l_users_engaged = list(set(df["user_id"].to_list()))
    for user_id in l_users_engaged:
        d_u = df[df["user_id"] == user_id].reset_index(drop=True)
        print("user_id", user_id, "*" * 99)
        for i in range(len(d_u)):
            action = d_u["action"].iat[i]
            post_id = d_u["post_id"].iat[i]
            try:
                comment_id = d_u["comment_id"].iat[i]
            except:
                comment_id = None
            # print(action, post_id, comment_id)
            try:
                reply_comment_id = d_u["reply_comment_id"].iat[i]
            except:
                reply_comment_id = None
            if action == "comment_post":
                print(action)
                d_like_comment = df.query('action == "like_comment_post" and comment_id == @comment_id')
                users = get_users(d_like_comment, user_id)
                if len(users) > 0 and is_duplicated_notification(max(d_like_comment["time"].to_list())) is False:
                    print("find people who like your comment:")
                    # print(d_like_comment)
                    n[user_id].append(
                        {"id": interaction.id_generator(),
                         "time": max(d_like_comment["time"].to_list()),
                         "url_info": get_url_info(post_id),
                         "users": users,
                         "user_photo_url": get_user_photo_url(users[0]),
                         "action": "like_comment"})
                    print(get_users(d_like_comment, user_id))
                del users
                del d_like_comment
                d_comment_same_post = df.query('action == "comment_post" and post_id == @post_id')
                users = get_users(d_comment_same_post, user_id)
                if len(users) > 0 and is_duplicated_notification(max(d_comment_same_post["time"].to_list())) is False:
                    print("find people also comment same post")
                    # print(d_comment_same_post)
                    print(get_users(d_comment_same_post, user_id))
                    n[user_id].append({"id": interaction.id_generator(),
                                        "time": max(d_comment_same_post["time"].to_list()),
                                       "url_info": get_url_info(post_id),
                                       "users": users,
                                       "user_photo_url": get_user_photo_url(users[0]),
                                       "action": "comment_same_post"})
                del users
                del d_comment_same_post
                d_c = df.dropna(subset=['comment'])
                d_c = d_c[d_c["comment"].str.contains("@" + user_id)]
                users = get_users(d_c, user_id)
                if len(users) > 0 and is_duplicated_notification(max(d_c["time"].to_list())) is False:
                    print("find people mentioned you")
                    print(d_c)

                    n[user_id].append({"id": interaction.id_generator(),
                                       "time": max(d_c["time"].to_list()),
                                       "url_info": get_url_info(post_id),
                                        "users": users,
                                        "user_photo_url": get_user_photo_url(users[0]),
                                       "action": "mentioned_you"})
                del users
                del d_c
            elif action == "like_post":
                d_comment_same_post = df.query('action == "comment_post" and post_id == @post_id')
                users = get_users(d_comment_same_post, user_id)
                if len(users) > 0 and is_duplicated_notification(max(d_comment_same_post["time"].to_list())) is False:
                    print("find people also comment same post")
                    # print(d_comment_same_post)
                    print(get_users(d_comment_same_post, user_id))
                    n[user_id].append({"id": interaction.id_generator(),
                                       "time": max(d_comment_same_post["time"].to_list()),
                                       "url_info": get_url_info(post_id),
                                       "users": users,
                                       "user_photo_url": get_user_photo_url(users[0]),
                                       "action": "comment_same_post"})
                del users
                del d_comment_same_post
            # find people comment in the post you like
            elif action == "like_comment_post":
                d_comment_same_post = df.query('action == "comment_post" and post_id == @post_id')
                users = get_users(d_comment_same_post, user_id)
                if len(users) > 0 and is_duplicated_notification(max(d_comment_same_post["time"].to_list())) is False:
                    print("find people also comment same post")
                    # print(d_comment_same_post)
                    print(get_users(d_comment_same_post, user_id))

                    n[user_id].append(
                        {"id": interaction.id_generator(),
                         "time": max(d_comment_same_post["time"].to_list()),
                         "url_info": get_url_info(post_id),
                         "users": users,
                         "user_photo_url": get_user_photo_url(users[0]),
                         "action": "comment_same_post"})
                del users
                del d_comment_same_post
            # find people comment in the same post
            elif action == "like_reply_comment":
                d_comment_same_post = df.query('action == "comment_post" and post_id == @post_id')
                users = get_users(d_comment_same_post, user_id)
                if len(users) > 0 and is_duplicated_notification(max(d_comment_same_post["time"].to_list())) is False:
                    print("find people also comment same post")
                    # print(d_comment_same_post)
                    print(get_users(d_comment_same_post, user_id))
                    n[user_id].append(
                        {"id": interaction.id_generator(),
                         "time": max(d_comment_same_post["time"].to_list()),
                         "url_info": get_url_info(post_id),
                         "users": users,
                         "user_photo_url": get_user_photo_url(users[0]),
                         "action": "comment_same_post"})
                del users
                del d_comment_same_post
            # find people comment in the same post
    with open("notifications.txt", "w") as f:
        f.write(json.dumps(n))
    return n


def get_notifications_for(user_id):
    with open("notifications.txt", "r") as f:
        n = json.loads(f.read())
    if user_id in n.keys():
        return n[user_id]
    else:
        return None


def get_url_info(post_id):
    df_goodnews = [i for i in os.listdir('multi_news') if "goodnews" in i]
    for file_name in df_goodnews:
        dfg = pd.read_csv(os.path.join('multi_news',file_name), sep="#")
        for i in range(len(dfg)):
            if dfg['url'].iat[i] == post_id:
                return '#'.join([str(i) for i in dfg.iloc[i,:].to_list()])


def get_n(user_id):
    df = load_df()
    users = list(set(df["user_id"]))
    posts = list(set(df.query("user_id==@user")["post_id"]))
    comments = list(set(df.query("user_id==@user")["comment_id"]))
    q = "user_id!=@user_id and\
    ((post_id==@posts and action!='view_post') or\
    (action=='like_comment_post' and comment_id==@comments))"
    n = df.query(q)
    print(n)
