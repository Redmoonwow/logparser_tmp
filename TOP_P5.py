#import splatool
import pandas
import datetime
import splatool_util

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
		if(splatool_util.log_chk_get_buff_26(message_dict,"D74")):
			self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"Dynamis"] += 1

		if(splatool_util.log_chk_00(message_dict,"この力の増幅は、リミッターカットでは説明不能……。 ヒトの不可解な強さと関係が……？")):
			self.interval_init()
			self.state_sigma = 1

		if (self.state_sigma == 1): # Display PRIORITY
			if(splatool_util.log_chk_get_buff_26(message_dict,"D72")):
				self.world_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"world"] = "Near"
			if(splatool_util.log_chk_get_buff_26(message_dict,"D73")):
				self.world_cnt += 1
				self.__PT_Data.loc[self.__PT_Data["ID"] == linedata[7],"world"] = "Far"
			if(self.world_cnt >= 2):
				pri_df = self.__PT_Data[self.__PT_Data["world"] != "Near"]
				pri_df = pri_df[pri_df["world"] != "Far"]
				pri_df = pri_df[pri_df["Dynamis"] == 1]
				pri_df = pri_df.reset_index(drop=True)
				print("--------------------------------------------------")
				print("SIGMA:PRIORITY")
				disnumkey =""
				for index, row in pri_df.iterrows():
					print(str(index + 1) + ": " + row["name"])
					#pyautogui.press(str(row["NUMKEY"]))
					disnumkey = disnumkey + str(row["NUMKEY"]).replace("num","")
				print("NUMKEY: " + disnumkey)
				print("--------------------------------------------------")
				self.state_sigma = 2
		if (self.state_sigma == 2):
			a = 1
		return