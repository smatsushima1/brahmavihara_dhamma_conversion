
import os
from bs4 import BeautifulSoup as bsp
import requests as rq
import time


###############################################################################
# Start timer for functinos
def start_function(func_name):
    start_time = time.time()
    print('\n' + ('#' * 80))
    print('Function: %s\nStarting...' % (func_name))
    return start_time


# End timer for functions
def end_function(start_time):
    end_time = time.time() - start_time
    if end_time > 60:
        res = end_time / 60
        res_spl = str(res).split('.')
        mins = res_spl[0]
        secs = round(float('.' + res_spl[1]) * 60, 3)
        print('''Function finished in %s' %s"''' % (mins, secs))
    else:
        print('Function finished in %s"' % round(time.time() - start_time, 3))


###############################################################################
# This method is much more complicated and doesn't have all headers
# bvd088 coded headers with b tags and not in p tags for some reason
def pull_all():
    start_time = start_function('pull_html')
    # Open file
    hdoc = open('brahmavihara_dhamma_html_complete.html', 'w', encoding = 'utf8')
    pull_html('http://www.buddhanet.net/brahmaviharas/', '')
    hdoc.close()
    end_function(start_time)
    
    
def pull_html(haddress, hfile):
    print('Working: ' + haddress + hfile)
    # Open the url and save it as an html object; hdr is required due to 403 errors
    hdr = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}
    hres = rq.get(haddress + hfile, headers = hdr).text
    # Turn it into html
    soup = bsp(hres, 'html.parser')
    # All text and links are in paragraphs
    htext = soup.find_all('p')
    # For all p tags, search to see if they have hrefs
    for i in htext:
        try:
            find_a = i.find_all('a')
            # If there is an a tag with an href, then go to it
            if len(find_a) > 1:
                for j in find_a:
                    pull_html(haddress, j.attrs['href'])
            # If there are no a tags after going to the href link, then one must be in a text file
            else:
                add_html(str(i))
        # In the event there is text but no href links, pass
        except AttributeError:
            pass


def add_html(html_text):
    adoc = open('brahmavihara_dhamma_html_complete.html', 'a', encoding = 'utf8')
    adoc.writelines(html_text)


# Much simpler, hard coding it in; missing bvg file
def html_dev():
    start_time = start_function('pull_html2')
    hdoc = open('brahmavihara_dhamma_html_complete.html', 'w', encoding = 'utf8')
    # All files with text have three digit numbers and start with bvd
    for i in range(118):
        # Include leading zeroes
        haddress = 'http://www.buddhanet.net/brahmaviharas/bvd' + "{:03d}".format(i) + '.htm'
        print('Working: ' + haddress)        
        hdr = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}
        hres = rq.get(haddress, headers = hdr).text
        # Turn it into html
        soup = bsp(hres, 'html.parser')
        # All text and links are in paragraphs
        for j in soup.find_all('table'):
            adoc = open('brahmavihara_dhamma_html_complete.html', 'a', encoding = 'utf8')
            # Borders that are "0" are the footers, so this skips them
            if j.attrs['border'] != '0':
                adoc.writelines(str(j))
    hdoc.close()
    end_function(start_time)
        

#pull_all()
html_dev()