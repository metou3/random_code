my_port = 5020
from dateutil.parser import parse
from dateutil.relativedelta import *
from datetime import datetime
from flask import Flask, request, redirect, url_for, send_from_directory, send_file
from flask import render_template, flash, session, redirect, jsonify
import re
import os
from werkzeug import secure_filename
from flask import jsonify
import pandas as pd
import string
import random
import pickle
import time
import requests
import subprocess as cmd
import interaction
import my_data_adapter
import json
import validate_subs
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import user_activities
import dynamic_web
import pandas as pd
import io

# my_l_tag="es,pl,sa,ns,el,da,ms,sw,sv,qu,mk,ko,lt,lv,nl,pt,is,tr,ja,pa,fa,tn,sl,bg,az,gl,he,bs,et,id,ur,hr,ky,mr,fr,ka,tl,ca,vi,nb,ps,sk,cy,fo,kk,en,it,ru,cs,se,ro,te,dv,zu,fi,eo,gu,hy,eu,sr,sy,zh,ar,mi,tt,uk,uz,nn,af,mt,th,ts,xh,mn,hi,sq,de,ta,hu,be,kn".split(",")
my_l_tag = ['af', 'am', 'ar', 'az', 'be', 'bg', 'bn', 'bs', 'ca', 'co', 'cs', 'cy', 'da', 'de', 'el', 'eo', 'es', 'et',
            'eu', 'fa', 'fi', 'fr', 'fy', 'ga', 'gd', 'gl', 'gu', 'ha', 'he', 'hi', 'hr', 'ht', 'hu', 'hy', 'id', 'ig',
            'in', 'is', 'it', 'iw', 'ja', 'ji', 'jv', 'jw', 'ka', 'kg', 'kk', 'km', 'kn', 'ko', 'ku', 'ky', 'la', 'lb',
            'lo', 'lt', 'lv', 'mg', 'mi', 'mk', 'ml', 'mn', 'mo', 'mr', 'ms', 'mt', 'my', 'nb', 'ne', 'nl', 'nn', 'no',
            'ny', 'or', 'pa', 'pl', 'ps', 'pt', 'ro', 'ru', 'rw', 'sd', 'sh', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq',
            'sr', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'tk', 'tl', 'tr', 'tt', 'ug', 'uk', 'ur', 'uz', 'vi',
            'xh', 'yi', 'yo', 'zh', 'zu']
# my_l_tag=["ar","bg","bn","cs","el","de","fr","en","he","hi"]+\
#                    ["hu","id","it","ja","ko","lt","ml","mr","nl","no"]+\
#                    ["pl","ro","ru","sk","sl","sr","sv","ta","te","th"]+\
#                    ["en",'tr','uk','vi']

from datetime import datetime as d

app = Flask(__name__)
# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["1/second"]
# )


@app.route('/ping')
def hello_world():
    return 'pong\n'


@app.route('/add_user', methods=["POST"], endpoint="add_user")
def add_user():
    if request.method == "POST":
        data = request.get_json()
        if "user_email" in data:
            return interaction.add_user(data["user_id"], data["user_email"],
                                        data["user_name"],
                                       #data["user_photo_url"],
					"none",
                                        data["language"],
                                        data["pro"])
        else:
            return interaction.add_user(data["user_id"], "empty",
                                        data["user_name"],
                                        #data["user_photo_url"],
					"none",
                                        data["language"],
                                        data["pro"])


@app.route('/user_sub/<string:action>', methods=["POST"], endpoint="user_sub")
def add_user(action):
    if request.method == "POST":
        data = request.get_json()
        if interaction.check_user(data["user_id"]):
            if action == "become_pro":
                return interaction.become_pro(data["user_id"])
            if action == "cancel_pro":
                return interaction.cancel_pro(data["user_id"])
            if action == "is_pro":
                return interaction.is_pro(data["user_id"])


