import scrapy
import MySQLdb
import json

class SignatureSpider(scrapy.Spider):
    name = "sign"

    def initDatabase(self):
        #   Please set the database host, user and password here
        with open('config.json') as config:    
            data = json.load(config)
            self.database = MySQLdb.connect(host = data['host'], user = data['user'], passwd = data['password'], db = data['db'], port = 3306)

    def start_requests(self):
        urls = [
            'https://crashreport.libreoffice.org/stats/version/5.2.4.2?limit=20000&days=28'
        ]
        self.initDatabase()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        rows = response.css("#data-table")[0].css("tbody")[0].css("tr")
        for row in rows:
            signature_name = row.css("a:first_child::text")[0].extract().strip()
            urlred = row.css("a:first_child::attr('href')")[0].extract()
            urlbugs = row.css("a.bug_link::attr('href')");
            cursor = self.database.cursor()
            cursor.execute("""INSERT IGNORE into signature(sign, url) values (%s,%s);""",(signature_name, response.urljoin(urlred)))
            for bug in urlbugs:
                buge = bug.extract()
                bugid = buge.split("id=")[1]
                cursor.execute("""INSERT IGNORE into bugs(id,sign,url) values (%s,%s,%s);""",(bugid,signature_name,buge))
            self.database.commit()
        self.database.close()