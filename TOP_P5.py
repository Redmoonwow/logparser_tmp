#import splatool
import pandas
import datetime
import pyautogui
import urllib.parse
import requests

def log_chk_00(message_dict,chk_message):
	linedata = message_dict["line"]
	if (linedata[0] == "00"):
		if (linedata[4] == chk_message):
			return True

	return False

def log_chk_get_buff_26(message_dict,buffID):
	linedata = message_dict["line"]
	if (linedata[0] == "26"):
		if (linedata[2] == buffID):
			a = 1
			return True

	return False

class top_p5:
	__PT_Data = pandas.DataFrame()
	world_cnt = 0
	line_cnt = 0
	is_start = False
	state_delta = 0
	state_sigma = 0
	state_omega = 0
	def __init__(self):
		self.__PT_Data = pandas.DataFrame()
		self.__PT_Data["Dynamis"] = 0
		self.__PT_Data["world"] = ""
		self.__PT_Data["line"] = ""
		return
	
	def start(self,PT_array:pandas.DataFrame):
		self.__PT_Data = PT_array.copy()
		self.__PT_Data["Dynamis"] = 0
		self.__PT_Data["world"] = ""
		self.__PT_Data["line"] = ""
		self.is_start = True
		return
	
	def init(self):
		self.__PT_Data.to_csv(r"E:\works\80.repos\splatool\dumps\top_p5_dump" + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y%m%d%H%M%S") + ".csv" )
		self.__PT_Data = pandas.DataFrame()
		self.__PT_Data["Dynamis"] = 0
		self.__PT_Data["world"] = ""
		self.__PT_Data["line"] = ""
		self.world_cnt = 0
		self.line_cnt = 0
		self.is_start = False
		self.state_delta = 0
		self.state_sigma = 0
		self.state_omega = 0
		return
	
	def interval_init(self):
		self.__PT_Data["world"] = ""
		self.__PT_Data["line"] = ""
		self.world_cnt = 0
		self.line_cnt = 0
		self.state_delta = 0
		self.state_sigma = 0
		self.state_omega = 0
		return
	
	def log_chk(self,message_dict):
		print(str(message_dict["rawLine"]).replace("\n",""))
		linedata = message_dict["line"]
		# デュナミスバフ管理
		if(log_chk_get_buff_26(message_dict,"D74")):
			self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"Dynamis"] += 1

		if(log_chk_00(message_dict,"この力の増幅は、リミッターカットでは説明不能……。 ヒトの不可解な強さと関係が……？")):
			self.interval_init()
			self.state_sigma = 1

		if (self.state_sigma == 1): # Display PRIORITY
			if(log_chk_get_buff_26(message_dict,"D72")):
				self.world_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"world"] = "Near"
			if(log_chk_get_buff_26(message_dict,"D73")):
				self.world_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"world"] = "Far"
			if(self.world_cnt >= 2):
				pri_df = self.__PT_Data[self.__PT_Data["world"] != "Near"]
				pri_df = pri_df[pri_df["world"] != "Far"]
				pri_df = pri_df[pri_df["Dynamis"] == 1]
				pri_df = pri_df.reset_index(drop=True)
				print("--------------------------------------------------")
				print("SIGMA:PRIORITY")
				for index, row in pri_df.iterrows():
					print(str(index + 1) + ": " + row["name"])
					#pyautogui.press(str(row["NUMKEY"]))
				print("--------------------------------------------------")
				self.state_sigma = 2
		if (self.state_sigma == 2):
			a = 1
		return

#d = {'elements': 'eyJOYW1lIjoidGVzdCIsInR5cGUiOjMsInJlZlkiOjI3LjAsInJhZGl1cyI6NTAuMCwiY29sb3IiOjE2Nzc3MjE4NTUsInJlZkFjdG9yTlBDTmFtZUlEIjo3Njk1LCJyZWZBY3RvckNvbXBhcmlzb25UeXBlIjo2LCJpbmNsdWRlUm90YXRpb24iOnRydWUsIm9ubHlWaXNpYmxlIjp0cnVlLCJBZGRpdGlvbmFsUm90YXRpb24iOjEuMzA4OTk2OX0=',"namespace":"extope"}
#d = {"destroy":"extope"}
#d_qs = urllib.parse.urlencode(d)
#requests.post("http://127.0.0.1:47774?" + d_qs)