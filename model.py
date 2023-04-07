'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
import sql
import os
import random
import json 
import datetime
import pickle
import time
import math
from bottle import request,response,redirect
import uuid
from collections import Counter
from CF_Recommend import cf_recommend

cf=cf_recommend("./data")


# Initialise our views, all arguments are defaults for the template

SESSION_EXPIRATION_TIME = datetime.timedelta(minutes=30)
catlist=["Cat__Thematic","Cat__Strategy","Cat__War","Cat__Family","Cat__CGS","Cat__Abstract","Cat__Party","Cat__Childrens","Cat__Other"]


page_view = view.View()
if os.path.exists("./temp.db")==False:
    database = sql.SQLDatabase("./temp.db")
    database.database_setup()
else:
    database = sql.SQLDatabase("./temp.db")


    # If need more table, then run below code depend on different case


    # Only run one time when you copy db from data direcotory after run test.py
    # database.database_reconstruct_login_part()
    # database.database_add_default_users_to_Userpassword()



# Get index of all attribute in certain db
attributelist=database.view_attribute("Games_Feture_Engineering")
attrdict={}

for i in attributelist:

    attrdict[i[1]]=i[0]

    



def update_user_rate_for_game(userid,rate,bggid):
    pass




def check_game_type(ls):
    for q in catlist:
        if ls[attrdict[q]]=="1":
        # print(q,i[attrdict[q]])
            return q.lstrip("Cat__")

    



def home():

    # username=username
    
    
    # Modify here to generate string in html format can be then be upload


    if is_valid_session():
        session_id=request.get_cookie('session_id')
        print(database.retrieve_session_data(session_id)['username'])




        username=database.retrieve_session_data(session_id)['username']
    




        # Get what user like and return


        recommend_result=cf.recommend(user_id=float(username), top_n=200)
        recommend_type_ls=[]
        percentage_ls=[]


        for index, row in recommend_result.iterrows():
            # dictgame={}
            # dictgame['rank']=index
            # dictgame['name']=row['p_Name']
            # dictgame['pop']=row['prediction']
            # dictgame['url']="/showgame?gameid={}".format(row['p_BGGId'])



            item=database.get_specific_game_by_gameid(row['p_BGGId'])
            cat=check_game_type(item)
            percentage_ls.append(cat)

        total_categories = len(percentage_ls)
        category_counts = {}
        for category in percentage_ls:
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1

        category_percentages = {}
        for category, count in category_counts.items():
            category_percentages[category] = count / total_categories * 100

        # Sort the percentage list by category
        sorted_percentages = sorted(category_percentages.items(), key=lambda x: x[1],reverse=True)

        # print(sorted_percentages)



        for i in range(0,len(sorted_percentages)):
            tmp=["<tr>","<td>","<h3>{}</h3>".format(i+1),
                "</td>"
                "<td>",
                "<a href=\"/recommend_game_of_certain_type?username={}&gametype={}\"></a>".format(username,sorted_percentages[i][0]),
                "<h4>{}<br></h4>".format(sorted_percentages[i][0]),
                "<span>{:.2f}%</span>".format(sorted_percentages[i][1]),
                "</a>",
                "</td>",
                "</tr>"]

            tmp2=''.join(tmp)
        
            recommend_type_ls.append(tmp2)

        recommend_type_ls=''.join(recommend_type_ls)


        return page_view("home",username=username,recommend_type=recommend_type_ls)
        
        
    
    else:

        username="vistor"
        # Generate category percentage

        topgames=database.select_top_n_game_by_column(column="AvgRating",top_n="1000")

        top_game_cate=[]


        rank=1
        for i in topgames:
            dictgame={}
            dictgame['rank']=rank
            dictgame['name']=i[attrdict['Name']]



            dictgame['description']=i[attrdict['Description']]



            # If you want label category
            for q in catlist:
                # print(i[attrdict[q]],q)
                if i[attrdict[q]]=="1":
                    # print(q,i[attrdict[q]])
                    dictgame['description']=q.lstrip("Cat__")
                    top_game_cate.append(q.lstrip("Cat__"))



            predictvalue=100-rank*5
            dictgame['pop']=predictvalue
            # print(i[attrdict['BGGId']])
            dictgame['url']="/showgame?gameid={}".format(i[attrdict['BGGId']])
            
            

            # calculate the percentage of each word
            rank=rank+1






        # count the occurrences of each word in the list
        word_counts = Counter(top_game_cate)

        # calculate the total count of all words
        total_count = sum(word_counts.values())
        percentages = {word: count / total_count * 100 for word, count in word_counts.items()}
        sorted_words = sorted(percentages.items(), key=lambda item: item[1], reverse=True)
        
        # print(sorted_words)
        
        
        
        
        recommend_type_ls=[]
        catrank=1
        for word, count in sorted_words:
            # print(word, count)
            # percentage = (count / total_count) * 100
            # print(f"{word}: {count:.2f}%")


            tmp=["<tr>","<td>","<h3>{}</h3>".format(catrank),
                "</td>"
                "<td>",
                "<a href=\"/recommend_game_of_certain_type?username={}&gametype={}\"></a>".format(username,word),
                "<h4>{}<br></h4>".format(word),
                "<span>{:.2f}%</span>".format(count),
                "</a>",
                "</td>",
                "</tr>"]

            tmp2=''.join(tmp)
            
            recommend_type_ls.append(tmp2)
            catrank=catrank+1
        recommend_type_ls=''.join(recommend_type_ls)



        

        return page_view("home",username=username,recommend_type=recommend_type_ls)





