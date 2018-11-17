#!/usr/local/bin/python3
import tornado.ioloop
import tornado.web
import cx_Oracle
import codecs
from tornado.escape import url_escape
from tornado.escape import json_encode
from datetime import datetime
from datetime import timedelta

class DailyByEventHandler(tornado.web.RequestHandler):
    def get(self):
        rs = cursor.execute("SELECT max(day) from NF_DailyByEvent")
        DefaultDay = rs.fetchone()[0].strftime('%Y-%m-%d')
        WhichDay = self.get_argument("WhichDay", default=DefaultDay)
        cursor.prepare("SELECT e.EventNameCN,e.cnt,s.owner,e.Reason from NF_DailyByEvent e,NF_EventSetting s where e.Eventnamecn = s.Eventnamecn and to_char(e.day,'YYYY-MM-DD')=:day order by e.cnt desc")
        rs = cursor.execute(None, {'day' : WhichDay})
        self.render("DailyByEvent.html",title="Haha", items=rs, day=WhichDay)
    def post(self):
        day = self.get_argument("day")
        input = self.get_argument("input")
        EventNameCN = self.get_argument("EventNameCN")
        cursor.prepare("update NF_DailyByEvent set Reason=:Reason where to_char(day,'YYYY-MM-DD')=:day and EventNameCN=:EventNameCN")
        cursor.execute(None,{'day':day,'Reason':input,'EventNameCN':EventNameCN})
        conn.commit()

class DailyByAppEventHandler(tornado.web.RequestHandler):
    def get(self):
        rs = cursor.execute("SELECT max(insert_time) from NF_EVENTDETAIL")
        DefaultDay = rs.fetchone()[0].strftime('%Y-%m-%d')
        WhichDay = self.get_argument("WhichDay", default=DefaultDay)
        cursor.prepare("SELECT AppName,EventNameCN,count(*) from NF_EVENTDETAIL where to_char(insert_time,'YYYY-MM-DD')=:day group by AppName,EventNameCN order by 3 desc")
        rs = cursor.execute(None, {'day' : WhichDay})
        self.render("DailyByAppEvent.html",title="Haha", items=rs, day=WhichDay)

class DetailByEventHandler(tornado.web.RequestHandler):
    def get(self):
        EventNameCN=self.get_argument("Event")
        WhichDay=self.get_argument("WhichDay")
        cursor.prepare("SELECT EVENTNAMECN,APPNAME,APPSHORTNAME,NODEIP,SUMMARYCN,FIRSTOCCURRENCE,LASTOCCURRENCE,TALLY,CUSTOMERSEVERITY,MAINTAINSTATUS,SD_NO from NF_EVENTDETAIL where EventNameCN= :EventNameCN and to_char(insert_time,'YYYY-MM-DD')= :WhichDay order by APPNAME,FIRSTOCCURRENCE")
        rs = cursor.execute(None, {'EventNameCN' : EventNameCN, 'WhichDay':WhichDay})
        self.render("Detail.html",items=rs)

class DetailByAppEventHandler(tornado.web.RequestHandler):
    def get(self):
        AppName=self.get_argument("App")
        EventNameCN=self.get_argument("Event")
        WhichDay=self.get_argument("WhichDay")

        cursor.prepare("SELECT EVENTNAMECN,APPNAME,APPSHORTNAME,NODEIP,SUMMARYCN,FIRSTOCCURRENCE,LASTOCCURRENCE,TALLY,CUSTOMERSEVERITY,MAINTAINSTATUS,SD_NO from NF_EVENTDETAIL where AppName= :AppName and EventNameCN= :EventNameCN and to_char(insert_time,'YYYY-MM-DD')= :WhichDay order by APPNAME,FIRSTOCCURRENCE")
        rs = cursor.execute(None, {'AppName' : AppName, 'EventNameCN' : EventNameCN, 'WhichDay':WhichDay})
        self.render("Detail.html",items=rs)

class WeeklyStatHandler(tornado.web.RequestHandler):
    def get(self):
        rs = cursor.execute("SELECT max(day) from NF_DailybyEvent")
        EndDayStr = rs.fetchone()[0].strftime('%Y-%m-%d')
        EndDay = datetime.strptime(EndDayStr, '%Y-%m-%d') 
        StartDay = EndDay + timedelta(days=-6)
        StartDayStr = StartDay.strftime('%Y-%m-%d')
        StartDayStr = self.get_argument("StartDay", default=StartDayStr)
        EndDayStr = self.get_argument("EndDay", default=EndDayStr)

        self.render("WeeklyStat.html",StartDay=StartDayStr, EndDay=EndDayStr )


