#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

 AUTHOR: zc
 HOST: zc@zcdeMacBook-Pro.local
 PATH: getcode4sis.py
 DATE: 2014-11-07 10:51:32


 INTRODUCTION:
    <<introduction write on here>>

 CHANGLOG:
    # FORMAT: DATE TIME AUTHOR COMMENT
    # etc. 2014-10-14 16:51:32 zc  # comment on here.

    <<changelog write on here>>

'''

import urllib2
import time

t = time.localtime(time.time())
forum_url = 'http://www.sis001.us/forum/forum-515-1.html'
pre_url = "http://www.sis001.us/forum/"
sStr = "redirect.php?tid="
eStr = "</a></em>"

tsStr="&nbsp; &nbsp; &nbsp; &nbsp;"
teStr="<br />"
today = str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)


def get_new_url():
    update_today = False
    req = urllib2.Request(forum_url)
    response = urllib2.urlopen(req)
    print "request url:",response.code
    the_page = response.read()

    nPos = 0
    urls = []
    new_url=None
    while True:
        nPos = the_page.find(sStr, nPos+1)
        ePos = the_page.find(eStr, nPos+1)
        #print the_page[nPos:ePos]
        urls.append(the_page[nPos:ePos])
        if nPos <= 0:
            break

    # skip something
    skips=["4477420", "9232561", "9226870", "9211877", "9188205", "4102660"]
    for s in skips:
        for u in urls:
            if u.find(s) >0 or len(u)<=0:
                try:
                    urls.remove(u)
                except:
                    continue

    # get date yyyy-m-d
    pub_at = urls[0][urls[0].index(">")+1:][:-6]
    if pub_at==today:
        update_today = True
        new_url = urls[0][:urls[0].index(">")-1].replace("amp;","")
        print "we got new url:",new_url

    return new_url, update_today


def get_new_code(new_url):
    req = urllib2.Request(pre_url + new_url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    nPos = 0
    urls = []
    codes=[]
    while True:
        nPos = the_page.find(tsStr, nPos+1)
        ePos = the_page.find(teStr, nPos+1)

        code = the_page[nPos:ePos]
        if code.find("</div>") >0:
            code = code[:code.index("</div>")]
        if len(code)>0:
            codes.append(code.split(tsStr))

        if nPos <= 0:
            break
        nPos=ePos+1
    codes.pop(0)
    return codes


def get_valid_code(codes):
    valid_codes=[]
    if not codes:
        return
    for c in codes:
        status_unicode = c[4].decode('gbk')
        status_utf_8 = status_unicode.encode('utf-8')
        if status_utf_8.replace(" ","") <> "标记为已送出":
            valid_codes.append(c[1])
    return valid_codes


def get_code():
    new_url, update_today = get_new_url()

    if new_url:
        valid_codes = get_valid_code(get_new_code(new_url))
        if valid_codes: #send to me
            print valid_codes
            send_mail("sis001 code! :)",','.join(valid_codes))
        else:
            print "not now! :("
    else:
        print "no update!"
    return update_today

if __name__ == '__main__':
    while True:
        if get_code():
            print "today is over! :( "
            break
        time.sleep(300)
