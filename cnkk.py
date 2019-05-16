import requests
from lxml import etree
import re
import time
import random
import pymysql
s  = requests.session()
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
'Cookie':'Ecp_ClientId=8190516151201268101; RsPerPage=20; cnkiUserKey=e4e2cbfc-c161-1ca0-d1d2-81a78658c058; Ecp_IpLoginFail=190516223.106.167.80; _pk_ses=*; ASP.NET_SessionId=lyovfbltfg44hsrcgw3pdm3t; SID_kns=123118; Hm_lvt_bfc6c23974fbad0bbfed25f88a973fb0=1558003184,1558004113; SID_klogin=125144; KNS_SortType=; Hm_lpvt_bfc6c23974fbad0bbfed25f88a973fb0=1558004359'
}
db = pymysql.connect("localhost", "root", "123456", "test0")
cursor = db.cursor()

def parse_detail(url):
    # urlc = 'http://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&dbname=CJFDTEMP&filename=XDFC20190404003'

    res = s.get(url, headers=headers)
    # print(res.text)
    e = etree.HTML(res.text)
    text = e.xpath('//*[@id="mainArea"]//h2/text()')[0]
    isbn = e.xpath('//*[@class="sourinfo"]/p[4]/text()')[0].strip()
    authors = e.xpath('//*[@class="author"]/span')
    organs = e.xpath('//*[@class="orgn"]/span')
    authorlist = []
    organlist = []
    for author in authors:
        authorname = author.xpath('a/text()')[0]
        # print(authorname)
        authorlist.append(authorname)

    for organ in organs:
        organname = organ.xpath('a/text()')[0]
        # print(organname)
        organlist.append(organname)
    authors = ','.join(authorlist)
    organs = ','.join(organlist)
    # print(text, isbn,authors,organs)
    sql = """ INSERT INTO CNKI(title,isbn,author,organ) VALUES ('%s','%s','%s','%s')"""%(text,isbn,authors,organs)
    try:
        cursor.execute(sql)
        db.commit()
        print('successful')
    except:
        db.rollback()

for i in range(1,21):
    url = 'http://kns.cnki.net/kns/brief/brief.aspx?curpage={}&RecordsPerPage=20&QueryID=5&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx&isinEn=1&'.format(i)
    r = s.get(url,headers=headers)
    print(url)
    r.encoding='utf-8'
    n = re.findall(r'&FileName=(.*?)&',r.text)
    url2 = 'http://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&dbname=CJFDTEMP&filename='
    for url in n:
        url3 = url2+url
        print(url3)
        time.sleep(1)
        try:
            parse_detail(url3)
        except:
            pass
cursor.close()
db.close()


# e.xpath('//table[@class="GridTableContent"]/tbody/tr[@bgcolor]')
