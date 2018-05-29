########USER DEFINED VARIABLES############

## Adjustment controls what fraction of the mean number of messages should be used as the cutoff to decide whether a friend should be analysed or not
ADJUSTMENT = 0.75
##KEYWORD DOCTIONARY
# confusion_=["doubtful","embarrassed","hesitant","not sure","distrustful","but i think","unsure","tense","stressed","uncomfortable","dishonest","disdainful","manipulative","judgmental","argumentative","authoritative","condescending","distracted","disoriented","off-kilter","frenzied","blushing","awkward","incapable","paralyzed","fatigued","inferior","vulnerable","distressed","pathetic","distraught","doomed","overwhelmed","incompetent","incapacitated","trapped","squirming","jittery","woozy","twitching","compulsive","uncaring","uninterested","unresponsive","terrified","suspicious","anxious","alarmed","panicked","threatened","cowardly","insecure","Deceived ","Helplessness","Disempowered"]
# anger_=["Ordeal","Outrageousness","Provoke","Repulsive","Scandal","Severe","Shameful","Shocking","Terrible","Tragic","Unreliable","Unstable","Wicked","Aggravate","Agony","Appalled","Atrocious","Corrupting","Damaging","Deplorable","Disadvantages","Disastrous","Disgusted","Dreadful","Eliminate","Harmful","Harsh","Inconsiderate","enraged","offensive","aggressive","frustrated","controlling","resentful","malicious","infuriated","critical","violent","vindictive","sadistic","spiteful","furious","agitated","antagonistic","repulsed","quarrelsome","venomous","rebellious","exasperated","impatient","contrary","condemning","seething","scornful","sarcastic","poisonous","jealous","ticked off","revengeful","retaliating","reprimanding","powerless","despicable","self-hating","desperate","alienated","pessimistic","dejected","vilified","violated"]
# happy_=["motivated","eager","keen","earnest","inspired","enthusiastic","bold","brave","daring","hopeful","upbeat","assured","clear","balanced","fine","grateful","carefree","adequate","fulfilled","genuine","authentic","forgiving","sincere","uplifted","unburdened","confident","self-sufficient","reliable","sure","unique","dynamic","tenacious","cooperative","productive","exuberant","in the zone","responsive","conscientious","approving","honored","privileged","adaptable","Empowered","Focused","Capable","blissful","joyous","delighted","overjoyed","gleeful","thankful","festive","ecstatic","satisfied","cheerful","sunny","elated","jubilant","jovial","awesome","lighthearted","glorious","innocent","childlike","gratified","euphoric","on top of the","world","playful","courageous","energetic","liberated","optimistic","frisky","animated","spirited","thrilled","wonderful","funny","intelligent","exhilarated","spunky","youthful","vigorous","tickled","creative","constructive","helpful","resourceful","comfortable","pleased","encouraged","surprised","content","serene","bright","blessed","Vibrant","Bountiful","Glowing"]
# calm_=["chill","at ease","comfortable","content","quiet","certain","relaxed","serene","bright","blessed","balanced","grateful","carefree","fulfilled","genuine","authentic","forgiving","sincere","uplifted","unburdened","confident","self-sufficient","glowing","radiant","beaming","reflective","smiling","grounded","unhurried","open-minded","efficient","non-controlling","unassuming","trusting","supported","fluid","light","spontaneous","aware","healthy","meditative","still","rested","waiting","laughing","graceful","natural","steady","centered","placid","Clear","Stoic","Aligned"]

confusion_=["not sure","i dunno","maybe i guess","but then","unsure","god knows","who knows"]
anger_=["fucking","damn","i hate","crap","asshole","shit","fuck"]
happy_=["awesome","incredible","amazing","i love"]
calm_=["i think","i feel","i hope","am certain"]



#What fraction of mean number of messages should be the cutoff for analysis
import json
import datetime
from glob import glob
files = glob('messages/*/message.json')
def msglength(el):
	if "messages" not in el:
		return 0
	else:
		return len(el["messages"])
def FilterChat(arr):
	mean_messages=sum(msglength(chatElem) for chatElem in arr)/len(arr)
	print("The mean messages is "+str(mean_messages))
	return [a for a in arr if QualifiesForAnalysis(a,mean_messages)]
def QualifiesForAnalysis(chat,cutoff):
	if 'participants' not in chat:
		return False
	participants=chat["participants"]
	if len(participants)!=1:
		return False
	participant = participants[0]
	if participant=="Facebook User" or len(participant)==0:
		return False
	if msglength(chat)<cutoff * ADJUSTMENT:
		return False
	#friends_.append(" "+participant.partition(' ')[0].lower()+" ")

	return True

def DeriveEssence(msg,to):
	if 'content' not in msg:
		return False
	if(len(msg["content"])>1000 or len(msg["content"])<120):
		return False
	timestamp = msg["timestamp"]
	year = datetime.datetime.fromtimestamp(timestamp).strftime('%Y')
	month=(int)datetime.datetime.fromtimestamp(timestamp).strftime('%m')
	M = msg["content"].lower()
	for keyword in calm_:
		if keyword.lower() in M:
			togo={'content':msg["content"],'timestamp':msg["timestamp"],'to':to,'yr':year,"match":"calm",'month':month}
			OUTPUT.append(togo);
	for keyword in happy_:
		if keyword.lower() in M:
			togo={'content':msg["content"],'timestamp':msg["timestamp"],'to':to,'yr':year,"match":"happy",'month':month}
			OUTPUT.append(togo);
	for keyword in anger_:
		if keyword.lower() in M:
			togo={'content':msg["content"],'timestamp':msg["timestamp"],'to':to,'yr':year,"match":"anger",'month':month}
			OUTPUT.append(togo);
	for keyword in confusion_:
		if keyword.lower() in M:
			togo={'content':msg["content"],'timestamp':msg["timestamp"],'to':to,'yr':year,"match":"confusion",'month':month}
			OUTPUT.append(togo);

def ExtractResults(arr):
	for conv in arr:
		print("Analysing "+conv["participants"][0])
		for message in conv["messages"]:
			if message["sender_name"]!=conv["participants"][0]:
				#Got my message, how about doing some proximity analysis here? with respect t message and conv["messages"]
				DeriveEssence(message,conv["participants"][0])

chatarray=[]
OUTPUT=[]
for file in files:
	with open(file) as f:
		chatdata = json.load(f)
		chatarray.append(chatdata)
filteredChatArray = FilterChat(chatarray);
ExtractResults(filteredChatArray)
print("--------------_DONE-------------------")
with open('data.json', 'w') as fout:
    json.dump(OUTPUT, fout)
#print([a["participants"] for a in filteredChatArray])




