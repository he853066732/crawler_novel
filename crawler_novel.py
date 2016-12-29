# encoding=utf8

#爬小说
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import urllib
import urllib2
import re

file_path='f:/txt'
file_name='a.txt'

def get_html_str_from_url(url):
    '通过URL来获得html，返回一个字符串'
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read()
    except urllib2.URLError, e:
        print "get html error", e.reason
        return None

def write_file(html,file_path,file_name):
    '从html中获得文本，写入文件中'
    txt_file = open(file_path + '/'+file_name, 'a')
    content = html.decode('utf-8','ignore')
    pattern = re.compile(u'<div class="bookname">.*?<h1>(.*?)</h1>.*?上一章</a>.*?<a href="(.*?)">章节列表</a>.*?<a href="(.*?)">下一章</a>.*?<div id="content"><script>.*?</script>(.*?)</div>', re.S)
    items = re.findall(pattern, content)
    txt=''
    global url_page
    global url_book
    for item in items:
        br=re.sub('<br />','\n',item[3])
        txt=re.sub('&nbsp;',' ',br)
        url_book=item[1]
        url_page=item[2]

        txt_file.write('\n\n\n标题：   '+item[0] + '\n\n\n')
    txt_file.write(txt)
    txt_file.close()

num_book=raw_input('input num of book:')
num_page=raw_input('input num of page:')

url_book='/book/'+str(num_book)+'/'
url_page=str(num_page)+'.html'

i=1

while(url_book!=url_page):
    html=None
    while html==None:
        html=get_html_str_from_url('http://www.biquge.la'+url_book+url_page)
    html=html.decode('gbk','ignore')

    write_file(html, file_path, file_name)
    print 'writing :', i
    i+=1

print 'success'