@app.route('/data_adapter/<string:action>', methods=["GET", "POST"], endpoint="data_adapter")
def data_adapter(action):
    if request.method == "POST":
        data = request.get_json()
        # if interaction.check_user(data["user_id"]):
        #     if action == "get_basic_list":
        #         print("load basic list data")
        #         list_post_id = json.loads(
        #             data["list_post_id"].replace(" ", "").replace(",", '","').replace("[", '["').replace("]", '"]'))
        #         result = my_data_adapter.get_basic_list(list_post_id)
        #         return result
        #     elif action == "get_comments":
        #         return my_data_adapter.get_comments_of(data)
        #     else:
        #         return "bad_request"
        # else:
        #     return "bad_request"

        if action == "get_basic_list":
            print("load basic list data")
            list_post_id = json.loads(
                data["list_post_id"].replace(" ", "").replace(",", '","').replace("[", '["').replace("]", '"]'))
            result = my_data_adapter.get_basic_list(list_post_id)
            return result
        elif action == "get_comments":
            return my_data_adapter.get_comments_of(data)
        else:
            return "bad_request"


@app.route('/data_adapter1/<string:action>', methods=["GET", "POST"], endpoint="data_adapter1")
def data_adapter(action):
    if request.method == "POST":
        data = request.get_json()
        if interaction.check_user(data["user_id"]):
            if action == "get_notifications":
                r = my_data_adapter.get_notifications_for(data["user_id"])
                if r is not None:
                    return {"notifications": r}
                else:
                    return "zero_notifications"
            else:
                return "bad_request"
        else:
            return "bad_request"


@app.route('/interaction/<string:user_reaction>', methods=["GET", "POST"], endpoint="interaction")
def user_interaction(user_reaction):
    if request.method == "POST":
        data = request.get_json()
        if interaction.check_user(data["user_id"]):
            if user_reaction == "view":
                result = interaction.view_post(data)
                return result
            elif user_reaction == "share":
                result = interaction.share_post(data)
                return result
            elif user_reaction == "comment_post":
                result = interaction.comment_post(data)
                # print(result)
                return result
            elif user_reaction == "like_post":
                result = interaction.like_post(data)
                return result
            elif user_reaction == "dislike_post":
                result = interaction.dislike_post(data)
                return result
            elif user_reaction == "like_post_comment":
                result = interaction.like_post_comment(data)
                return result
            elif user_reaction == "dislike_post_comment":
                result = interaction.dislike_post_comment(data)
                return result
            elif user_reaction == "reply_comment":
                result = interaction.reply_comment(data)
                # print(result)
                return result
            elif user_reaction == "like_reply_comment":
                result = interaction.like_reply_comment(data)
                return result
            elif user_reaction == "dislike_reply_comment":
                result = interaction.dislike_reply_comment(data)
                return result
            return {"status": "bad_request"}
        else:
            return {"status": "non_valid_user"}


@app.route('/upload', methods=['GET', 'POST'], endpoint='upload')
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # print('**found file', file.filename)
            filename = secure_filename(file.filename)
            file_dir = os.path.join(os.getcwd() + "/multi_news/", filename)
            new_df = pd.read_csv(file, sep="#")
            old_df = pd.read_csv(file_dir, sep="#").iloc[:, 0:11]

            new_urls = new_df["url"].to_list()
            old_urls = old_df["url"].to_list()
            new_unique_urls = list(set(new_urls) - (set(new_urls) & set(old_urls)))
            new_df = new_df[new_df["url"].apply(lambda x: x in new_unique_urls)]

            combine_df = pd.concat([new_df, old_df]).drop_duplicates(keep="last").reset_index(drop=True)
            combine_df = combine_df[list(old_df.columns)[:11]]
            #final_df = my_data_adapter.add_reaction_to_df(combine_df)
            print("new_df", new_df)
            print("old_df", old_df)
            print("merge_and_remove_duplicate", combine_df)
            # file.save(file_dir)
            combine_df.to_csv(file_dir, sep="#", index=False)
            #os.system("sudo python3 dynamic_web_once.py")
            return jsonify({"status": "upload_done"})


