import requests
import sys
import json

urls = requests.get("www.mydea.org/api")

if(os.path.exists('./token')):
	token = open('./token').readline()
else:
	f = {'username':'quinn','password':'franklin'}
	r = requests.post(urls['login'],data = f)
	if r.status_code == requests.code.ok:
		token = json.loads(r.json)['token']
		f = open('./token','w')
		f.write(token)
		f.close()
		
def sendResource(iD, data):
	contentType = 1
	if(os.path.exists(data)):
		contentType = 2
		
		
	if contentType > 1:
		payload =  {'value':(open(data,'rb'))}
		form = {'id':iD,'type':contentType}
	else:
		payload = {}
		form = {'id':iD,'type':contentType,'value':data}
	
	r = requests.post(urls['media'],files = payload, data = form)

def addNew(desc,title, data):
	form = { 'desc':desc,'title':title}
	
	dataHeader = {'token':token}
	r = requests.post(urls['ideas'],data=form,headers = dataHeader)
	if( r.status_code == 302):
		ideaUrl = r.text
		print(ideaURL)
		ideaID = requests.get(ideaUrl)
		sendResource(ideaURL,ideaID,data)
	else:
		raise(LookupError("Ideas unreachable"))
	

def edit(item):
	pass

if len(sys.argv) < 5:
	print("you done goofed")
	quit(1)
	
if sys.argv[1] == "new":
	addNew(sys.argv[2],sys.argv[3],sys.argv[4])


if sys.argv[1] == "edit":
	edit(sys.argv[2])
