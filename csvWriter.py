import csv
import requests
from bs4 import BeautifulSoup as bs4
import os
from socket import inet_aton
import datetime

class csvWriter:
    filename = 'recipes.csv'
    writer = None
    reader = None
    num = 0
    firstRow = ['記事番号', '記事タイトル', '記事URL', 'タグ1', 'タグ2', 'タグ3', 'タグ4', 'タグ5', '作成日時']

    # コンストラクタ　オブジェクト作成時にcsvの第1行を埋める処理
    def __init__(self):
        if os.path.isfile(self.filename):
            read = open(self.filename, 'r')
            self.reader = csv.reader(read, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
            f = open(self.filename, 'a') 
            self.writer = csv.writer(f)
            l = [row for row in self.reader]
            self.num = len(l) -1
        else:
            f = open(self.filename, 'w', newline='') 
            self.writer = csv.writer(f)
            self.writer.writerow(self.firstRow)
        read = open(self.filename, 'r')
        self.reader = csv.reader(read, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        super().__init__()

    # 読み込みをアップデートするメソッド　内部処理に用いる
    def readerUpdate(self):
        if os.path.isfile(self.filename):
            read = open(self.filename, 'r')
            self.reader = csv.reader(read, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
            f = open(self.filename, 'a') 
            self.writer = csv.writer(f)
            l = [row for row in self.reader]
            self.num = len(l) -1
        else:
            f = open(self.filename, 'w', newline='') 
            self.writer = csv.writer(f)
            self.writer.writerow(self.firstRow)
        read = open(self.filename, 'r')
        self.reader = csv.reader(read, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    # ブックマークを追加するメソッド
    # url : 対象のurl(string)　tags : タグ一覧(string list)
    async def addFavorite(self, url, tags):
        judge = self.ipcheck(str(url))
        if judge:
            return 'IP ha YAMETE'
        url = str(url)
        self.readerUpdate()
        self.num += 1
        r = requests.get(url)
        soup = bs4(r.content, 'lxml')
        title = str(soup.find('title'))
        title = title.lstrip('<title>')
        title = title.rstrip('</title>')
        res = False
        msg = ''

        contents = [str(self.num), str(title), str(url)]
        tagnum = 0
        for item in tags:
            contents.append(str(item))
            tagnum += 1
        if tagnum > 5:res=False
        else:
            while tagnum < 5:
                contents.append('')
                tagnum += 1
            res = True
            contents.append(str(datetime.datetime.now()))
        self.writer.writerow(contents)
        if res:
            msg = 'succeeded in adding recipe'
        else:
            msg = 'error : tags are more than limit '
        self.readerUpdate()
        return msg

    # ブックマークを削除するメソッド
    # num : 削除するブックマークの記事番号(int or string)
    async def deleteFavorite(self, num):
        self.readerUpdate()
        newLists = []
        res = False
        l = [row for row in self.reader]
        msg = ''
        for row in l:
            if row[0] == '記事番号':
                newLists.append(row)
            elif str(row[0]) == str(num):
                newLists.append(['', '', '', '', '', '', '', '', ''])
                res = True
            else:
                newLists.append(row)
        if res:
            w = open(self.filename, 'w', newline='')
            rewriter = csv.writer(w)
            rewriter.writerows(newLists)
            msg = 'succeeded in deleting recipe'
        else:
            msg = 'error: '+ str(num) + ' was not found'
        self.readerUpdate()
        return msg

    # タグを追加するメソッド
    # num : 追加する記事番号(int or string)　tag : 追加するタグ(string)
    async def addTag(self, num, tag):
        self.readerUpdate()
        newLists = []
        tag = str(tag)
        res = False
        l = [row for row in self.reader]
        msg = ''

        for row in l:
            if row[0] == '記事番号':
                newLists.append(row)
            elif str(row[0]) == str(num):
                if row[3] == '':
                    newLists.append([row[0], row[1],row[2], tag, row[4], row[5], row[6], row[7], row[8]])
                    res = True
                elif row[4] == '':
                    newLists.append([row[0], row[1],row[2], row[3], tag, row[5], row[6], row[7], row[8]])
                    res = True 
                elif row[5] == '':
                    newLists.append([row[0], row[1],row[2], row[3], row[4], tag, row[6], row[7], row[8]])
                    res = True
                elif row[6] == '':
                    newLists.append([row[0], row[1],row[2], row[3], row[4], row[5], tag, row[7], row[8]])
                    res = True
                elif row[7] == '':
                    newLists.append([row[0], row[1],row[2], row[3], row[4], row[5], row[6], tag, row[8]])
                    res = True
                else:
                    newLists.append(row)
                    msg = 'full'
            else:
                newLists.append(row)
        if res:
            w = open(self.filename, 'w', newline='')
            rewriter = csv.writer(w)
            rewriter.writerows(newLists) 
            msg = 'succeed in adding tag: '  + str(tag)
        elif msg != '':
            msg = 'the list is full of tags'
        else:
            msg = 'error: '+ str(num) + ' does not exist' 
        self.readerUpdate()
        return msg

    # タグを削除するメソッド
    # num :  削除する記事番号(int or string)　tag : 削除するタグ(string) 
    async def deleteTag(self, num, tag):
        self.readerUpdate()
        newLists = []
        tag = str(tag)
        res = False
        l = [row for row in self.reader]
        msg = ''

        for row in l:
            if row[0] == '記事番号':
                newLists.append(row)
            elif str(row[0]) == str(num):
                if row[3] == tag:
                    newLists.append([row[0], row[1],row[2], '', row[4], row[5], row[6], row[7], row[8]])
                    res = True
                elif row[4] == tag:
                    newLists.append([row[0], row[1],row[2], row[3], '', row[5], row[6], row[7], row[8]])
                    res = True 
                elif row[5] == tag:
                    newLists.append([row[0], row[1],row[2], row[3], row[4], '', row[6], row[7], row[8]])
                    res = True
                elif row[6] == tag:
                    newLists.append([row[0], row[1],row[2], row[3], row[4], row[5], '', row[7], row[8]])
                    res = True
                elif row[7] == tag:
                    newLists.append([row[0], row[1],row[2], row[3], row[4], row[5], row[6], '', row[8]])
                    res = True
                else:
                    newLists.append(row)
                    msg = 'tag not'
            else:
                newLists.append(row)
        if res:
            w = open(self.filename, 'w', newline='')
            rewriter = csv.writer(w)
            rewriter.writerows(newLists) 
            msg = 'succeed in deleting tag: '  + str(tag)
        elif msg != '':
            msg = 'tag : ' + str(tag) + ' was not found'
        else:
            msg = 'error: '+ str(num) + ' was not found'
        self.readerUpdate()
        return msg

    # csvをリセットするメソッド
    async def clear(self):
        w = open(self.filename, 'w', newline='')
        rewriter = csv.writer(w)
        self.num = 0
        rewriter.writerow(self.firstRow) 
        self.readerUpdate()
        return 'All cleared'

    # 記事のタグをリセットするメソッド
    # リセットしたい記事番号(int or string)
    async def clearFavoriteTags(self, num):
        self.readerUpdate()
        newLists = []
        res = False
        l = [row for row in self.reader]
        msg = ''
        for row in l:
            if row[0] == '記事番号':
                newLists.append(row)
            elif str(row[0]) == str(num):
                newLists.append([row[0], row[1], row[2], '', '', '', '', '', row[8]])
                res = True
            else:
                newLists.append(row)
        if res:
            w = open(self.filename, 'w', newline='')
            rewriter = csv.writer(w)
            rewriter.writerows(newLists)
            msg = 'succeeded in clearing tags : ' + str(num)
        else:
            msg = 'error: '+ str(num) + ' was not found'
        self.readerUpdate()
        return msg

    # タグの置換を行うメソッド
    # num : 置換したい記事番号(int or str)　deltag : 置換前のタグ(str)　newtag : 置換後のタグ(str)
    async def replaceTags(self, num, deltag, newtag):
        self.readerUpdate()
        newLists = []
        tag = str(deltag)
        res = False
        l = [row for row in self.reader]
        msg = ''

        for row in l:
            if row[0] == '記事番号':
                newLists.append(row)
            elif str(row[0]) == str(num):
                if row[3] == tag:
                    newLists.append([row[0], row[1],row[2], newtag, row[4], row[5], row[6], row[7], row[8]])
                    res = True
                elif row[4] == tag:
                    newLists.append([row[0], row[1],row[2], row[3], newtag, row[5], row[6], row[7], row[8]])
                    res = True 
                elif row[5] == tag:
                    newLists.append([row[0], row[1],row[2], row[3], row[4], newtag, row[6], row[7], row[8]])
                    res = True
                elif row[6] == tag:
                    newLists.append([row[0], row[1],row[2], row[3], row[4], row[5], newtag, row[7], row[8]])
                    res = True
                elif row[7] == tag:
                    newLists.append([row[0], row[1],row[2], row[3], row[4], row[5], row[6], newtag, row[8]])
                    res = True
                else:
                    newLists.append(row)
                    msg = 'tag not'
            else:
                newLists.append(row)

        if res:
            w = open(self.filename, 'w', newline='')
            rewriter = csv.writer(w)
            rewriter.writerows(newLists) 
            msg = 'succeed in replacing tag: '  + str(tag) + ' to ' + str(newtag)
        elif msg != '':
            msg = 'tag : ' + str(tag) + ' was not found'
        else:
            msg = 'error: '+ str(num) + ' was not found'
        self.readerUpdate()
        return msg

    # 表の中身を全て表示するメソッド　確認に使用　Botに実装はしない
    def show(self):
        self.readerUpdate()
        count = 0
        l = [row for row in self.reader]
        for row in l:
            print(row)
            count += 1
        return 'fin'

    # 与えられたURLがIPでないことを確認するメソッド
    def ipcheck(self, url):
        addr = url.lstrip('http://')
        addr = addr.lstrip('https://')
        addr = addr.rstrip('/')
        if ':' in addr[-5:]:
            addr = addr[:-4]
            addr = addr.rstrip(':')
        judge = self.is_valid_ip(addr)
        if judge :
            return True
        elif 'localhost' in addr:
            return True
        else:
            return False

    #与えられた文字列がIPであるかを確認するメソッド
    def is_valid_ip(self, addr):
        try:
            inet_aton(addr)
            return True
        except:
            return False


# written by https://github.com/Sane21