@app.route('/upload/web/<string:l_tag>', methods=['GET', 'POST'], endpoint='upload_web')
def upload_file_01(l_tag):
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # print('**found file', file.filename)
            filename = secure_filename(file.filename)
            save_dir = os.path.join(os.getcwd(), "web", l_tag, filename)
            file.save(save_dir)
            cmd.call(["sudo", "mv", save_dir, "/opt/bitnami/apps/wordpress/htdocs/goodnews/web/" + l_tag])
            return jsonify({"status": "upload_done"})


@app.route('/web/<string:l_tag>/<string:page_id>', methods=['GET'], endpoint='view_web')
def view_web(l_tag, page_id):
    if request.method == 'GET':
        return dynamic_web.main(l_tag, page_id)


@app.route('/web', methods=['GET'], endpoint='view_web_1')
def view_web():
    if request.method == 'GET':
        print("l_tag", request.args.get("l_tag"))
        print("page_id", request.args.get("page_id"))
        return dynamic_web.main(request.args.get('l_tag')
                                , request.args.get('page_id'))


@app.route('/newsfeed', endpoint="newsfeed")
def return_file_01():
    try:
        return send_file('df_goodnews.csv', attachment_filename='df_goodnews')
    except Exception as e:
        return str(e)

@app.route('/multi_news/<string:l_tag>', endpoint="dl0")
def return_file_00(l_tag):
    time_limit = datetime.now() - relativedelta(days=30)
    csv_stream = io.StringIO()
    if l_tag not in my_l_tag:
        df = pd.read_csv(os.getcwd() + "/multi_news/" + 'df_goodnews_' + 'en' + ".csv", sep="#")
        # try:
        #     return send_file(os.getcwd() + "/multi_news/" + 'df_goodnews_' + 'en' + ".csv",
        #                      attachment_filename='df_goodnews')
        # except Exception as e:
        #     return str(e)
    else:
        df = pd.read_csv(os.getcwd() + "/multi_news/" + 'df_goodnews_' + l_tag + ".csv", sep="#")

    final_df = df[df["datetime"].apply(lambda x: parse(str(x)) > time_limit)]

    if l_tag!="en":
        df.to_csv(csv_stream, sep="#", index=False)
    else:
        final_df.to_csv(csv_stream, sep="#", index=False)

    mem = io.BytesIO()
    mem.write(csv_stream.getvalue().encode('utf-8'))
    # seeking was necessary. Python 3.5.2, Flask 0.12.2
    mem.seek(0)
    csv_stream.close()

    return send_file(mem, as_attachment=True, attachment_filename='df_goodnews.csv', mimetype='text/csv')

#@app.route('/multi_news/<string:l_tag>', endpoint="dl0")
#def return_file_00(l_tag):
#    if l_tag not in my_l_tag:
#        try:
#            return send_file(os.getcwd() + "/multi_news/" + 'df_goodnews_' + 'en' + ".csv",
#                             attachment_filename='df_goodnews')
#        except Exception as e:
#            return str(e)
#    else:
#        try:
#            return send_file(os.getcwd() + "/multi_news/" + 'df_goodnews_' + l_tag + ".csv",
#                             attachment_filename='df_goodnews')
            # return send_file(os.getcwd() +"/test_df"+ ".csv",
            #                  attachment_filename='df_goodnews')
#        except Exception as e:
#            return str(e)


@app.route('/multi_news_small_batch/<string:l_tag>', endpoint="dl0_small_batch")
def return_file_00(l_tag):
    if l_tag not in my_l_tag:
        try:
            file_dir = os.getcwd() + "/multi_news/" + 'df_goodnews_' + 'en' + ".csv"
            df = pd.read_csv(file_dir, sep="#")
            small_df = df.sample(n=5).reset_index(drop=True)
            csv_buffer = io.StringIO()
            small_df.to_csv(csv_buffer)
            return send_file(csv_buffer.getvalue(),
                             attachment_filename='df_goodnews', mimetype='text/csv', as_attachment=True)
        except Exception as e:
            return str(e)
    else:
        try:
            return send_file(os.getcwd() + "/multi_news/" + 'df_goodnews_' + l_tag + ".csv",
                             attachment_filename='df_goodnews')
        except Exception as e:
            return str(e)


