# coding: utf-8
import urllib2;
from HTMLParser import HTMLParser

def conv_to_info(data):
    sem_info = {
        "title"  : data[0],
        "name"   : data[1],
        "date"   : data[2],
        "time"   : data[3],
        "place"  : data[4],
        "number" : data[5],
        "link"   : data[6]}
    return sem_info

def show_info(info):
    print info["number"]
    print info["title"]
    print info["name"]
    print info["date"], info["time"]
    print info["place"]
    print info["link"]

class ExtractEvents(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_seminar_info_section = False
        self.is_h3 = False
        self.is_p  = False
        self.data  = [] # パース中にデータを貯めるバッファ
        
    def handle_starttag(self, tagname, attribute):
        if tagname == "h3":
            self.is_h3 = True
        if tagname == "p":
            self.is_p = True
        if tagname == "a": #イベント詳細へのリンクを表示
            if self.is_seminar_info_section and self.is_p:
                for i in attribute:
                    if i[0].lower() == "href":
                        self.is_p = False # リンク以降の文字列は表示しない
                        self.data.append("http://www.bs.s.u-tokyo.ac.jp/" + i[1])
                        show_info(conv_to_info(self.data)) # 取得したデータを表示
                        self.data = [] # データバッファを空に
            
    def handle_data(self, data):
        if self.is_h3:            
            if data == "講演会・セミナー予定":
                self.is_seminar_info_section = True
            if data == "過去の講演会・セミナー":
                self.is_seminar_info_section = False
                
        if self.is_seminar_info_section and self.is_p:
            buf = data.replace('&nbsp;','').strip()
            if len(buf) > 0: # 空行除去してデータを追加
                self.data.append(buf)            
            
    def handle_endtag(self, tagname):
        if tagname == "h3":
            self.is_h3 = False
        if tagname == "p":
            self.is_p = False
                
def main():
    url = "http://www.bs.s.u-tokyo.ac.jp/event/"                    
    htmldata = urllib2.urlopen(url)

    parser = ExtractEvents()
    parser.feed(htmldata.read())

    parser.close()
    htmldata.close()

if __name__ == "__main__":
    main();
