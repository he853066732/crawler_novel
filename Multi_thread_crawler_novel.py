# encoding=utf8

# 多线程爬小说
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
import re
import threading
import time
import chardet

file_name='f:/txt/'
url_list=[]
uni_now='gbk'

class cl_mythread (threading.Thread):
    '多线程的类'

    def __init__(self,id):
        threading.Thread.__init__(self)
        self.id=id
        self.num_now_page=0
        self.bre=True

    def run(self):
        global uni_now
        global num_thread
        global num_writed
        global num_name_list
        while self.bre:

            if num_writed<num_name_list:

                if writed_list[self.num_now_page]:
                    lock_num_writed.acquire()
                    num_writed+=1
                    self.num_now_page=num_writed
                    print self.id,' get ',self.num_now_page
                    lock_num_writed.release()
                    html=None
                    while html==None:
                        html = get_html_str_from_url('http://www.biquge.la' + url_book + name_list[self.num_now_page - 1])
                    html=html.decode('gbk','ignore')
                    content = html.decode('utf-8','ignore')
                    pattern = re.compile(u'<div class="bookname">.*?<h1>(.*?)</h1>.*?<div id="content"><script>.*?</script>(.*?)</div>',re.S)
                    items = re.findall(pattern, content)
                    for item in items:
                        br = re.sub('<br /><br />', '\n', item[1])
                        txt = re.sub('&nbsp;', ' ', br)
                        title=item[0]
            while writed_list[self.num_now_page - 1] and writed_list[self.num_now_page]==False:
                self.bre=True
                lock_file_writing.acquire()
                txt_file=open(file_name,'a')
                txt_file.write(('\n\n\n'+title + '\n\n\n'))
                txt_file.write(txt)
                writed_list[self.num_now_page]=True
                print self.id,' writing ',self.num_now_page
                if self.num_now_page>num_name_list-num_thread:
                    self.bre=False
                txt_file.close()
                lock_file_writing.release()


lock_num_writed=threading.Lock()

lock_file_writing=threading.Lock()

lock_print=threading.Lock()

file_path=raw_input('input the name of sava:')

file_name=file_name+file_path

num_book=raw_input('input book num:')

url_book='/book/'+num_book+'/'

file=open(file_name,'w')
file.close()

def get_html_str_from_url(url):
    '通过URL来获得html，返回一个字符串'
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read()
    except urllib2.URLError, e:
        print "get html error", e.reason
        return None

def init():
    html=get_html_str_from_url('http://www.biquge.la'+url_book).decode('gbk','ignore')
    content = html.decode('utf-8','ignore')
    pattern = re.compile(u'<dl>.*?</dl>',re.S)
    str_all_name = re.search(pattern, content)
    pattern2 = re.compile(u'<dd><a href="(.*?)">', re.S)
    name_list=re.findall(pattern2,str_all_name.group())
    return name_list

name_list=init() # 章节名列表

num_name_list=len(name_list) # 章节的数量

num_writed=0 # 已经写入的章节数量

writed_list=[True]

num_thread=int(raw_input('input num of thread:'))

j=0
while j<=num_name_list:
    writed_list.append(False)
    j+=1

i=0
mythread_list=[]
while i<num_thread:
    mythread=cl_mythread(i+1)
    mythread_list.append(mythread)
    mythread_list[i].start()
    i+=1

for thread in mythread_list:
    thread.join()
print 'success'

