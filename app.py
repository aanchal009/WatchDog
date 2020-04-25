from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime,date,timedelta
import time as t
import pytz
html='Creating Ranklist'
#function to process spreadsheet and create html file
def sensor():
	global html
	dt=datetime.now(pytz.timezone('Asia/Kolkata'))
	s=str(dt)
	s11=''
	for i in range(0,19):
		s11+=s[i]
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('NowOrNever-ranklist-9a4615e87ecb.json', scope)
	client = gspread.authorize(creds)
	rl=[]
	the_list=[]
	rl=[["SN","Name","Easy Problems","Medium Problems","Hard Problems","Total Problems","Score"]]
	#function to process team's sheet
	def mainfun(team,tm):
		rl1=[]
		Sheet=client.open(team)
		sheet=Sheet.worksheet("Easy Problems")
		r1=sheet.row_values(1)
		for i in range(5,len(r1)):
			if(r1[i]!=''):
				rl1.append([1,r1[i]+tm,0,0,0,0,0])
		n=len(rl1)
		#funtion to process easy medium and hard problems sheet
		def fun(sht,i1):
			sheet=Sheet.worksheet(sht)
			for j in range(0,n):
				c1=sheet.col_values(j*10+7)
				for i in range(5,len(c1)):
					if(c1[i].replace(" ","")!="" and c1[i].replace(" ","").lower()!='no'):
						rl1[j][i1]+=1
			return
		fun("Easy Problems",2)
		t.sleep(40)
		fun("Medium Problems",3)
		t.sleep(40)
		fun("Hard Problems",4)
		t.sleep(40)
		for i in range(n):
			rl.append(rl1[i])
		return
	mainfun("Target 2021 Team-1","(1)")
	t.sleep(100)
	mainfun("Target 2021 Team-2A","(2A)")
	t.sleep(100)
	mainfun("Target 2021 Team-2B","(2B)")
	#calculating score, easy=10,medium=30,hard=50
	for i in range(1,len(rl)):
		rl[i][6]=rl[i][4]*50+rl[i][3]*30+rl[i][2]*10
	#sorting based on score
	for i in range(1,len(rl)):
		for j in range(i+1,len(rl)):
			if(rl[i][6]<rl[j][6]):
				rl[i],rl[j]=rl[j],rl[i]
	#determining rank and total number of problems solved
	for i in range(1,len(rl)):
		rl[i][0]=i
		rl[i][5]=rl[i][2]+rl[i][3]+rl[i][4]
	#storing each row value in a string in justified manner
	for i in range(len(rl)):
		aa=rl[i]
		bb=[0,4,25,44,63,82,101]
		ss=[' ']*106
		for ii in range(7):
			stt=str(aa[ii])
			for jj in range(len(stt)):
				ss[jj+bb[ii]]=stt[jj]
		ss11=''
		for ii in ss:
			ss11+=ii

		the_list.append(ss11)
	#creating html file
	html=''
	html+='<title>NowOrNever-2k21 Ranklist</title><link rel = "icon" href ="https://i.ibb.co/DgJbHKP/browser-action-19.png"type = "image/x-icon">'
	html+='<style>body {background-image: url("https://i.ibb.co/R233GWZ/background.png");margin: 0; background-repeat: no-repeat;background-attachment: fixed;height: 100%;background-position: center;background-repeat: no-repeat;background-size: cover;}</style>'
	html+='<style>h2 {background-color: lightgrey;width:1300px;border:5px solid #003300;padding:10px;margin: 5px;}</style>'
	html+='<p style="text-align:right;">Last Update: '+s11+'</p>'
	html+='<h1 style="text-align:center;font-size: 65px;">NowOrNever-2k21 Ranklist</h1><p style="text-align:center;font-size: 25px;">-by WatchDog</p>'
	html+='<pre><h2 style="border:5px solid black;">'+the_list[0]+'</h2></pre>'
	def funforhtml(a,b,col):
		global html
		for i in range(a,b+1):
			html+='<pre><h2 style="color:'+col+';">'+the_list[i]+'</h2></pre>'
		return
	funforhtml(1,3,"red")
	funforhtml(4,10,"#cc6600")
	# funforhtml(11,16,"#cc00cc")
	funforhtml(11,20,"#cc00cc")
	funforhtml(21,30,"blue")
	funforhtml(31,len(the_list)-1,"green")
	html+='<p style="text-align:left;">Note: Each of the easy question = 10 points, Medium question= 30 points, and hard question=50 points</p>'
	html+='<style>footer { left: 0;bottom: 0;width: 100%;height: 30px;background-color: #99ff66;color: white;text-align: center;}'+'a{color:black;}</style><footer><p style="color:blue;"><b>~Creators: </b><a href="https://github.com/sonuverma1/">sonuverma1</a> || <a href="https://github.com/shre-ya/">shre-ya</a> || <a href="https://github.com/niimmii/">niimmii</a> || <a href="https://github.com/trishalanaman/">trishalanaman</a> || <a href="https://github.com/aanchal269/">aanchal269</a></p></footer>'
	f=open('myhtml.html','w')
	f.write(html)
	f.close()
	return

# Background Scheduling the update functon
sched = BackgroundScheduler()
tm1=['01','03','05','07','09','11','13','15','17','19','21','23']
for ii in tm1:
	sched.add_job(sensor, "cron", hour=ii, minute='00')
sched.start()
app = Flask(__name__)
@app.route("/")
def home():
	f=open('myhtml.html','r')
	s=''
	s=f.read()
	f.close()
	return s

if __name__ == "__main__":
    app.run()
