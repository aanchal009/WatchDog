import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('WatchDog-48ac764516a3.json', scope)
client = gspread.authorize(creds)
rl=[]
def mainfun(SHEET):
	rl1=[]
	sheet=client.open(SHEET).worksheet("Easy Problems")
	r1=sheet.row_values(1)
	for i in range(5,len(r1)):
		if(r1[i]!=''):
			v=['',0,0,0,0]
			v[0]=r1[i]
			rl1.append(v)
	n=len(rl1)
	def fun(sht,i1):
		sheet=client.open(SHEET).worksheet(sht)
		for j in range(0,n):
			c1=sheet.col_values(j*10+7)
			for i in range(5,len(c1)):
				if(c1[i]!='' and c1[i].lower()!='no'):
					rl1[j][i1]+=1
	fun("Easy Problems",1)
	fun("Medium Problems",2)
	fun("Hard Problems",3)
	for i in range(n):
		rl.append(rl1[i])
mainfun("test_team_1")
mainfun("test_team_2A")
mainfun("test_team_2B")

for i in range(len(rl)):
	rl[i][4]=rl[i][3]*50+rl[i][2]*30+rl[i][1]*10
for i in range(len(rl)):
	for j in range(i+1,len(rl)):
		if(rl[i][4]<rl[j][4]):
			rl[i],rl[j]=rl[j],rl[i]
# print("Name    Easy_Problems    Medium_Problems   Hard_Problems   Score",file=open("Ranklist.txt","w"))
print("Name Easy_Problems Medium_Problems Hard_Problems Score",file=open("Ranklist.txt","w"))
for i in range(len(rl)):
	for j in range(5):
		print(rl[i][j], end =" ",file=open("RankList.txt","a"))
	print("",file=open("RankList.txt","a"))

########################## New part added here
f = open("Ranklist.txt","r")
your_string = f.read()
print(your_string)
text_markdown = "\t"
with open('Ranklist.txt') as this_file:
    for a in this_file.read():
        if "\n" in a:
            text_markdown += "\n \t"
        else:
            text_markdown += a
app = dash.Dash('')
server = app.server
app.config.suppress_callback_exceptions = False
app.scripts.config.serve_locally = True
class DashCallbackVariables:
    """Class to store information useful to callbacks"""

    def __init__(self):
        self.n_clicks = {1: 0, 2: 0}

    def update_n_clicks(self, nclicks, bt_num):
        self.n_clicks[bt_num] = nclicks


callbacks_vars = DashCallbackVariables()
root_layout=html.Div(id='a',children=[
      
      html.Button('Generate Ranklist', id='button'),
        html.Div(id='output',children=[
            
            dcc.Markdown(
            '',
            id='d'
        ),
            
        #   html.Div([
        #                 dcc.Markdown(text_markdown)
        #    ])  
            ])
          
                
])
app.layout =  root_layout
@app.callback(
    Output('d', 'children'),
    [Input('button', 'n_clicks')])
def clicks(n_clicks):
    if n_clicks>0:
       return text_markdown 
    return ""
            
    
if __name__ == '__main__':
   app.run_server(debug=True)