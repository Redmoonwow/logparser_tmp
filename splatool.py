import websocket
import json
import numpy
import pandas
import re
import datetime

# ギミッククラス
import TOP_P5

PT_array = pandas.DataFrame(numpy.zeros((8,9)),columns=["name","ID","JOB","x","y","z","PRIO","MINE","NUMKEY"])
MY_PC = pandas.DataFrame(numpy.zeros((1,2)),columns=["name","ID"])
ZoneID = 462
fg_combat = 0
fg_PT_setup_done = False
fg_gimmkck_open_fd = False
fg_test_mode = False

JOBLIST = {
	"00":"",
	"01":"",
	"02":"",
	"03":"",
	"04":"",
	"05":"",
	"06":"",
	"07":"",
	"08":"",
	"09":"",
	"0A":"",
	"0B":"",
	"0C":"",
	"0D":"",
	"0E":"",
	"0F":"",
	"10":"",
	"11":"",
	"12":"",
	"13":"PLD",
	"14":"MNK",
	"15":"WAR",
	"16":"DRG",
	"17":"BRD",
	"18":"WHM",
	"19":"BLM",
	"1A":"",
	"1B":"SMN",
	"1C":"SCH",
	"1D":"",
	"1E":"NIN",
	"1F":"MCH",
	"20":"DRK",
	"21":"AST",
	"22":"SAM",
	"23":"RDM",
	"24":"BLU",
	"25":"GNB",
	"26":"DNC",
	"27":"RPR",
	"28":"SGE"
}
JOBPRIO = {
	"DRK":0,
	"WAR":1,
	"GNB":2,
	"PLD":3,
	"WHM":4,
	"AST":5,
	"SCH":6,
	"SGE":7,
	"DRG":8,
	"MNK":9,
	"SAM":10,
	"RPR":11,
	"NIN":12,
	"BRD":13,
	"MCH":14,
	"DNC":15,
	"SMN":16,
	"BLM":17,
	"RDM":18,
	"":98,
	"BLU":99
}

Gimmick_class_00 = TOP_P5.top_p5()

def Gimmick_branch(message_dict):
	global PT_array
	global Gimmick_class_00
	#TOP P5
	if(log_chk_00(message_dict,"ガガ……ガガガガ……この力は、いったい……！？")):
		Gimmick_class_00.start(PT_array)
		return
	if(Gimmick_class_00.is_start == True):
		Gimmick_class_00.log_chk(message_dict)
	return

def Gimmick_init():
	global Gimmick_class_00
	#TOP P5
	Gimmick_class_00.init()
	return


def log_chk_00(message_dict,chk_message):
	linedata = message_dict["line"]
	if (linedata[0] == "00"):
		if (linedata[4] == chk_message):
			return True

	return False

def func_InCombat(message_dict):
	global fg_combat
	#print(message_dict)
	"""
	if bool(message_dict["inGameCombat"]) != fg_combat:
		fg_combat = message_dict["inGameCombat"]
		if True == message_dict["inGameCombat"]:
			print("-----戦闘開始-----")
		else:
			print("-----戦闘終了-----")
	"""
	return

