import scrapy
import MySQLdb
import json
import datetime

class CrashSpider(scrapy.Spider):
    name = "bug"

    def initDatabase(self):
        with open('config.json') as config:    
            data = json.load(config)
            self.database = MySQLdb.connect(host = data['host'], user = data['user'], passwd = data['password'], db = data['db'], port = 3306)

    def start_requests(self):
        self.initDatabase()
        bug_ids = self.get_unfinished_bugs()
        for bugid in bug_ids:
            url = "https://bugs.documentfoundation.org/show_bug.cgi?ctype=xml&id=%s"%(bugid)
            yield scrapy.Request(url=url, callback=self.parse, meta={'id':bugid})

    def parse(self, response):
        bugid = response.meta.get('id')
        data = self.get_data(response)
        self.update(bugid, data)   

    def get_data(self, response):
        data = {}
        data["creation_time"] = self.parseDate(response.css("creation_ts::text").extract_first());
        data["last_modified"] = self.parseDate(response.css("delta_ts::text").extract_first());
        data["priority"] = response.css("priority::text").extract_first();
        data["severity"] = response.css("bug_severity::text").extract_first();
        data["cc_count"] = str(len(response.css("cc")))
        data["comment_count"] = str(len(response.css("commentid")))
        data["attachment_count"] = str(len(response.css("attachid")))
        data["status"] = response.css("bug_status::text").extract_first()
        data["resolution"] = response.css("resolution::text").extract_first() 
        data["duplicate_of"] = response.css("dup_id::text").extract_first() 
        return data

    def get_unfinished_bugs(self):
        cursor = self.database.cursor()       
        cursor.execute('SELECT id FROM bugs WHERE create_time is null ')
        results = cursor.fetchall()
        return results

    def update(self, id, data):        
        cursor = self.database.cursor()
        cursor.execute("""
            UPDATE bugs SET
                create_time = %s,
                last_modified = %s,
                priority = %s,
                severity = %s,
                cc_count = %s,
                comment_count = %s,
                attachment_count = %s,
                status = %s,
                resolution = %s,
                duplicate_of = %s
            where id = %s;""",
            [
            data["creation_time"],
            data["last_modified"],
            data["priority"],
            data["severity"],
            data["cc_count"],
            data["comment_count"],
            data["attachment_count"],
            data["status"],
            data.get("resolution"),
            data.get("duplicate_of"),
            id
            ])
        self.database.commit()

    def parseDate(self, val):
        #2016-11-30 17:06:00 +0000
        #%Y-%m-%d %H:%M:%S %z
        val = val.split(" +")[0]
        val = datetime.datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
        return val
        