import scrapy
import MySQLdb
import json

class CrashSpider(scrapy.Spider):
    name = "crash"

    def initDatabase(self):
        with open('config.json') as config:    
            data = json.load(config)
            self.database = MySQLdb.connect(host = data['host'], user = data['user'], passwd = data['password'], db = data['db'], port = 3306)

    def start_requests(self):
        self.initDatabase()
        results = self.get_unfinished_sign()
        for result in results:
            url = result[2] or result[1]
            yield scrapy.Request(url=url, callback=self.parse, meta={'sign':result[0]})

    def parse(self, response):
        sign = response.meta.get('sign')
        links = response.css('#reports tbody tr td a::attr(href)')
        texts = response.css('#reports tbody tr td a::text')
        for i in range(len(links)):
            self.insert(texts[i].extract().strip(), sign, response.urljoin(links[i].extract()))
        self.database.commit()
        paginations = response.css('p.pagination a')
        nextlink = ''
        for pagination in paginations:
            if 'next' in pagination.extract():
                nextlink= pagination.css('a::attr(href)').extract_first()
        if nextlink:
            nextlink = response.urljoin(nextlink)
            self.update_last(sign, nextlink)
            yield scrapy.Request(nextlink, callback=self.parse, meta={'sign': sign})
        else:
            self.done_with_sign(sign)

    def get_unfinished_sign(self):
        cursor = self.database.cursor()       
        cursor.execute('''SELECT sign,url,last_crawled_crash_url
        FROM signature
        WHERE 
        sign in 
            ( SELECT distinct(sign) FROM bugs)
        AND crawled_crash_list = false 
        ORDER BY signature.sign ASC;''')
        #cursor.execute('SELECT sign, url from signature where  crawled_crash_list = false;')
        results = cursor.fetchall()
        return results

    def insert(self, id, sign, link):
        cursor = self.database.cursor()
        cursor.execute("""INSERT IGNORE into crash(id, sign, url) values (%s,%s,%s);""",(id, sign, link))

    def update_last(self, sign, link):        
        cursor = self.database.cursor()
        cursor.execute("""UPDATE signature set last_crawled_crash_url = %s where sign = %s;""",[link, sign])
        self.database.commit()

    def done_with_sign(self, sign):
        cursor = self.database.cursor()  
        cursor.execute("""UPDATE signature set crawled_crash_list = true where sign = %s;""",[sign])
        self.database.commit()