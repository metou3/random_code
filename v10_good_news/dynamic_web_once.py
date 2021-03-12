import pandas as pd
import os
import time

def get_df_goodnews(l_tag):
    return pd.read_csv("multi_news/df_goodnews_"+l_tag+".csv", sep="#")


def main(l_tag, page_id):
    my_info = find_page_info(l_tag, page_id)
    return make_html(my_info)


def save_web(page_info, source_page):
    production_dir = '/home/contact_sunnysunny/apps/wordpress/htdocs/goodnews/web'
    debug_dir = 'web'
    if page_info["page_id"]+".html" not in os.listdir(production_dir+"/"+page_info["language"]):
        html_file = open("/".join([production_dir, page_info["language"], page_info["page_id"]+".html"]), 'w')
        html_file.write(source_page)
        html_file.close()
    else:
#        print("file existed")
        pass


def find_page_info(l_tag, page_id):
    my_df = get_df_goodnews(l_tag)
    page_id_col = my_df["page_id"]
    for ii in range(len(page_id_col)):
        if page_id in page_id_col[ii]:
            print(ii)
            my_info = my_df.iloc[ii]
            return my_info


# print(get_df_goodnews("en").iloc[5]["page_id"])

dict_continue_reading = {
    "ar": "أكمل القراءة...",
    "en": "Continue reading...",
    "vi": "Tiếp tục đọc...",
    "fr": "Continuer la lecture...",
    "de": "Weiterlesen...",
    "it": "Continua a leggere..."
}


def make_html(my_info):
    headline = my_info["title"]
    author = my_info["source_domain"]
    main_img = my_info["image_url"]
    description = my_info["description"]
    language = my_info["language"]
    datetime = my_info["datetime"]
    try:
        continue_reading = dict_continue_reading[language]
    except:
        continue_reading = dict_continue_reading["en"]
    html_template = """
                   <!DOCTYPE html>
                   <html>
                      <head>
                        <meta charset="utf-8">
                         <title>""" + headline + """</title>
                      </head>
                      <style>
                         img {
                         border-radius: 16px;
                         width: 80%;
                         height: auto;
                         }
                         a {
                      text-decoration: none !important;
                      color: black;
                   }
                   h3,h2,h1,p {
                         font-size: 4vw;
                         }
                         h1{
                            color:blue;
                         }
                   </style>
                      <body>
                         <div align="center">
                     <a href="https://play.google.com/store/apps/details?id=com.everythingsunny.goodnews">
                      <h1>""" + headline + """</h1>
                   <div align="left" style="margin-left:10vw">
                   <h3>""" + author + """</h3>
                  <h3>""" + datetime + """</h3>
                   </div>
                            <img alt="image_main" src=""" + main_img + """>
                      <p>""" + description + """</p>
                   <h3>""" + continue_reading + """</h3>
                            <img src="https://www.sunnybot.org/goodnews/logo-app.jpg"
                            style="height:auto;width:50%;">
                               <h2>Gorgeously: Only Good News, Daily Happy News</h2>
                                     <img src="https://www.sunnybot.org/goodnews/web/google-play-badge_""" + language + """.png"
                            style="height:auto;width:50%;">
                   </a>
                   </div>
                      </body>
                   </html>
                   """

    return html_template


if __name__ == '__main__':
   # print(get_df_goodnews("en").head())
	l_tags = ["en","ar", "fr", "de", "es", "it", "pt", "vi", "hi", "in", "sw"]
	for l_tag in l_tags:
		all_news = get_df_goodnews(l_tag)
		for i in range(len(all_news)):
			one_news = all_news.iloc[i]
			try:
				html_page = make_html(one_news)
				save_web(one_news, html_page)
			except Exception as e:
				print(e)
				print(l_tag)
				print(one_news)
				
	print("finish making web pages")

#        print("page_id", one_news["page_id"])

