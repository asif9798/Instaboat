import requests
import urllib
import time
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

ACCESS_TOKEN = '4476537005.3661e10.d5d178bdb2ed4854bf3fc8e098f24a7f'

#Token Owner : Asif Ahmed
#Sandbox Users : bhavna,xsschauhan

BASE_URL = 'https://api.instagram.com/v1/'

'''
Function declaration to get your own info

'''

def self_info():
    url = (BASE_URL + 'users/self/?access_token=%s') %(ACCESS_TOKEN)
    print 'GET request url : %s' %(url)
    r = requests.get(url).json()


    if r['meta']['code'] == 200:
        if len(r['data']):
            print 'Username: %s' % (r['data']['username'])
            print 'No. of followers: %s' % (r['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
            print 'No. of posts: %s' % (r['data']['counts']['media'])
            time.sleep(1)
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
function declaration to get the ownid of a user by username from instagram
'''

def get_user_id(insta_username):
    request_url = (BASE_URL + "users/search?q=%s&access_token=%s") % (insta_username,ACCESS_TOKEN)
    print 'GET request url of get_user_id: %s' % (request_url)
    user_info = requests.get(request_url).json()
    print user_info

    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            return user_info["data"][0]["id"]
        else:
            return None
        time.sleep(2)
    else:
        print'status code other than 200!'

        time.sleep(2)


'''
search the information of a user by username
'''

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'user not exist'
        exit()

    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id,ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:

            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


'''
function to get most recent post of user self
'''

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (ACCESS_TOKEN)
    print 'url of post is :%s' %(request_url)
    r = requests.get(request_url).json()


    if r['meta']['code'] == 200:
        if len(r['data']) :
            img_name = r['data'][0]['id'] + '.jpeg'
            img_url = r['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url, img_name)
            print 'your image has been downloaded'
        else:
            print"post does not exist"
            #exit()
    else:
        print 'status code other than 200! received'

'''
function to get a user post
'''

def get_user_post(insta_username):
    '''1.search for user id by its iusername
       2.
    '''
    user_id = get_user_id(insta_username)
    if user_id == None:
        print"user not exist"
        exit()

    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") %(user_id, ACCESS_TOKEN)
    print " Get request url is :%s" % (request_url)
    user_media = requests.get(request_url).json()

    if user_media ['meta']['code'] == 200:
        if len(user_media['data']):
            img_name = user_media['data'][0]['id'] + '.jpeg'
            img_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url,img_name)
            print "your image has been downloaded sucessfully "
        else:
            print "post does not exist"
    else:
        print "status code other than 200 received!"

'''
function to get total media like by the user
'''

def getcount_user_like():
    '''
    1.url of media like by the user
    2.extract the count and print it
    '''
    url = BASE_URL + ("users/self/media/recent?access_token=%s") %(ACCESS_TOKEN)
    print "Get request url for post like by user is %s:" %(url)
    r=requests.get(url).json()
    s1= r['data'][0]['likes']['count']
    print"total media like by the user is %s" % (s1)

'''
function declaration to get id of recent post of a user by username
'''

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
            time.sleep(2)
        else:
            print 'There is no recent post of the user!'
            time.sleep(2)
    else:
        print 'Status code other than 200 received!'
        time.sleep(2)



'''
function declaration to like a post
'''

def like_a_post(insta_username):
  media_id = get_post_id(insta_username)
  request_url = (BASE_URL + 'media/%s/likes') % (media_id)
  payload = {"access_token": ACCESS_TOKEN}
  print 'POST request url : %s' % (request_url)
  post_a_like = requests.post(request_url, payload).json()

  if post_a_like['meta']['code'] == 200:
      print 'Like was successful!'
      time.sleep(2)
  else:
      print 'Your like was unsuccessful. Try again!'
      time.sleep(2)

'''
function to get a list of comments
'''

def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = BASE_URL+("media/%s/comments/?access_token=%s") %(media_id, ACCESS_TOKEN)
    print "Get request url is %s" %(request_url)
    comment_list = requests.get(request_url).json()
    print comment_list
    type (comment_list)

    if comment_list["meta"]["code"]==200:
        if len(comment_list["data"]):
            position =1;
            for _ in comment_list['data']:
                print "Username: %s" % (comment_list["data"][position - 1]["from"]["username"])
                print "comment: %s" % (comment_list["data"][position - 1]["text"])
                position = position + 1
                time.sleep(2)
            print 'Number of comments:' + str(position - 1)
        else:
            print "There is no comment"
            time.sleep(2)
    else:
        print "status code other than 200 received!"
        time.sleep(2)



'''
function declaration to comment on a post
'''

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("write a comment: ")
    payload ={"access_token" : ACCESS_TOKEN, "text" : comment_text }
    url = (BASE_URL + 'media/%s/comments') % (media_id)
    print "post request url is : %s" % (url)
    make_comment = requests.post(url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "successfull added a new comment!"
        time.sleep(2)
    else:
        print "unable to add comment.Try again!"
        time.sleep(2)







def start_bot():
    while True:
        print '\n'
        print"welcome to instaboat \npleasse select your action"
        print "a.get your own details"
        print "b.get details of a user by username"
        print "c.get  your own recent post "
        print "d.get the recent post of a user by username "
        print "e.get total media liked by a user"
        #print "f.Get a list of people who have liked the recent post of a user"
        print "g.Like the recent post of a user"
        print "h.Get a list of comments on the recent post of a user"
        print "i.Make a comment on the recent post of a user"
        #print "j.Delete negative comments from the recent post of a user"
        print "k.Exit"

        choice = raw_input("enter your choice:")
        if choice == "a":
            self_info()
        elif choice == "b":
            name=raw_input("enter user name ")
            get_user_info(name)
        elif choice == "c":
            get_own_post()
        elif choice =="d":
            name = raw_input("enter user do want to download the media:")
            get_user_post(name)
        elif choice == "e":
            getcount_user_like()

        elif choice == "g":
            name = raw_input("enter the username of the user you want to like the media")
            like_a_post(name)
        elif choice =="h":
            name = raw_input("enter username")
            get_comment_list(name)


        elif choice =="i":
            name = raw_input("enter username to comment for a post")
            post_a_comment(name)


        elif choice == "j":
            print "you chose for exit"
            exit()
        else:
            print "wrong choice! please choose correct choice"


start_bot()

