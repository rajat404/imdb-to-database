import sqlite3
import requests
import lxml.html
import timeit

def main():
    start = timeit.default_timer()
    con = sqlite3.connect('')    #give full path to your sqlite database here
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS "movdat" (name TEXT,imdb_id TEXT,year INT,rating REAL,poster TEXT,genres TEXT,summary     TEXT,runtime TEXT,director TEXT,PRIMARY KEY (imdb_id))""")
    
    num=input("Enter the total number of movies you want in the database: ")

    for j in range(1,num,50):
        url="http://www.imdb.com/search/title?at=0&sort=moviemeter,asc&start="+str(j)+"&title_type=feature"
        movpath = lxml.html.document_fromstring(requests.get(url).content)
        for i in range(2,52):
            mov = movpath.xpath('//*[@id="main"]/table/tr['+str(i)+']/td[3]/a/@href')
            name=movpath.xpath('//*[@id="main"]/table/tr['+str(i)+']/td[3]/a/text()')
            print j+i-2,name,mov

            imid=mov[0]    
            hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com" + imid).content)
            imid=imid[:-1]
            imdb_id=imid[7:]
                    
            
            try:
                name = hxs.xpath('//*[@id="overview-top"]/h1/span[1]/text()')[0].strip()
            except IndexError:
                name = ""
            try:
                year = hxs.xpath('//*[@id="overview-top"]/h1/span[2]/a/text()')[0].strip()
            except IndexError:
                try:
                    year = hxs.xpath('//*[@id="overview-top"]/h1/span[3]/a/text()')[0].strip()
                except IndexError:
                    year = ""
            try:
                runtime = hxs.xpath('//*[@id="overview-top"]/div[2]/time/text()')[0].strip()
            except IndexError:
                runtime = ""
            try:
                genre = hxs.xpath('//*[@id="overview-top"]/div[2]/a/span/text()')
                for item in genre:
                    genres=genre[0]+','
                    genres=genres+item+','
                    
            except IndexError:
                genres = ""
            try:
                rating = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/strong/span/text()')[0]
            except IndexError:
                rating = ""
            try:
                summary = hxs.xpath('//*[@id="overview-top"]/p[2]/text()')[0].strip()
            except IndexError:
                summary = ""
            try:
                director = hxs.xpath('//*[@id="overview-top"]/div[4]/a/span/text()')[0].strip()
            except IndexError:
                director = ""
            try:
                poster = hxs.xpath('//*[@id="img_primary"]/div/a/img/@src')[0]
            except IndexError:
                poster = ""
            det=[]
            det.extend([name,imdb_id,year,rating,poster,genres,summary,runtime,director])
            det=tuple(det,)

            cur.execute("INSERT INTO movdat VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", det)
            con.commit()
            
    stop = timeit.default_timer()
    print'\n'
    print"Running time:",stop - start


if __name__ == '__main__':
    main()

                




