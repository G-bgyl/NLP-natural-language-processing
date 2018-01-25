# -*- coding: utf-8 -*-
__author__ = 'Alicia Ge'
__date__="Jan 17 2018"

import re,sys

input_file = str(sys.argv[1])
putput_file = str(sys.argv[2])
# input_file = 'webpages.txt'
# putput_file = 'result.txt'

def open_file(input_file):
    f = open(input_file, 'r')

    html_list = []
    for l in f.readlines():
        html_list.append(l)
    f.close()

    return html_list

def search(html_list):

    email_list=[]
    for str_ in html_list:

        #take the tags out
        content = re.sub("<[^>]*>","",str_)

        #get the raw email data
        email_raw = re.search("([^@\s]+)(\s+/*\[*at/*\]?\s|\s*@@?\s*)(\w+)(\s/*\[*dot/*\]*\s|\s*\.\s*)([^@\s]+)",content)

        #format the raw email data
        if email_raw != None:
            email = email_raw.group(1)+ "@" + email_raw.group(3) + '.' + email_raw.group(5)
            email_list.append(email)
        else:
            email_list.append(str(email_raw))

    return email_list


def save_result(putput_file,email):

    outfile = open(putput_file, 'w')
    for each in email:
        outfile.write("{}\n".format(each))
    outfile.close()

def test(email):
    f = open('trial-pages.emails.txt', 'r')
    result_list=[]
    for l in f.readlines():
        result_list.append(l)
    f.close()

    matches = 0
    i=0
    for g, t in zip(email, result_list):
        i=i+1
        g=g+'\n'
        if str(g) == str(t):
            matches += 1
        else:
            print(g,t)
    print(matches)

def test_one_webpage(html_list,num):
    email_list=[]
    str_=html_list[num]
    #take the tags out
    content = re.sub("<[^>]*>","",str_)
    print('content:',content)
    email_raw = re.search("([^@\s]+)(\s+/*\[*at/*\]?\s|\s*@@?\s*)(\w+)(\s/*\[*dot/*\]*\s|\s*\.\s*)([^@\s]+)",content)
    if email_raw != None:
        print(email_raw.group(0))
    else:
        print(email_raw)
    return email_list

# run webpages code
html_list=open_file(input_file)
email=search(html_list)
save_result(putput_file,email)
# test_one_webpage(html_list,9791)


# run trial code
# html_list=open_file(input_file)
# email=search(html_list)
# save_result(putput_file,email)
# test(email)
