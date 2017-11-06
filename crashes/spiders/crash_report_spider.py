import scrapy
import MySQLdb
import json
import datetime


class CrashSpider(scrapy.Spider):
    name = "crashreport"

    def initDatabase(self):
        with open('config.json') as config:    
            data = json.load(config)
            self.database = MySQLdb.connect(host = data['host'], user = data['user'], passwd = data['password'], db = data['db'], port = 3306)

    def start_requests(self):
        self.initDatabase()
        results = self.get_unfinished_buggy_crashreports()
        for result in results:
            yield scrapy.Request(url=result[1], callback=self.parse, meta={'sign':result[2], 'id': result[0]})

    def parse(self, response):
        sign = response.meta.get('sign')
        id = response.meta.get('id')
        data = self.get_data(response)
        self.done_with_crashreport(id, data)

    def get_unfinished_buggy_crashreports(self):
        cursor = self.database.cursor()       
        cursor.execute("""
            SELECT crash.id, crash.url, crash.sign FROM crash 
            WHERE crash.crash_date IS NULL and
            crash.sign in 
            ( SELECT signature.sign FROM signature, bugs WHERE signature.sign=bugs.sign and bugs.id IS NOT NULL) LIMIT 1000;
            """)
        results = cursor.fetchall()
        return results

    def done_with_crashreport(self, id, data):
        cursor = self.database.cursor()  
        cursor.execute("""
            UPDATE crash SET 
            crash_date = %s, 
            os_name = %s,
            os_version = %s,
            cpu_info = %s,
            build = %s,
            version = %s,
            reason = %s,
            opengldriver = %s,
            opengldevice = %s
            where id = %s;""",
            [data["crash_date"], data["os_name"], data["os_version"], data["cpu_info"], data["build"], data["version"], data["reason"], data["opengldriver"], data["opengldevice"], id])
        self.database.commit()

    def get_data(self, response):
        dic = {}
        self.get_details(response, dic)
        self.get_opengl_dets(response, dic)
        return dic

    def get_details(self, response, dic):
        rows = response.css("#details table.record.data-table tr")
        dic_def = {
            "Version" : "version",
            "Upload Time" : "crash_date",
            "OS" : "os_name",
            "OS details" : "os_version",
            "CPU Info" : "cpu_info",
            "Build Architecture" : "build",
            "Crash Reason" : "reason"
        }
        for row in rows:
            key = row.css("th::text").extract_first().strip()
            val = row.css("td::text").extract_first().strip()
            if(key in dic_def):
                if(dic_def[key] == "version"):
                    val = val.split(":")[1].strip()
                elif(dic_def[key] == "crash_date"):
                    val = self.parseDate(val)
                dic[dic_def[key]] = val

    def get_opengl_dets(self, response, dic):
        rows = response.css("#metadata table.record.data-table tr")
        dic_def = {
            "OpenGLDriver" : "opengldriver",
            "OpenGLDevice" : "opengldevice"
        }
        for row in rows:
            key = row.css("th::text").extract_first().strip()
            val = row.css("td::text").extract_first().strip()
            if(key in dic_def):
                dic[dic_def[key]] = val

    def parseDate(self, val):
        val = val.replace("p.m.", "pm").replace("a.m.","am").replace(".","")
        vals = val.split(" ")
        vals[0] = vals[0][:3] #Nove Nov
        val = " ".join(vals)

        formats = ['%b %d, %Y, %I:%M %p', '%b %d, %Y, %I %p']
        for formt in formats:
            try:
                val = datetime.datetime.strptime(val, formt)
                return val
            except ValueError:
                pass
        try:
            return datetime.datetime.strptime(val.split(",")[0], '%b %d')
        except:
            pass
        raise ValueError("cant parse %s"%(val))
