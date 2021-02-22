import csv

class csvReader:
    filename = 'recipes.csv'
    reader = None

    # プライベートメソッド
    async def __read(self):
        csvfile = open(self.filename, newline='')
        self.reader = csv.DictReader(csvfile) 

    # 番号指定したブクマを呼び出す
    async def readFavorite(self, num):
        await self.__read()
        f = self.reader
        target = map(lambda x: x["記事URL"], filter(lambda x: x["記事番号"] == str(num), f))
        returnString = ""
        for string in list(target):
            returnString += string
        return returnString if returnString != "" else "Not found your number"

    # タグひとつで検索
    async def searchTag(self, tag):
        await self.__read()
        f =self.reader
        tagNum = ["タグ1","タグ2","タグ3","タグ4","タグ5"]
        returnString = ""
        for row in f:
            tagList = []
            [tagList.append(row[value]) for value in tagNum]
            if tag in tagList:
                returnString += row["記事URL"]+"\n"
        return returnString if returnString != "" else "Not found your tag"

    # 複数のタグで検索(完全一致)
    async def searchTags(self, tags):
        await self.__read()
        f = self.reader
        tagNum = ["タグ1","タグ2","タグ3","タグ4","タグ5"]
        returnString = ""
        for row in f:
            tagList = []
            [tagList.append(row[value]) for value in tagNum]
            if set(tags) <= set(tagList):
                returnString += row["記事URL"]+"\n"
        return returnString if returnString != "" else "Not found your tags"


    # 全てのブクマの番号とタイトルを見せる
    async def showFavList(self):
        await self.__read()
        f = self.reader
        FavList = "記事番号,記事URL"
        for row in f:
            FavList += "\n"+row["記事番号"] + "," + row["記事URL"]
        return FavList
        
    
    # あるブクマの全ての要素を見せる
    async def showFavAll(self, num):
        await self.__read()
        f = self.reader
        target = None
        try:
            target = list(filter(lambda x: x["記事番号"] == str(num), f))[0]
        except IndexError:
            return "Not found your number"
        elements = ""
        for value in target.values() :
            elements += value+"\n" if value != "" else ""
        return elements

    # 現存する全てのタグを表示する
    async def showAllTag(self):
        await self.__read()
        f = self.reader
        tagNum = ["タグ1","タグ2","タグ3","タグ4","タグ5"]
        tagSet = set()
        for row in f:
            [tagSet.add(row[value]) for value in tagNum]
        tags = ""
        for tag in tagSet:
            tags += tag+"\n"
        return tags

# 発見して返すのはURL