class StatByEventJasonHandler(tornado.web.RequestHandler):
    def get(self):
        json_data = {"days":["day1","day2","day3"],"data_arr":[{"data":[1,2,3],"name":"name1"},{"data":[1,2,3],"name":"name2"}]}
        StartDayStr = self.get_argument("StartDay")
        EndDayStr = self.get_argument("EndDay")

        cursor.prepare("Select EventNameCN, sum(cnt) from NF_DailyByEvent where day >= to_date(:StartDay,'YYYY-MM-DD') and day <=to_date(:EndDay,'YYYY-MM-DD')+1 group by EventNameCN order by 2 desc")
        cursor.execute(None, {'StartDay':StartDayStr,'EndDay':EndDayStr})
        tops=cursor.fetchmany(numRows=10)

        data_series = []
        for top in tops:
            topEvent = top[0]
            cursor.prepare("SELECT cnt from NF_DailyByEvent where EventNameCN=:topEvent and day >= to_date(:StartDay,'YYYY-MM-DD') and day <=to_date(:EndDay,'YYYY-MM-DD')+1 order by day asc")
            cursor.execute(None, {'topEvent':topEvent,'StartDay':StartDayStr,'EndDay':EndDayStr})
            serie_data = []
            for cnt in cursor.fetchall():
                serie_data.append(cnt[0])
            data_series.append({"data":serie_data,"name":topEvent})

        days = []
        TheDay = datetime.strptime(StartDayStr, '%Y-%m-%d')
        while (TheDay.strftime('%Y-%m-%d') != EndDayStr):
            days.append(TheDay.strftime('%Y-%m-%d'))
            TheDay = TheDay + timedelta(days=1)
        days.append(EndDayStr)

        json_data = {'data_series':data_series,'days':days}
        self.write(json_encode(json_data))

class StatByAppEventJasonHandler(tornado.web.RequestHandler):
    def get(self):
        data_series = []
        StartDayStr = self.get_argument("StartDay")
        EndDayStr = self.get_argument("EndDay")
        cursor.prepare("Select AppName, EventNameCN, sum(cnt) from NF_DailyByAppEvent where day >= to_date(:StartDay,'YYYY-MM-DD') and day <=to_date(:EndDay,'YYYY-MM-DD')+1 group by AppName,EventNameCN order by 3 desc")
        cursor.execute(None, {'StartDay':StartDayStr,'EndDay':EndDayStr})
        rows=cursor.fetchmany(numRows=10)
        for row in rows:
            data_series.append([row[0] + "_" + row[1], row[2]])
        self.write(json_encode(data_series))

class SettingHandler(tornado.web.RequestHandler):
    def get(self):
        settings = []
        cursor.execute("SELECT * from NF_EventSetting")
        settings = cursor.fetchall()
        self.render("Setting.html",title="Haha", settings=settings)
    def post(self):
        print("post called")
        Action = self.get_argument("Action")
        EventNameCN = self.get_argument("EventNameCN")
        Owner = self.get_argument("Owner")
        SqlFilter = self.get_argument("SqlFilter")
        try:
            rs = cursor.execute("SELECT * from reporter_status where FirstOccurrence > sysdate - 1 and " + SqlFilter)
            rs.fetchone();
        except:
            self.write('SQLError');
        else:
            if (Action == 'update'):
                try:
                    cursor.prepare("update NF_EventSetting set Owner=:Owner,Filter=:SqlFilter where EventNameCN=:EventNameCN")
                    cursor.execute(None,{'Owner':Owner,'SqlFilter':SqlFilter,'EventNameCN':EventNameCN})
                    conn.commit()
                except:
                    print("update failure")
                    self.write('UpdateError')
                else:
                    self.write('OK')
            elif (Action == 'add'):
                try:
                    cursor.prepare("insert into NF_EventSetting(EventNameCN,Owner,Filter) values(:EventNameCN,:Owner,:Filter)")
                    cursor.execute(None,{'EventNameCN':EventNameCN,'Owner':Owner,'Filter':SqlFilter})
                    conn.commit()
                except:
                    print("insert failure")
                    self.write('AddError')
                else:
                    self.write('OK')

settings= {
    "template_path":"./templates",
    "static_path":"./static"
}

application = tornado.web.Application([
    (r"/", DailyByEventHandler),
    (r"/DailyByEvent.html", DailyByEventHandler),
    (r"/DailyByAppEvent.html", DailyByAppEventHandler),
    (r"/DetailByAppEvent.html", DetailByAppEventHandler),
    (r"/DetailByEvent.html", DetailByEventHandler),
    (r"/WeeklyStat.html", WeeklyStatHandler),
    (r"/StatByEvent.json", StatByEventJasonHandler),
    (r"/StatByAppEvent.json", StatByAppEventJasonHandler),
    (r"/Setting.html", SettingHandler),
], **settings)


if __name__ == "__main__":
    conn = cx_Oracle.connect('dbusername/dbpassword@dbhostname/reporter')
    cursor = conn.cursor()
    application.listen(8081)
    tornado.ioloop.IOLoop.current().start()
