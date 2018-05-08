import codecs
import glob
import json
from bs4 import BeautifulSoup as BS
#list all the filenames in this list
files=sorted(glob.glob("../messages/*.html"));
i=0;
OUTPUT={"feelings":[],"love":[],"life":[],"friends":[],"Myself":[]}
nameorigin=codecs.open("../html/friends.htm",'r');
namesoup=BS(nameorigin,'html.parser')
myname=namesoup.title.get_text().replace(" - Friends","")

while(i<len(files)):
#while(i<1):

	fi=codecs.open(files[i],'r')
	# fi=codecs.open('messages/1019.html','r')
	soup=BS(fi,'html.parser')
	ti=soup.title.get_text()
	conversationwith=ti.replace('Conversation with ','')
	if("," not in ti and "Facebook" not in ti):
		#all the magic should happen here
		number_of_messages=len(soup.find_all("div", class_="message"))
		##Do we need it? Message number filter
		if(number_of_messages>120):
			print("Analysing",ti)
			mees=soup.find_all(text=myname)
			for me in mees:
				#print(me)
				parentspan=me.parent
				meta=parentspan.findNext('span')
				msgheaderdiv=parentspan.parent
				mesggrand=msgheaderdiv.parent
				sweetp=mesggrand.findNext('p')
				toanalyze=sweetp.get_text().lower()
				if("i feel" in toanalyze and len(toanalyze)<1250 and len(toanalyze)>100):
					poo={"to":conversationwith,"msg":sweetp.get_text(),"meta":meta.get_text()}
					OUTPUT["feelings"].append(poo)
					print("Found a feeling. Appending Feeling #",len(OUTPUT["feelings"]))
				if("love" in toanalyze and len(toanalyze)<1250 and len(toanalyze)>100):
					poo={"to":conversationwith,"msg":sweetp.get_text(),"meta":meta.get_text()}
					OUTPUT["love"].append(poo)
					print("Found love. Appending Love #",len(OUTPUT["love"]))
				if("life" in toanalyze and len(toanalyze)<1250 and len(toanalyze)>100):
					poo={"to":conversationwith,"msg":sweetp.get_text(),"meta":meta.get_text()}
					OUTPUT["life"].append(poo)
					print("Found life lesson #",len(OUTPUT["life"]))
				if("friends" in toanalyze and len(toanalyze)<1250 and len(toanalyze)>100):
					poo={"to":conversationwith,"msg":sweetp.get_text(),"meta":meta.get_text()}
					OUTPUT["friends"].append(poo)
					print("Found message about friendship #",len(OUTPUT["friends"]))
				if("I am" in toanalyze and len(toanalyze)<1250 and len(toanalyze)>100):
					poo={"to":conversationwith,"msg":sweetp.get_text(),"meta":meta.get_text()}
					OUTPUT["Myself"].append(poo)
					print("Found reference to self #",len(OUTPUT["Myself"]))
	i+=1
	if i>50:
		break
with open('data.json', 'w') as fout:
    json.dump(OUTPUT, fout)