def func_ChangePrimaryPlayer(message_dict):
	global MY_PC
	MY_PC.loc[0,"ID"]	= format(message_dict["charID"],"X")
	MY_PC.loc[0,"name"]	= message_dict["charName"]
	json_fd = open("splatool\\json\\" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y%m%d%H%M%S") + "_ChangePrimaryPlayer_data.json","w",encoding="utf-8")
	json_fd.write(json.dumps(message_dict, indent=4))
	json_fd.close()
	return

def func_ChangeZone(message_dict):
	global ZoneID
	global fg_PT_setup_done
	ZoneID = message_dict["zoneID"]
	json_fd = open("splatool\\json\\" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y%m%d%H%M%S") + "_" + message_dict["zoneName"] + "_ChangeZone_data.json","w",encoding="utf-8")
	json_fd.write(json.dumps(message_dict, indent=4))
	json_fd.close()
	fg_PT_setup_done = False
	return

def func_ChangeMap(message_dict):
	#print(message_dict)
	# ZoneIDだけでいい
	return

def func_PartyChanged(message_dict):
	global PT_array
	i = 0
	for data in message_dict["party"]:
		PT_array.loc[i,"ID"] = data["id"]
		PT_array.loc[i,"name"] = data["name"]
		PT_array.loc[i,"JOB"] = JOBLIST[format(data["job"],"X")]
		PT_array.loc[i,"PRIO"] = JOBPRIO[PT_array["JOB"][i]]
		i += 1
	json_fd = open("splatool\\json\\" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y%m%d%H%M%S") + "_PartyChanged_data.json","w",encoding="utf-8")
	json_fd.write(json.dumps(message_dict, indent=4))
	json_fd.close()
	return

def func_LogLine(message_dict):
	global PT_array
	global ZoneID
	global fg_gimmkck_open_fd
	global gimmick_fd
	global fg_combat
	global fg_PT_setup_done
	linedata = message_dict["line"]
	if (	(249 <= int(linedata[0]))	and \
			(260 > int(linedata[0]))	):
		return
	match int(linedata[0]):
		case 40:
			return
		case 1:
			return
		case 2:
			return
		case 3:
			return
		case 4:
			return
		case 21:
			return
		case 22:
			return
		case 24:
			return
		case 25:
			return
		case 28:
			return
		case 31:
			return
		case 36:
			return
		case 37:
			return
		case 12:
			return
		case 11:
			func_set_PTarray()
			return
		case 260:
			if ((int(linedata[3]) != fg_combat) and (fg_PT_setup_done == True)):
				fg_combat = int(linedata[3])
				if 1 == int(linedata[3]):
					gimmick_fd = open("splatool\\gimmick_file\\" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y%m%d%H%M%S") + "_gimmick_data.log","w",encoding="utf-8")
					fg_gimmkck_open_fd = True
					gimmick_fd.write("---------------戦闘開始---------------\n")
					print("-----戦闘開始-----")
				else:
					gimmick_fd.write("---------------戦闘終了---------------\n")
					gimmick_fd.close()
					fg_gimmkck_open_fd = False
					Gimmick_init()
					print("-----戦闘終了-----")
			return
		case 38:
			if((True == PT_array[PT_array["ID"] == linedata[2]].empty) and (fg_PT_setup_done == True)):
				return
			else:
				ok = 1
			#print(message_dict["rawLine"])
			PT_array.loc[PT_array["ID"] == linedata[2],"x"] = linedata[11]
			PT_array.loc[PT_array["ID"] == linedata[2],"y"] = linedata[12]
			PT_array.loc[PT_array["ID"] == linedata[2],"z"] = linedata[13]
			return
		case 39:
			if((True == PT_array[PT_array["ID"] == linedata[2]].empty) and (fg_PT_setup_done == True)):
				return
			else:
				ok = 1
			#print(message_dict["rawLine"])
			PT_array.loc[PT_array["ID"] == linedata[2],"x"] = linedata[10]
			PT_array.loc[PT_array["ID"] == linedata[2],"y"] = linedata[11]
			PT_array.loc[PT_array["ID"] == linedata[2],"z"] = linedata[12]
			return
		case 0:
			chatID = linedata[2]
			chatauther = linedata[3]
			chatdata = linedata[4]
			if ("Hojoring" in chatdata):
				return
			if ("Sonar" in chatauther):
				return
			if ("0044" not in chatID):
				return
			#print(message_dict["rawLine"])
		case 20:
			#### 味方から発生してるバフはスキルバフなので除外する
			if(False == PT_array[PT_array["ID"] == linedata[2]].empty):
				return
			else:
				ok = 1
		case 26:
			#### 味方から発生してるバフはスキルバフなので除外する
			if(False == PT_array[PT_array["ID"] == linedata[5]].empty):
				return
			else:
				ok = 1
		case 30:
			#### 味方から発生してるバフはスキルバフなので除外する
			if(False == PT_array[PT_array["ID"] == linedata[5]].empty):
				return
			else:
				ok = 1




		
	#### ここにたどり着くログはギミック処理分岐でつかうためギミック処理分岐にまわす

	Gimmick_branch(message_dict)
	#print(str(message_dict["rawLine"]).replace("\n",""))
	if (fg_gimmkck_open_fd != False):
		gimmick_fd.write(str(message_dict["rawLine"]))
	
	return

def func_OnlineStatusChanged(message_dict):
	print(message_dict)
	return

def func_getCombatants(message_dict):
	print(message_dict)
	return

def func_set_PTarray():
	global PT_array
	global MY_PC
	global fg_PT_setup_done
	PT_array.loc[PT_array["ID"] == str(MY_PC.loc[0,"ID"]),"MINE"] = 1
	PT_array = PT_array.sort_values("PRIO")
	PT_array = PT_array.reset_index(drop=True)
	PT_array.loc[0,"NUMKEY"] = "num5"
	PT_array.loc[1,"NUMKEY"] = "num6"
	PT_array.loc[2,"NUMKEY"] = "num7"
	PT_array.loc[3,"NUMKEY"] = "num8"
	PT_array.loc[4,"NUMKEY"] = "num2"
	PT_array.loc[5,"NUMKEY"] = "num3"
	PT_array.loc[6,"NUMKEY"] = "num1"
	PT_array.loc[7,"NUMKEY"] = "num4"
	fg_PT_setup_done = True


def main():
	#websocket.enableTrace(True)
	ws_cliant = websocket.WebSocket()
	ws_cliant.connect("ws://127.0.0.1:10501/ws",)
	ws_cliant.send('{"call":"subscribe","events":["ChangePrimaryPlayer"]}')
	ws_cliant.send('{"call":"subscribe","events":["ChangeZone"]}')
	ws_cliant.send('{"call":"subscribe","events":["ChangeMap"]}')
	ws_cliant.send('{"call":"subscribe","events":["PartyChanged"]}')
	ws_cliant.send('{"call":"subscribe","events":["LogLine"]}')
	ws_cliant.send('{"call":"subscribe","events":["InCombat"]}')
	ws_cliant.send('{"call":"subscribe","events":["OnlineStatusChanged"]}')
	ws_cliant.send('{"call":"getCombatants","ids":[],"props":["CurrentWorldID","WorldID","WorldName","BNpcID","BNpcNameID","PartyType","ID","OwnerID","Type","type","Job","Level","Name","CurrentHP","MaxHP","CurrentMP","MaxMP","PosX","PosY","PosZ","Heading","TargetID","ModelStatus","IsTargetable","TransformationId","WeaponId"],"rseq":"specificCombatants"}')
	#ws_cliant.send('{"call":"subscribe","events":["GameVersion"]}')
	#ws_cliant.send('{"rseq":"getLanguage","call":"getLanguage"}')
	#ws_cliant.send('{"rseq":"getVersion","call":"getVersion"}')
	ws_cliant.send('{"rseq":"allCombatants","props":["CurrentWorldID","WorldID","WorldName","BNpcID","BNpcNameID","PartyType","ID","OwnerID","Type","type","Job","Level","Name","CurrentHP","MaxHP","CurrentMP","MaxMP","PosX","PosY","PosZ","Heading","TargetID","ModelStatus","IsTargetable","TransformationId","WeaponId"],"call":"getCombatants"}')
	
	while True:
		data:dict = json.loads(ws_cliant.recv())
		if "combatants" in data.keys():
			continue #nop
		#print(data)
		match data["type"]:
			case "ChangePrimaryPlayer":
				func_ChangePrimaryPlayer(data)
			case "ChangeZone":
				func_ChangeZone(data)
			#case "ChangeMap":
			#	func_ChangeMap(data)
			case "PartyChanged":
				func_PartyChanged(data)
			case "LogLine":
				func_LogLine(data)
			case "InCombat":
				func_InCombat(data)
#			case "OnlineStatusChanged":
#				func_OnlineStatusChanged(data)
#			case "getCombatants":
#				func_getCombatants(data)

def damy_main():
	log_p = open(r"E:\logs\Network_26800_20230228.log",encoding = "utf-8")
	pchg_data = open("E:\\works\\80.repos\\splatool\\json\\20230301091033_ChangePrimaryPlayer_data_t.json")
	PTchg_data = '{"type": "PartyChanged", "party": [{"id": "102AE487", "name": "An Hermit", "worldId": 52, "job": 40, "level": 90, "inParty": "True"}, {"id": "102AAE60", "name": "Amelia Wiliams", "worldId": 60, "job": 33, "level": 90, "inParty": "True"}, {"id": "10306755", "name": "Fata Moshroca", "worldId": 52, "job": 30, "level": 90, "inParty": "True"}, {"id": "10337897", "name": "Layla Magnolia", "worldId": 52, "job": 37, "level": 90, "inParty": "True"}, {"id": "10265C76", "name": "Eko Micare", "worldId": 60, "job": 35, "level": 90, "inParty": "True"}, {"id": "1029735D", "name": "Meltz Zacker", "worldId": 60, "job": 32, "level": 90, "inParty": "True"}, {"id": "1005FA50", "name": "Redmoon Rynde", "worldId": 59, "job": 31, "level": 90, "inParty": "True"}, {"id": "101EF83D", "name": "Nasir Spherelot", "worldId": 51, "job": 22, "level": 90, "inParty": "True"}]}'
	func_ChangePrimaryPlayer(json.load(pchg_data))
	func_PartyChanged(json.loads(PTchg_data))
	for log_rawdata in log_p:
		log_array = log_rawdata.split("|")
		log_dict = { "rawLine":log_rawdata,"line":log_array }
		func_LogLine(log_dict)

if __name__ == "__main__":
	#main()
	damy_main()
	