@app.route('/js_config/<string:l_tag>', endpoint="js_config")
def return_js_config(l_tag):
    try:
        return my_data_adapter.get_config(l_tag)
    except:
        return my_data_adapter.get_config("en")


@app.route('/purchases/get_details/<string:purchase_token>', endpoint="purchases")
def get_purchase_details(purchase_token):
    results = validate_subs.get_purchase_detail(validate_subs.get_access_token(), purchase_token)
    if not results:
        time.sleep(5)
        results = validate_subs.get_purchase_detail(validate_subs.get_new_access_token(), purchase_token)
        return results
    else:
        return results


@app.route('/purchases/check_state/<string:purchase_token>/<string:sub_id>', endpoint="check_order_state")
def get_sub_state(purchase_token, sub_id):
    try:
        state = validate_subs.check_state(purchase_token, "0.99usd_1month_sub")
        return state
    except:
        pass
    try:
        state = validate_subs.check_state(purchase_token, "5.99usd_1month_sub")
        return state
    except:
        pass
    try:
        state = validate_subs.check_state(purchase_token, "2.99usd_1month_sub")
        return state
    except:
        pass
    try:
        state = validate_subs.check_state(purchase_token, "33.99usd_1year_sub")
        return state
    except:
        pass


@app.route("/get_urls/<string:l_tag>/<string:secret_key>", endpoint="get_urls")
def get_urls(l_tag, secret_key):
    if secret_key == "Y<.,&bh,Xe@hn5my":
        if l_tag not in my_l_tag:
            df = pd.read_csv(os.getcwd() + "/multi_news/" + 'df_goodnews_' + 'en' + ".csv", sep="#")
            # try:
            #     return send_file(os.getcwd() + "/multi_news/" + 'df_goodnews_' + 'en' + ".csv",
            #                      attachment_filename='df_goodnews')
            # except Exception as e:
            #     return str(e)
        else:
            df = pd.read_csv(os.getcwd() + "/multi_news/" + 'df_goodnews_' + l_tag + ".csv", sep="#")
        
        my_urls = df["url"].to_list()
        return jsonify({"status": True, "urls": my_urls})  
    else:
        return jsonify({"status": False})

@app.route('/upload/jsconfig/<string:l_tag>', methods=['POST'], endpoint='upload_jsconfig')
def upload_jsconfig(l_tag):
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # print('**found file', file.filename)
            filename = secure_filename(file.filename)
            save_dir = os.path.join(os.getcwd(), "jsconfig", filename)
            file.save(save_dir)
            return jsonify({"status": "upload_done"})

@app.route('/multi_news_general/<string:l_tag>', endpoint="dl_news_0")
def return_file_99(l_tag):
    time_limit = datetime.now() - relativedelta(days=3)
    csv_stream = io.StringIO()
    if l_tag not in my_l_tag:
        df = pd.read_csv(os.getcwd() + "/multi_news/" +
                         'df_news_' + 'en' + ".csv", sep="#")
    else:
        df = pd.read_csv(os.getcwd() + "/multi_news/" +
                         'df_news_' + l_tag + ".csv", sep="#")

    final_df = df[df["datetime"].apply(lambda x: parse(str(x)) > time_limit)]

    if len(final_df) < 100:
        df.to_csv(csv_stream, sep="#", index=False)
    else:
        final_df.to_csv(csv_stream, sep="#", index=False)

    mem = io.BytesIO()
    mem.write(csv_stream.getvalue().encode('utf-8'))
    # seeking was necessary. Python 3.5.2, Flask 0.12.2
    mem.seek(0)
    csv_stream.close()

    return send_file(mem, as_attachment=True, attachment_filename='df_news.csv', mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=my_port, host="0.0.0.0")
