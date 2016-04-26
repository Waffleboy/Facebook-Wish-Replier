# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 15:42:30 2016

@author: Waffleboy
"""
from facepy import GraphAPI
import random as rand
from dateutil import parser

##Insert Token from GraphAPI here
TOKEN = 'INSERT TOKEN HERE'
#Keywords to look for
hitWords = set(['hb','birthday','bday','bday!','happy'])
#Replies to give
randomReply = ['Thanks! :)','Thank you! :)','Thanks alot! :)']

""" SUBSIDARY FUNCTIONS """
# Input: String: message
# Output: Boolean: True/False
# Desc: Check if a given string is a birthday message
def checkIfBirthdayMessage(message):
    global hitWords
    message = set(message.split(' '))
    if message.intersection(hitWords):
        return True
    return False

# Input: String: ID of post
# Output: Void
# Desc: like+comment on the birthday message
def postReply(postID):
    global randomReply
    #like post
    graph.post(postID+'/likes')
    #comment post
    graph.post(postID+'/comments',message= rand.choice(randomReply))

""" end subsidary functions """


### MAIN FUNCTION ###
def main():
    global TOKEN
    
    graph = GraphAPI(TOKEN) #initialize facepy
    currentPage=graph.get('me/feed') # Get my latest posts
    # Get my Information
    myInfo = graph.get("me")
    myBirthdate = parser.parse(myInfo['birthday']).date()
    myID = myInfo['id']

    nextPage = True
    while nextPage:
        data = currentPage['data'] #get list of posts
        for entry in data:
            # Terminating conditions #
            #1 --> Beyond my birthday.
            date = parser.parse(entry['created_time']).date()
            if date.month < myBirthdate.month or date.day < myBirthdate.day:
                nextPage = False
                return
            
            # Skipping Conditions #
            #1 if poster is myself, skip
            if entry['id'] == myID:
                continue
            
            #Else, check if birthday msg, post random reply
            if checkIfBirthdayMessage(entry['message']) == True:
                postReply(entry['id'])
        #page
        currentPage = currentPage['paging']['next']
        currentPage = nextPage.replace('https://graph.facebook.com/v2.0/','')

if __name__ == '__main__':
    main()
