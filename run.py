#-*- coding: utf-8 -*-

import sys
from time import sleep

from config import *
from weibopy.auth import OAuthHandler
from weibopy.api import API
from helper import Writer

class Weibo(object):
    """
    新浪微博自动备份.
    """
    def __init__(self):
        self.hdl = OAuthHandler(APP_KEY, APP_SECRET)
        self.api = None
        self.writer = None
        self.reader = None
        self.token  = {}

    def auth(self, pin=""):
        try:
            """
            token = self.hdl.get_access_token(pin)
            """
            self.hdl.setToken(
                TOKEN,
                SECRET
            )
            self.api = API(self.hdl)
        except Exception, e:
            print e

    def get_auth_url(self):
        return self.hdl.get_authorization_url()

    def get_status(self, screen_name, page):
        count = 20
        while True:
            try:
                res = self.api.user_timeline(
                    screen_name=screen_name,
                    count=count,
                    page=page
                )
                if len(res)==0:
                    return page
                else:
                    for status in res:
                        text = status.text
                        retweet = getattr(
                            status,
                            "retweeted_status",
                            False
                        )
                        if retweet:
                            text = text+"//"+retweet.text
                        text = text.encode("utf-8")
                        self.writer.append(text)
                page = page+1
            except Exception, e:
                print e
            

    def save_status(self, screen_name, filename):
        self.writer = Writer(filename)
        page,alert_num = 1,0
        while alert_num<ALERT_MAX_TIMES:
            page = self.get_status(screen_name, page)
            alert_num += 1

    def update(self, status):
        ret = self.api.update_status(status=status)
        return getattr(ret, 'id')

    def update_status(self, filename):
        self.reader = Reader(filename)
        while True:
            status = self.reader.read()
            if not status:
                return
            self.update(status) 
            sleep(0.5)

    def get_followers(self, screen_name):
        follwers = []
        count = 20
        page, alert_num = 0,0
        while alert_num<ALERT_MAX_TIMES:
            try:
                res = self.api.friends(
                    screen_name=screen_name,
                    cursor=page*count
                )
                if len(res) == 0:
                    alert_num += 1
                    sleep(2)
                    continue
                else:
                    map(lambda p:follwers.append(p.screen_name), res)
                page = page+1
            except Exception, e:
                print e
        return follwers
        
    def set_followers(self, follwers):
        # TODO:
        count, limit = 0, 60
        for uid in follwers[35:]:
            try:
                res = self.api.create_friendship(
                    user_id=uid
                )
                count += 1
                #if not count%limit:
                #   sleep(3600)
            except Exception, e:
                print e

    def destroy_friendship(self, name):
        self.api.destroy_friendship(
            screen_name=name
        )  

    def run(self, screen_name):
        # Step1.Get All status
        # Step2.Get All Follwers
        # Step3.Set All Follwers.
        # Step4.Update All status
        targets = self.get_followers(screen_name)
        self.set_followers(targets)

if __name__ == '__main__':
    obj = Weibo()
    obj.auth()
    friends = obj.get_followers(self, TARGET)
    print "LEN: ", len(friends)
