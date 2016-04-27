# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 15:42:30 2016

@author: Waffleboy
"""
from facepy import GraphAPI
import random as rand
from dateutil import parser
import csv

##Insert Token from GraphAPI here
TOKEN = 'INSERT TOKEN HERE'
#Keywords to look for
hitWords = set(['hb','birthday','bday','bday!','happy','hbd','birfday'])
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
    graph.post(postID+'/comments', message = rand.choice(randomReply))

""" end subsidary functions """


### MAIN FUNCTION ###

#Input: 
#1) <Boolean> Silent :if true, individual names of posters will not be printed to console.
#2) <Boolean> save :if true, will save people who wished you to csv file for reference.
def main(silent=True,save=False):
    global TOKEN
    counter = 0 
    graph = GraphAPI(TOKEN) #initialize facepy
    currentPage=graph.get('me/feed') # Get my latest posts
    # Get my Information
    myInfo = graph.get("me")
    myBirthdate = parser.parse(myInfo['birthday']).date()
    myID = myInfo['id']
    
    if save: #if save, create file to save to
        with open('birthday'+str(myBirthdate.year)+'.csv','a') as f:
            writer = csv.writer(f)
            writer.writerow(['ID','Name'])

    nextPage = True
    while nextPage:
        data = currentPage['data'] #get list of posts
        for entry in data:
            # Terminating conditions #
            #1 --> Beyond my birthday.
            date = parser.parse(entry['created_time']).date()
            if date.month < myBirthdate.month or date.day < myBirthdate.day:
                nextPage = False
                print('Completed. Replied '+str(counter)+' posts.')
                return 
            
            # Skipping Conditions #
            #1 if poster is myself, skip
            if entry['id'] == myID:
                continue
            
            #Else, check if birthday msg, post random reply
            if checkIfBirthdayMessage(entry['message']) == True:
                counter+=1
                postReply(entry['id'])
                
                if not silent:
                    print('Replied '+entry['from']['name'])
                if save:
                    ID = entry['from']['id']
                    name = entry['from']['name']
                    with open('birthday'+str(myBirthdate.year)+'.csv','a') as f:
                        writer = csv.writer(f)
                        writer.writerow([ID,name])
        #page
        currentPage = currentPage['paging']['next']
        currentPage = nextPage.replace('https://graph.facebook.com/v2.0/','')

if __name__ == '__main__':
    main(silent=True,save=False)
