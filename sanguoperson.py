#coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import json
import codecs

def download(url,pageno):
    postparam={'pageno':pageno,'callback':'jQuery111304542359812369223_1513070966991','_':15130709669}
    headers={'Referer':url,
    'Connection':'keep-alive',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Accept-Encoding':'gzip, deflate',
    'X-Requested-With':'XMLHttpRequest',
    'Accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
    html=requests.get(url,data=postparam,headers=headers).text
    return html

def jiexi(html):
    sanguo=[]
    soul=html.split('soul:')[1].split('})')[0]
    soul=soul.encode('unicode_escape')
    soul=re.sub(r'\\\\',r'\\',soul)
    soul=soul.decode('unicode-escape')
    soul=soul.encode('utf-8')
    soul=re.sub('cata:','\'cata\':',soul)
    soul=re.sub('content:','\'content\':',soul)
    soul=re.sub('id:','\'id\':',soul)
    soul=re.sub('jiguan:','\'jiguan\':',soul)
    soul=re.sub('name:','\'name\':',soul)
    soul=re.sub('pic:','\'pic\':',soul)
    soul=re.sub('pinyin:','\'pinyin\':',soul)
    soul=re.sub('sex:','\'sex\':',soul)
    soul=re.sub('shengsi:','\'shengsi\':',soul)
    soul=re.sub('votep:','\'votep\':',soul)
    soul=re.sub('zhengshi:','\'zhengshi\':',soul)
    soul=re.sub('zi:','\'zi\':',soul)
    soul=re.sub('&nbsp; ','',soul)
    soul=re.sub('\'','"',soul)
    news=json.loads(soul)
    for new in news:
        n={'cata':new['cata'].encode('utf-8'),
        'content':new['content'].encode('utf-8'),
        'id':new['id'],
        'jiguan':new['jiguan'].encode('utf-8'),
        'name':new['name'].encode('utf-8'),
        'pic':new['pic'].encode('utf-8'),
        'pinyin':new['pinyin'].encode('utf-8'),
        'sex':new['sex'].encode('utf-8'),
        'shengsi':new['shengsi'].encode('utf-8'),
        'votep':new['votep'].encode('utf-8'),
        'zhengshi':new['zhengshi'].encode('utf-8'),
        'zi':new['zi'].encode('utf-8')}
        sanguo.append(n)
    return sanguo

def main():
    with codecs.open('sanguo','wb') as sg:
        url='http://www.e3ol.com/biography/inc_ajax.asp?types=index&a1=&a2=&a3=&a4=&a7=&a6=&a5=&key='
        pageno=1
        sanguo=[]
        sgproperty=[]
        sgproperty=['排名',
        '姓名',
        '拼音',
        '表字',
        'id',
        '性别',
        '主效',
        '生卒',
        '正史/虚构',
        '头像',
        '籍贯',
        '事件']
        yppt=re.search(r'\[(.*)\]',str(sgproperty)).group(1)
        ppt=re.sub('\'','',yppt).decode('string_escape')
        sg.write(ppt)
        sg.write('\n')
        while pageno<226:
            html=download(url,pageno=pageno)
            sanguo.append(jiexi(html))
            pageno=pageno+1
        for sglist in sanguo:
            for sgperson in sglist:
                listsg=[]
                listsg=[sgperson['votep'],
                sgperson['name'],
                sgperson['pinyin'],
                re.sub('字：','',sgperson['zi']),
                sgperson['id'],
                sgperson['sex'],
                re.sub('主效：','',sgperson['cata']),
                re.sub('\)','',re.sub('生卒\(','',sgperson['shengsi'])),
                re.sub('人物','',sgperson['zhengshi']),
                re.sub('/biography','www.e3ol.com/biography',sgperson['pic']),
                re.sub('籍贯：','',sgperson['jiguan']),
                sgperson['content']]
                ystrsg=re.search(r'\[(.*)\]',str(listsg)).group(1)
                strsg=re.sub('\'','',ystrsg).decode('string_escape')
                strsg=re.sub(' www','www',strsg)
                sg.write(strsg)
                sg.write('\n')
        print '\n\n\n            ','Well done!\n\n\n'

if __name__ == '__main__':
    main()