def recommend_game_of_certain_type(username,gametype):


    # Based on username, generate recommend game type and game in each type

    session_id=request.get_cookie('session_id')
    if session_id!=None:
        try:
            username=database.retrieve_session_data(session_id)['username']
        except:
            username="visitor"
    else:
        username="visitor"

    # Define a Python dictionary
    dat=[]




    # print(gametype)
    print(username,gametype)


    if gametype!=None and username=="visitor":


        topgames=database.select_top_n_game_by_column(column="AvgRating",top_n="200")



        rank=1
        for i in topgames:
            dictgame={}
            for q in catlist:
                # print(i[attrdict[q]],q)
                if i[attrdict[q]]=="1":
                    # print(q,i[attrdict[q]])
                    dictgame['description']=q.lstrip("Cat__")
                    break
            if dictgame['description']!=gametype:
                continue


            dictgame['rank']=rank
            dictgame['name']=i[attrdict['Name']]



 



            predictvalue=100-rank*5
            dictgame['pop']=predictvalue
            # print(i[attrdict['BGGId']])
            dictgame['url']="/showgame?gameid={}".format(i[attrdict['BGGId']])
            rank=rank+1
            dat.append(dictgame)


        # rank=1
        # for i in topgames:
        #     dictgame={}
        #     dictgame['rank']=rank
        #     dictgame['name']=i[attrdict['Name']]
        #     for q in catlist:
        #         if i[attrdict[q]]==1:
        #             dictgame['description']=q

        #     predictvalue=90
        #     dictgame['pop']=predictvalue
        #     dictgame['url']="/showgame?gameid=".format(i[attrdict['BGGId']])
        #     rank=rank+1
        #     dat.append(dictgame)


        # recommend_game_of_all_type=["<tr>","<td>2</td>","<td>Seikiro</td>","<td>ACT game</td>","<td><span class=\"status high\">42%</span></td>","<td>bggid</td>","</tr>"]

        # dat = [
        #     {
        #         "rank": "1",
        #         "name": "Dark Soul 3",
        #         "description": "Hard game",
        #         "pop":"90",
        #         "url":"https://google.com"
        #     },
        #     {
        #         "rank": "2",
        #         "name": "Dark soul 2",
        #         "description": "Another Hard game",
        #         "pop":"60",
        #         "url":"https://google.com"
        #     },
        #     {
        #         "rank": "3",
        #         "name": "Dark soul 1",
        #         "description": "Very Hard game",
        #         "pop":"30",
        #         "url":"https://google.com"
        #     },
        #     {
        #         "rank": "3",
        #         "name": "Dark soul 1",
        #         "description": "Very Hard game",
        #         "pop":"30",
        #         "url":"https://google.com"
        #     },
        #     {
        #         "rank": "3",
        #         "name": "Dark soul 1",
        #         "description": "Very Hard game",
        #         "pop":"30",
        #         "url":"https://google.com"
        #     },
        #     {
        #         "rank": "3",
        #         "name": "Dark soul 1",
        #         "description": "Very Hard game",
        #         "pop":"30",
        #         "url":"https://google.com"
        #     }

        # ]

    elif gametype==None and username=="visitor":


        topgames=database.select_top_n_game_by_column(column="AvgRating",top_n="20")

        rank=1
        for i in topgames:
            dictgame={}
            dictgame['rank']=rank
            dictgame['name']=i[attrdict['Name']]





            # If you want label category
            for q in catlist:
                # print(i[attrdict[q]],q)
                if i[attrdict[q]]=="1":
                    # print(q,i[attrdict[q]])
                    dictgame['description']=q.lstrip("Cat__")



            predictvalue=100-rank*5
            dictgame['pop']=predictvalue
            # print(i[attrdict['BGGId']])
            dictgame['url']="/showgame?gameid={}".format(i[attrdict['BGGId']])
            rank=rank+1
            dat.append(dictgame)

        # dat = [
        #     {
        #         "rank": "1",
        #         "name": "(Type: all)Most popular game 1 for visitor",
        #         "description": "Hard game",
        #         "pop":"90",
        #         "url":"https://google.com"
        #     },
        #     {
        #         "rank": "2",
        #         "name": "(Type: all) Most popular game 2 for visitor",
        #         "description": "Another Hard game",
        #         "pop":"60",
        #         "url":"https://google.com"
        #     },
        #     {
        #         "rank": "3",
        #         "name": "(Type: all) Most popular game 3 for visitor",
        #         "description": "Very Hard game",
        #         "pop":"30",
        #         "url":"https://google.com"
        #     }

        # ]

    elif username!="visitor" and gametype==None:
        """# 3. Recommendation"""
        recommend_result=cf.recommend(user_id=float(username), top_n=20)
        for index, row in recommend_result.iterrows():
            dictgame={}
            dictgame['rank']=index+1
            dictgame['name']=row['p_Name']

            item=database.get_specific_game_by_gameid(row['p_BGGId'])
            cat=check_game_type(item)

            # print(row['p_Name'],type(row['p_Name']))
            dictgame["description"]=cat
            dictgame['pop']="{:.2f}".format(float(row['prediction'])*10)
            dictgame['url']="/showgame?gameid={}".format(row['p_BGGId'])



            dat.append(dictgame)


    elif username!="visitor" and gametype!=None and ("Cat__"+gametype) in catlist:
        

        # Recommend first, return based on gametype
        
        """# 3. Recommendation"""
        recommend_result=cf.recommend(user_id=float(username), top_n=200)
        count=1

        for index, row in recommend_result.iterrows():
            item=database.get_specific_game_by_gameid(row['p_BGGId'])
            cat=check_game_type(item)
            if count <= 20 and cat ==gametype:
                dictgame={}
                dictgame['rank']=count
                dictgame['name']=row['p_Name']

                # print(row['p_Name'],type(row['p_Name']))
                dictgame["description"]=cat
                dictgame['pop']="{:.2f}".format(float(row['prediction'])*10)
                dictgame['url']="/showgame?gameid={}".format(row['p_BGGId'])
                dat.append(dictgame)

                count+=1
            else:
                continue




    # Convert the Python dictionary to a JSON object
    dat2 = json.dumps(dat)


    return dat2

