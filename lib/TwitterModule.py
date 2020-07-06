#!/usr/bin/env python2

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 18:21:43 2020

Author: Priscila Gutierres <priscila.gutierres@gmail.com>

License: MIT
"""

import tweepy
import time

class ManageTwitter:
    '''This class manage tweepy API making it easy for the user'''
    
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, \
                 ACCESS_TOKEN_SECRET):
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth,wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)
#        self.streaming = self.MyStreamListener()
        
    def send(self, status):
        '''
        Sends a simple status.
        Input: status (string)
        '''
        self.api.update_status(status)
    def erase(self, tweet_id):
        '''
        Erases a single status
        Input: status ID (string)
        '''
        self.api.destroy_status(tweet_id)
    def erase_all(self,pattern):
        '''
        Erases a bunch of statuss with a pattern
        Input: pattern (string)
        '''
        for status in tweepy.Cursor(self.api.user_timeline).items():
            if pattern in status.text:
                self.api.destroy_status(status.id)
    def search(self,text, items = 10):
        '''
        Searchs for some text in tweets
        Input: text, items (optional)
        Output: tweets that match
        '''
        result = tweepy.Cursor(self.api.search, q=text).items(items)
        return result
    def reply(self, status, tweetid):
        '''
        Reply a status by a certain user
        Input: status (string), tweetid (string) 
        '''
        self.api.update_status(status, in_reply_to_status_id = tweetid)
    def retweet(self, tweetid):
        '''
        Retweet a status by a certain user
        Input: tweetid (string)
        '''
        self.api.retweet(tweetid)
        
    def verify(self):
        '''
        Verify if the credentials are ok. 
        Raise an exception if not
        '''
        self.api.verify_credentials()
    def stream(self,status,time):
        '''
        Do Async Streaming 
        Input: status (string)
        '''
        myStreamListener = MyStreamListener(time_limit=time)
        myStream = tweepy.Stream(auth = self.api.auth,
                                 listener = myStreamListener)
        myStream.filter(track=[status], is_async = True)
    
class MyStreamListener(tweepy.StreamListener):
    '''
    Create class MyStreamListener inheriting from StreamListener 
    and overriding on_status
    '''
    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        super(MyStreamListener, self).__init__()
        
    def on_status(self,status):
        '''
        Returns a stream
        '''
        if (time.time() - self.start_time) < self.limit:
            author = status.author._json['screen_name']
            date = status.created_at
            print('\n')
            print('@{}, {}'.format(author,date))
            print(status.text)
            return True
        else:
            return False
          
  
    