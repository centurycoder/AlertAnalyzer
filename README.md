# AlertAnalyzer
A python web application that displays alert statistics, using tornado framework , jquery and  highcharts.

# How to run (You may need to change first line to your actual python path)
nohup ./AA.py &

# Program Structure

1. AA.py - the main program, which based on tornado web-framework.

Tornado is a light-weight python web framework like flask. It starts listening and accepting client http request by following code:
	application.listen(8081)
	tornado.ioloop.IOLoop.current().start()

When Tornado receive a http request, it instantialize a tornado.web.RequestHandler object as to below route configuration, that is, a tuple list:
	(r"/", DailyByEventHandler),
    (r"/DailyByEvent.html", DailyByEventHandler),
    (r"/DailyByAppEvent.html", DailyByAppEventHandler),
    (r"/DetailByAppEvent.html", DetailByAppEventHandler),
    (r"/DetailByEvent.html", DetailByEventHandler),
    (r"/WeeklyStat.html", WeeklyStatHandler),
    (r"/StatByEvent.json", StatByEventJasonHandler),
    (r"/StatByAppEvent.json", StatByAppEventJasonHandler),
    (r"/Setting.html", SettingHandler),
	
	Each handler class overrides get() and post() method, and is invoked by the framework. 
	
In get/post method, The program gets arguments, do database select/update/insert and other logics, render the html template, and return the result html response.


2. templates folder - html template place
	1) Base.html
		The common part of all html pages, that is, http header and navigation part that's shared by all pages.
	2) DailyByEvent.html
		This html page extends Base.html, and include following part:
			A form allow user to choose a date, and submit button
			A table structure, the table content is embedded with python codes, and will be instantiated to real html by framework render fuction.
	3) WeeklyStat.html
		Contains 2 panel(place holder): WeeklyTop10Panel and EventAppPanel
		Include js/WeeklyStat.js, which will be called when page is ready, and the js will first send http request to server for json data, and when data is ready, the js will plot using highcharts.
	4) And so on
	
3. staic/js - js file place
	1) DailyByEvent.js
		When "edit" button is clicked, the js will be called, which will be get user input and send content to server-side using HTTP POST.
	2) WeeklyStat.js
		When document is ready, the js will first send http request to server for json data, and when data is ready, plot using highcharts.
	3) And so on.	
		
4. static/css
	Where CSS style file resides.