def search(keyword):

    attributelist=database.view_attribute("Games_Feture_Engineering")



    attrdict={}

    for i in attributelist:

        attrdict[i[1]]=i[0]



    result=database.get_game(keyword)

    merchant_list=""

    if result!=False:


        

        for i in result:
            concatels=["<div class='"'merchant'"' onclick='"'showgame(this)'"'>",
                       "<img src='"'{}'"' alt='"'Merchant Image'"'>".format(i[attrdict['ImagePath']]),
                       "<div>"+"<h3>{}</h3>".format(i[attrdict['Name']]),
                       "<h2 style=\"display: none;\">{}</h2>".format(i[attrdict['BGGId']]),
                       "<p>{}</p>".format(i[attrdict['Description']])
                       ,"</div>"+"</div>"]
            merchant_list=merchant_list+' '.join(concatels)


        return page_view("search_result",merchant_list=merchant_list)
    
    else:
        return page_view("search_result",merchant_list=merchant_list)
    







def showgame(gameid):

    attributelist=database.view_attribute("Games_Feture_Engineering")



    attrdict={}

    for i in attributelist:

        attrdict[i[1]]=i[0]



    result=database.get_specific_game_by_gameid(gameid)


    if result!=False:
        # print(result)

        
        picture_path="<img src=\" "+result[attrdict['ImagePath']]+"\" alt='"'Game Image'"'>"



        return page_view("game",gameid=gameid,Name=result[attrdict['Name']],picture_path=picture_path,Description=result[attrdict['Description']]
                         ,MinPlayers=result[attrdict['MinPlayers']],YearPublished=result[attrdict['YearPublished']]
                         ,MaxPlayers=result[attrdict['MaxPlayers']],BGGId=result[attrdict['BGGId']])
    
    else:
        return page_view("game")





def registerpage():
    return page_view("register")




def register(username,password):

    if database.check_u_register(username)==False:

        database.add_u(username,password)
    else:
        print("Username already registered! Try again!")

        return page_view("register")

    return page_view("home",username="vistor")




def update_session_expiry_time(session_id):
    current_time = datetime.datetime.now()

    # Calculate the new expiry time based on the session expiration time
    expiry_time = current_time + SESSION_EXPIRATION_TIME

    # Update the session data in the session data store with the new expiry time
    session_data = database.retrieve_session_data(session_id)
    session_data['expiry_time'] = expiry_time.strftime('%Y-%m-%d %H:%M:%S')
    database.update_session_data(session_id, session_data)



def is_valid_session():
    # Check if the session ID is present in the session cookie
    session_id = request.get_cookie('session_id')
    print(session_id)
    if session_id==None:
        print("sessionid not exist")
        return False

    # Retrieve the session data from the session data store
    session_data = database.retrieve_session_data(session_id)

    # Check if the session data exists
    
    print(session_data)
    
    if not session_data:

        return False

    # Check if the session has expired
    session_expiry_time = session_data.get('expiry_time')
    session_expiry_time= datetime.datetime.strptime(session_expiry_time, '%Y-%m-%d %H:%M:%S')



    if session_expiry_time and session_expiry_time < datetime.datetime.now():
        # Remove the expired session from the session data store
        database.remove_session_data_by_session_id(session_id)
        return False

    # If the session is valid, update the expiry time
    update_session_expiry_time(session_id)

    # Return True to indicate that the session is valid
    return True



def loginpage():

    if is_valid_session():
        print("already sign in")
        redirect("/home")

    return page_view("login")



def login(username,password):

    # check login
    result=database.get_u(username,password)

    if result!=False:
        # print("Result")
        print("Find user:{} , hash value:{} ".format(result[0],result[1]))

        session_id = str(uuid.uuid4())
        
        username=result[0]

        expiry_time= datetime.datetime.now()+SESSION_EXPIRATION_TIME
        expiry_time= expiry_time.strftime('%Y-%m-%d %H:%M:%S')


        print(expiry_time)

        # Store the session ID in a session cookie
        response.set_cookie('session_id', session_id, path='/')

        database.remove_session_data_by_username(username)
        database.add_session(session_id,username,expiry_time)
        print(database.retrieve_session_data(session_id))
        print("here")
        # redirect("/home?param1=value1&param2=value2")
        redirect("/home")
    else:
        print("Not found")
        redirect("/login")

    # return page_view("home")



def logout():
    response.delete_cookie('session_id')
    redirect("/home")


def user_profile():
    if is_valid_session():
        session_id=request.get_cookie('session_id')
        print(database.retrieve_session_data(session_id)['username'])
        username=database.retrieve_session_data(session_id)['username']



        user_rate_games=[]
        ls=database.get_all_rating_by_userid(username)
        # print(ls)
        sorted_data = sorted(ls, key=lambda x: x[1],reverse=True)


        for i in sorted_data:
            

            # ('213788', '7.50667', '10017')
            #    bggid      rate      userid
            bggid=i[0]
            rate=i[1]

            res=database.get_specific_game_by_gameid(bggid)

            gamename=res[attrdict['Name']]


            link="<a href=\"/showgame?gameid={}\">{}</a>".format(bggid,gamename)

            tmp=["<tr>",
                 "<td>{}</td>".format(link),
                "<td>{}</td>".format(rate),
                "</tr>"]
            tmp2="".join(tmp)
            user_rate_games.append(tmp2)
        user_rate_games="".join(user_rate_games)




    
        return page_view("profile",username=username,user_rate_games=user_rate_games)
    else:
        # pass
        redirect("/home")





def print_userid():
    session_id=request.get_cookie('session_id')
    print(database.retrieve_session_data(session_id)['username'])