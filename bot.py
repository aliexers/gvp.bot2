from requests import get
from re import findall
import os
import glob
from rubika.client import Bot
import requests
from rubika.tools import Tools
from rubika.encryption import encryption
from gtts import gTTS
from mutagen.mp3 import MP3
import time
import random
import urllib
import io

bot = Bot("pydroid 3", auth="wrychztzmhiqshmbkthytfudydggkwkm")
target = "g0Bigrk0ea10fcf719cc0e68768bb9a9"

# created By Sajad & morteza

def hasAds(msg):
	links = ["http://","https://",".ir",".com",".org",".net",".me"]
	for i in links:
		if i in msg:
			return True
			
def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData
	
# static variable
answered, sleeped, retries = [], False, {}

alerts, blacklist = [] , []

def alert(guid,user,link=False):
	alerts.append(guid)
	coun = int(alerts.count(guid))

	haslink = ""
	if link : haslink = "به دلیل فرستادن لینک اخطار گرفت"

	if coun == 1:
		bot.sendMessage(target, "🔹 این یهود, [ @"+user+" ] "+haslink+" \n  در حال حاضر این واژن زاده (1/3) اخطار داره 👺")
	elif coun == 2:
		bot.sendMessage(target, "🔹 این یهود, [ @"+user+" ] "+haslink+" \n  در حال حاضر این واژن زاده (2/3) اخطار داره 👺 \n دفعه بعد لینک بفرستی از گروه اخراج میشی")

	elif coun == 3:
		blacklist.append(guid)
		bot.sendMessage(target, "🚫 🔹 این ملعون, [ @"+user+" ] \n به دلیل گرفتن 3 اخطار از گروه اخراج شد 👺")
		bot.banGroupMember(target, guid)


while True:
	# time.sleep(15)
	try:
		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]

		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue

		for msg in messages:
			try:
				if msg["type"]=="Text" and not msg.get("message_id") in answered:
					if not sleeped:
						if hasAds(msg.get("text")) and not msg.get("author_object_guid") in admins :
							guid = msg.get("author_object_guid")
							user = bot.getUserInfo(guid)["data"]["user"]["username"]
							bot.deleteMessages(target, [msg.get("message_id")])
							alert(guid,user,True)

						elif msg.get("text") == "!stop" or msg.get("text") == "خاموش" and msg.get("author_object_guid") in admins :
							try:
								sleeped = True
								bot.sendMessage(target, "ربات خاموش شد دا 🗿", message_id=msg.get("message_id"))
							except:
								print("err off bot")
								
						elif msg.get("text") == "!restart" or msg.get("text") == "ریستارت" and msg.get("author_object_guid") in admins :
							try:
								sleeped = True
								bot.sendMessage(target, "Restarting ...", message_id=msg.get("message_id"))
								sleeped = False
								bot.sendMessage(target, "ربات با موفقیت ریستارت شد دا 🗿", message_id=msg.get("message_id"))
							except:
								print("err Restart bot")
								
						elif msg.get("text").startswith("حذف") and msg.get("author_object_guid") in admins :
							try:
								number = int(msg.get("text").split(" ")[1])
								answered.reverse()
								bot.deleteMessages(target, answered[0:number])

								bot.sendMessage(target, "✅ "+ str(number) +" ᴿᴱᶜᴱᴺᵀ ᴹᴱˢˢᴬᴳᴱ ˢᵁᶜᶜᴱˢˢᶠᵁᴸᴸᵞ ᴰᴱᴸᴱᵀᴱᴰ", message_id=msg.get("message_id"))
								answered.reverse()

							except IndexError:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "✅ پیام حذف شد دا", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ دستور رو دوباره بفرست سید", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("بن") and msg.get("author_object_guid") in admins :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									bot.banGroupMember(target, guid)
									# bot.sendMessage(target, "این یهود با موفقیت از گروه بن شد🗿", message_id=msg.get("message_id"))
								else :
									bot.sendMessage(target, "کصخل این ادمینه 👺", message_id=msg.get("message_id"))
									
							except IndexError:
								bot.banGroupMember(target, bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"])
								# bot.sendMessage(target, "این یهود با موفقیت از گروه بن شد🗿", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "جقی درست وارد کن دستور رو 👺", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("افزودن") or msg.get("text").startswith("!add") :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"]
								if guid in blacklist:
									if msg.get("author_object_guid") in admins:
										alerts.remove(guid)
										alerts.remove(guid)
										alerts.remove(guid)
										blacklist.remove(guid)

										bot.invite(target, [guid])
									else:
										bot.sendMessage(target, "❌ این کاربر تو مخاطبین ربات ذخیره نشده سید", message_id=msg.get("message_id"))
								else:
									bot.invite(target, [guid])
									# bot.sendMessage(target, "✅ کاربر اکنون عضو گروه است", message_id=msg.get("message_id"))

							except IndexError:
								bot.sendMessage(target, "جقی درست وارد کن دستور رو 👺", message_id=msg.get("message_id"))
							
							except:
								bot.sendMessage(target, "❌ این کاربر تو مخاطبین ربات ذخیره نشده سید", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "دستورات":
							try:
								rules = open("help.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text").startswith("آپدیت دستورات") and msg.get("author_object_guid") in admins:
							try:
								rules = open("help.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت قوانین")))
								bot.sendMessage(target, "ᴿᴬᴮᴬᵀ ᴿᵁᴸᴱˢ ᴴᴬⱽᴱ ᴮᴱᴱᴺ ᵁᴾᴰᴬᵀᴱᴰ!", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "ᵀᴴᴱᴿᴱ ᵂᴬˢ ᴬ ᴾᴿᴼᴮᴸᴱᴹ, ᵀᴿᵞ ᴬᴳᴬᴵᴺ!", message_id=msg.get("message_id"))
								
						elif msg["text"].startswith("!number") or msg["text"].startswith("بشمار"):
							try:
								response = get(f"http://api.codebazan.ir/adad/?text={msg['text'].split()[1]}").json()
								bot.sendMessage(msg["author_object_guid"], "\n".join(list(response["result"].values())[:20])).text
								bot.sendMessage(target, "نتیجه بزودی برای شما ارسال خواهد شد...", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "هعب سید متاسفانه دستوری مجود نبود 😧", message_id=msg["message_id"])
							
						elif msg.get("text").startswith("زمان"):
							try:
								response = get("https://api.codebazan.ir/time-date/?td=all").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								print("err answer time")
								
						elif msg.get("text") == "ساعت":
							try:
								bot.sendMessage(target, f"Time : {time.localtime().tm_hour} : {time.localtime().tm_min} : {time.localtime().tm_sec}", message_id=msg.get("message_id"))
							except:
								print("err time answer")
						
						elif msg.get("text") == "!date":
							try:
								bot.sendMessage(target, f"Date: {time.localtime().tm_year} / {time.localtime().tm_mon} / {time.localtime().tm_mday}", message_id=msg.get("message_id"))
							except:
								print("err date")
								
						elif msg.get("text") == "پاک" and msg.get("author_object_guid") in admins :
							try:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "ᵀᴴᴱ ᴹᴱˢˢᴬᴳᴱ ᵂᴬˢ ᴰᴱᴸᴱᵀᴱᴰ ...", message_id=msg.get("message_id"))
							except:
								print("err pak")
								
						elif msg.get("text").startswith("!cal") or msg.get("text").startswith("حساب"):
							msd = msg.get("text")
							if plus == True:
								try:
									call = [msd.split(" ")[1], msd.split(" ")[2], msd.split(" ")[3]]
									if call[1] == "+":
										try:
											am = float(call[0]) + float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
											plus = False
										except:
											print("err answer +")
										
									elif call[1] == "-":
										try:
											am = float(call[0]) - float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer -")
										
									elif call[1] == "*":
										try:
											am = float(call[0]) * float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer *")
										
									elif call[1] == "/":
										try:
											am = float(call[0]) / float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer /")
											
								except IndexError:
									bot.sendMessage(target, "جقی درست وارد کن دستور رو 👺" ,message_id=msg.get("message_id"))
									plus= True
						
						elif hasInsult(msg.get("text"))[0] and not msg.get("author_object_guid") in admins :
							try:
								print("yek ahmagh fohsh dad")
								bot.deleteMessages(target, [str(msg.get("message_id"))])
								print("fohsh pak shod")
							except:
								print("err del fohsh Bug")
                                
						elif msg.get("text").startswith("اصل") or msg.get("text").startswith("اصل بده") or msg.get("text").startswith("اصل بشوت") or msg.get("text").startswith("اصل بد") or msg.get("text").startswith("اصل میدی") or msg.get("text").startswith("اصل میدی اشنا شیم"):
							try:
								bot.sendMessage(target,'گوربه غمگین هستم سید . 2 ساله هستم و ساکن خیابان های یزد هعب 😾' ,message_id=msg.get("message_id"))
							except:
								print("err asll")

						elif msg.get("text").startswith("خوبی") or msg.get("text").startswith("خبی"):
							try:
								bot.sendMessage(target, "به خوبیت سید تو چطوری؟", message_id=msg.get("message_id"))
							except:
								print("err khobi")
								
						elif msg.get("text").startswith("چه خبر") or msg.get("text").startswith("چخبر"):
							try:
								bot.sendMessage(target, "ســلامـتیت♥", message_id=msg.get("message_id"))
							except:
								print("err CheKhabar")
                                
						elif msg.get("text").startswith("بیا پی") or msg.get("text").startswith("بیا پیوی"):
							try:
								bot.sendMessage(target, "حله سید", message_id=msg.get("message_id"))
							except:
								print("err biya pv")
                                
						elif msg.get("text").startswith("اها") or msg.get("text").startswith("عاها"):
							try:
								bot.sendMessage(target, "طنز نشو دلقک", message_id=msg.get("message_id"))
							except:
								print("err kossheryek")
                                
						elif msg.get("text").startswith("کونی") or msg.get("text").startswith("کیونی"):
							try:
								bot.sendMessage(target, "پدرته😀", message_id=msg.get("message_id"))
							except:
								print("err kossherdo")
                                
						elif msg.get("text").startswith("کسکش") or msg.get("text").startswith("کصکش"):
							try:
								bot.sendMessage(target, "بشین سرش کیسه بکش🙂", message_id=msg.get("message_id"))
							except:
								print("err kossherse")
                                
						elif msg.get("text").startswith("کیری") or msg.get("text").startswith("کیر"):
							try:
								bot.sendMessage(target, "اینو بخور نمیری", message_id=msg.get("message_id"))
							except:
								print("err kossherchar")
                                
						elif msg.get("text").startswith("خبید") or msg.get("text").startswith("خبی"):
							try:
								bot.sendMessage(target, "حله", message_id=msg.get("message_id"))
							except:
								print("err kossherpang")
                                
						elif msg.get("text").startswith("مرسی") or msg.get("text").startswith("مرس"):
							try:
								bot.sendMessage(target, "مرسی از خایمالیت  🤝", message_id=msg.get("message_id"))
							except:
								print("err kosshershish")
                                
						elif msg.get("text").startswith("ممنون") or msg.get("text").startswith("خیلی ممنون"):
							try:
								bot.sendMessage(target, "مرسی از خایمالیت سید 🤝", message_id=msg.get("message_id"))
							except:
								print("err kossherhaf")
                                
						elif msg.get("text").startswith("مرسی ممنون") or msg.get("text").startswith("ملسی"):
							try:
								bot.sendMessage(target, "ممنون از خایمالیت 🤝", message_id=msg.get("message_id"))
							except:
								print("err kossherhash")
                                
						elif msg.get("text").startswith("جقی") or msg.get("text").startswith("جغی"):
							try:
								bot.sendMessage(target, "پدرت جقیه", message_id=msg.get("message_id"))
							except:
								print("err kossherno")
                                
						elif msg.get("text").startswith("بکیرم") or msg.get("text").startswith("بیکیرم"):
							try:
								bot.sendMessage(target, "نداری لف بده😂", message_id=msg.get("message_id"))
							except:
								print("err kossherdah")
                                
						elif msg.get("text").startswith("به تخمم") or msg.get("text").startswith("ب تخمم"):
							try:
								bot.sendMessage(target, "به اون نخودا میگی تخم؟", message_id=msg.get("message_id"))
							except:
								print("err kossheryazdah")
                                
						elif msg.get("text").startswith("رل پی") or msg.get("text").startswith("رل میخوام"):
							try:
								bot.sendMessage(target, "جقی", message_id=msg.get("message_id"))
							except:
								print("err kossherdavazdah")
                                
						elif msg.get("text").startswith("رل پیوی") or msg.get("text").startswith("رل پیوی"):
							try:
								bot.sendMessage(target, "جقی", message_id=msg.get("message_id"))
							except:
								print("err kosshersinzdah")
                                
						elif msg.get("text").startswith("رلپی") or msg.get("text").startswith("رلپی"):
							try:
								bot.sendMessage(target, "جقی", message_id=msg.get("message_id"))
							except:
								print("err kossherchardah")
                                
						elif msg.get("text").startswith("مایل به لواط") or msg.get("text").startswith("مایل ب لواط"):
							try:
								bot.sendMessage(target, "لاواطه که مایه حیاته سید", message_id=msg.get("message_id"))
							except:
								print("err kossherponzah")
                                
						elif msg.get("text").startswith("سکس چت پی") or msg.get("text").startswith("سکس چت پی"):
							try:
								bot.sendMessage(target, "جقی", message_id=msg.get("message_id"))
							except:
								print("err kosshershonza")
								
						elif msg.get("text").startswith("خارکسه") or msg.get("text").startswith("خارکسده"):
							try:
								bot.sendMessage(target, "خارتو بردم", message_id=msg.get("message_id"))
							except:
								print("err hivdah")
                                
						elif msg.get("text").startswith("کیر") or msg.get("text").startswith("کیر"):
							try:
								bot.sendMessage(target, "دوس داری بگم علی بده بت😖", message_id=msg.get("message_id"))
							except:
								print("err hijhdah")
                                
						elif msg.get("text").startswith("کص") or msg.get("text").startswith("کس"):
							try:
								bot.sendMessage(target, "ناراحت شدم دا قرار نبود ناموصی بدی . ما اگه اینجا فحش هم میدیم جنبه شوخی داره و ناموصی نمی دیم", message_id=msg.get("message_id"))
							except:
								print("err nozdah")
                                
						elif msg.get("text").startswith("ممه میخام") or msg.get("text").startswith("ممه میقام"):
							try:
								bot.sendMessage(target, "دخترا گپ میدن😂", message_id=msg.get("message_id"))
							except:
								print("err bis")
                                
						elif msg.get("text").startswith("😂") or msg.get("text").startswith("😂😂"):
							try:
								bot.sendMessage(target, "خنده مکنی کونکش؟", message_id=msg.get("message_id"))
							except:
								print("err bis yek")
                                
						elif msg.get("text").startswith("چطوری") or msg.get("text").startswith("چتوری"):
							try:
								bot.sendMessage(target, "خوبم دا تو چطوری سد؟", message_id=msg.get("message_id"))
							except:
								print("err bisdo")
                                
						elif msg.get("text").startswith("خوبی؟") or msg.get("text").startswith("خوبی"):
							try:
								bot.sendMessage(target, "اره دا بد نیستیم", message_id=msg.get("message_id"))
							except:
								print("err bisse")
                                
						elif msg.get("text").startswith("لواط") or msg.get("text").startswith("لوات"):
							try:
								bot.sendMessage(target, "مایل به تمایل", message_id=msg.get("message_id"))
							except:
								print("err bischar")
                                
						elif msg.get("text").startswith("رل میخوام") or msg.get("text").startswith("رل"):
							try:
								bot.sendMessage(target, "دا اینجا همه پسرن", message_id=msg.get("message_id"))
							except:
								print("err bispang")
                                
						elif msg.get("text").startswith("سکسچت پی") or msg.get("text").startswith("سکسچت پی"):
							try:
								bot.sendMessage(target, "گیی دا؟", message_id=msg.get("message_id"))
							except:
								print("err bisshish")
                                
						elif msg.get("text").startswith("کبص") or msg.get("text").startswith("کوبص"):
							try:
								bot.sendMessage(target, "کیبر", message_id=msg.get("message_id"))
							except:
								print("err bishaf")
                                
						elif msg.get("text").startswith("کون") or msg.get("text").startswith("کیون"):
							try:
								bot.sendMessage(target, "کون ممرضا رو میگی؟", message_id=msg.get("message_id"))
							except:
								print("err bishash")
                                
						elif msg.get("text").startswith("کص ننت") or msg.get("text").startswith("کس ننت"):
							try:
								bot.sendMessage(target, "ناراحت شدم دا قرار نبود ناموصی بدی . ما اگه اینجا فحش هم میدیم جنبه شوخی داره و ناموصی نمی دیم", message_id=msg.get("message_id"))
							except:
								print("err bisnoh")
                                
						elif msg.get("text").startswith("عکس بده") or msg.get("text").startswith("عکس"):
							try:
								bot.sendMessage(target, "بشین تا بدم", message_id=msg.get("message_id"))
							except:
								print("err si")
                                
						elif msg.get("text").startswith("کیرم توت") or msg.get("text").startswith("کیرم توت"):
							try:
								bot.sendMessage(target, "حله", message_id=msg.get("message_id"))
							except:
								print("err siyek")
                                
						elif msg.get("text").startswith("بای") or msg.get("text").startswith("باحی"):
							try:
								bot.sendMessage(target, "خدا پشت و پناهت سید 🖐", message_id=msg.get("message_id"))
							except:
								print("err sido")
                                
						elif msg.get("text").startswith("فعلا") or msg.get("text").startswith("فعلن"):
							try:
								bot.sendMessage(target, "خدا پشت و پناهت سید 🖐", message_id=msg.get("message_id"))
							except:
								print("err sise")
                                
						elif msg.get("text").startswith("علی") or msg.get("text").startswith("علی گیمر"):
							try:
								bot.sendMessage(target, "اگه کاری باهاش داری پیویش بگو سید @AIi_Gamer", message_id=msg.get("message_id"))
							except:
								print("err sichar")
                                
						elif msg.get("text").startswith("گوزو") or msg.get("text").startswith("گوزو"):
							try:
								bot.sendMessage(target, "خودت میگوزی میزاری گردن من؟", message_id=msg.get("message_id"))
							except:
								print("err sipang")
                                
						elif msg.get("text").startswith("میکنمت") or msg.get("text").startswith("میکنمت"):
							try:
								bot.sendMessage(target, "نخندون داپ😐با هسته خرما میخای غوغا کنی؟", message_id=msg.get("message_id"))
							except:
								print("err sishish")
                                
						elif msg.get("text").startswith("گودرت") or msg.get("text").startswith("گدرت"):
							try:
								bot.sendMessage(target, "گودرت ندارم |دانلود گودرت.......................۹۸.ارور❌", message_id=msg.get("message_id"))
							except:
								print("err sihaf")
                                
						elif msg.get("text").startswith("🗿") or msg.get("text").startswith("🗿🗿"):
							try:
								bot.sendMessage(target, "سید رفتیم قرن بعدی هنوز موای میدی؟", message_id=msg.get("message_id"))
							except:
								print("err sihash")
                                
						elif msg.get("text").startswith("دانلود سطح") or msg.get("text").startswith("سطح"):
							try:
								bot.sendMessage(target, "فرایند دانلود سطح برای این نوب آغاز شد.⇧⇧⇧████████▓▓▓70درصد❌ارور 404 این فرد یک نوب خالص است.!!!!❌", message_id=msg.get("message_id"))
							except:
								print("err sinoh")
                                
						elif msg.get("text").startswith("سلاپ") or msg.get("text").startswith("سلاپ"):
							try:
								bot.sendMessage(target, "برگرد به سیرکت", message_id=msg.get("message_id"))
							except:
								print("err chel")
                                
						elif msg.get("text").startswith("جیگرم") or msg.get("text").startswith("جیگر"):
							try:
								bot.sendMessage(target, "مرتیکه گیخوار گی", message_id=msg.get("message_id"))
							except:
								print("err celyek")
                                
						elif msg.get("text").startswith("😂❤") or msg.get("text").startswith("❤😂"):
							try:
								bot.sendMessage(target, "قلب براچی دادی . نکنه دوباره میخوای مخمو بزنی بیام لواط باهات", message_id=msg.get("message_id"))
							except:
								print("err cheldo")
                                
						elif msg.get("text").startswith("😐💔") or msg.get("text").startswith("💔😐"):
							try:
								bot.sendMessage(target, "چته سد", message_id=msg.get("message_id"))
							except:
								print("err chelse")
                                
						elif msg.get("text").startswith("حاجی") or msg.get("text").startswith("حجی"):
							try:
								bot.sendMessage(target, "حاجی؟ 😐😂", message_id=msg.get("message_id"))
							except:
								print("err chelchar")
                                
						elif msg.get("text").startswith("دعوا") or msg.get("text").startswith("دعوا باز"):
							try:
								bot.sendMessage(target, "هروز دعوا هس😂", message_id=msg.get("message_id"))
							except:
								print("err chelpang")
                                
						elif msg.get("text").startswith("رضا") or msg.get("text").startswith("رضاا"):
							try:
								bot.sendMessage(target, "دوقلو بزا🥺", message_id=msg.get("message_id"))
							except:
								print("err chelshish")
                                
						elif msg.get("text").startswith("سلام") or msg.get("text").startswith("سلم"):
							try:
								bot.sendMessage(target, "سلام دختری ؟", message_id=msg.get("message_id"))
							except:
								print("err chelhaf")
                                
						elif msg.get("text").startswith("بگو هایا") or msg.get("text").startswith("هایا"):
							try:
								bot.sendMessage(target, " سام بادی گیو می هایااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااهههههههههههههههههههههه", message_id=msg.get("message_id"))
							except:
								print("err chelhash")
                                
						elif msg.get("text").startswith("بات") or msg.get("text").startswith("بات"):
							try:
								bot.sendMessage(target, "اخه کی به گوربه میگه بات دلقک کصپدر", message_id=msg.get("message_id"))
							except:
								print("err chelnoh")
                                
						elif msg.get("text").startswith("سکوت") or msg.get("text").startswith("سکوت"):
							try:
								bot.sendMessage(target, "!این اخطار اخر بود ملعون ! سکوت کن ای ملعون! تا از گروه ریم نشدی 🫂", message_id=msg.get("message_id"))
							except:
								print("err panjah")
                                
						elif msg.get("text").startswith("زیر ابیا") or msg.get("text").startswith("زیر ابیا"):
							try:
								bot.sendMessage(target, "برگرد به سیرکت . مگه اینجا دریاس؟", message_id=msg.get("message_id"))
							except:
								print("err pyek")
                                
						elif msg.get("text").startswith("کوفت") or msg.get("text").startswith("کوفت"):
							try:
								bot.sendMessage(target, "ک= کل وجودم  و=واقعا  ف=فدای  ت=تو🥲💜", message_id=msg.get("message_id"))
							except:
								print("err pdo")
                                
						elif msg.get("text").startswith("💜") or msg.get("text").startswith("💜"):
							try:
								bot.sendMessage(target, "فقط اونجا که سپهر میگه:برام فرستاد یه قلب بنفش شاید باز میخاد بزاره سربه سرم  نده دیوث 😐😂حصله عشق و عاشقی و رابطه ندارم 😑😐", message_id=msg.get("message_id"))
							except:
								print("err pse")
                                
						elif msg.get("text").startswith("💙") or msg.get("text").startswith("💙"):
							try:
								bot.sendMessage(target, "(منظورم اینه مرسی از خایمالیت)😉❤میدونم رفیقمی", message_id=msg.get("message_id"))
							except:
								print("err pchar")
                                
						elif msg.get("text").startswith("❤") or msg.get("text").startswith("❤"):
							try:
								bot.sendMessage(target, "میدونم عاشقمی🥺❤", message_id=msg.get("message_id"))
							except:
								print("err phaf")
                                
						elif msg.get("text").startswith("کون میخام") or msg.get("text").startswith("کون میقام"):
							try:
								bot.sendMessage(target, "مرتیکه گی", message_id=msg.get("message_id"))
							except:
								print("err phash")
                                
						elif msg.get("text").startswith("ممه بدید") or msg.get("text").startswith("ممه"):
							try:
								bot.sendMessage(target, "نه دا", message_id=msg.get("message_id"))
							except:
								print("err pnoh")
                                
						elif msg.get("text").startswith("مردید؟") or msg.get("text").startswith("مردین"):
							try:
								bot.sendMessage(target, "برگرد به سیرکت", message_id=msg.get("message_id"))
							except:
								print("err shas")
                                
						elif msg.get("text").startswith("عزیزم") or msg.get("text").startswith("عزیزم"):
							try:
								bot.sendMessage(target, "داش من گی نیستم به مولا بیخیال ما شو", message_id=msg.get("message_id"))
							except:
								print("err shyek")
                                
						elif msg.get("text").startswith("رل زدم") or msg.get("text").startswith("رل زدم"):
							try:
								bot.sendMessage(target, "به دکم", message_id=msg.get("message_id"))
							except:
								print("err shdo")
                                
						elif msg.get("text").startswith("سید") or msg.get("text").startswith("سید"):
							try:
								bot.sendMessage(target, "جان سید ،سید فدات شه😃", message_id=msg.get("message_id"))
							except:
								print("err shse")
                                
						elif msg.get("text").startswith("گشنمه") or msg.get("text").startswith("گشنمه"):
							try:
								bot.sendMessage(target, "بخورش 👇", message_id=msg.get("message_id"))
							except:
								print("err shechar")
                                
						elif msg.get("text").startswith("زندگی من کیه") or msg.get("text").startswith("زندگی من کیهه"):
							try:
								bot.sendMessage(target, "منم عزیزم🥺(لواط)", message_id=msg.get("message_id"))
							except:
								print("err shehaf")
                                
						elif msg.get("text").startswith("بوس بده") or msg.get("text").startswith("بوس"):
							try:
								bot.sendMessage(target, "داش اگه میخوای لواط کنی لازم نیس از این دلقک بازیا  در بیاری", message_id=msg.get("message_id"))
							except:
								print("err shehash")
                                
						elif msg.get("text").startswith("هن") or msg.get("text").startswith("هن"):
							try:
								bot.sendMessage(target, "خ", message_id=msg.get("message_id"))
							except:
								print("err shenoh")
                                
						elif msg.get("text").startswith("چایی") or msg.get("text").startswith("چای"):
							try:
								bot.sendMessage(target, "فن امیر توسلی دا ؟ هعب", message_id=msg.get("message_id"))
							except:
								print("err haftad")
                                
						elif msg.get("text").startswith("تکس") or msg.get("text").startswith("تکص"):
							try:
								bot.sendMessage(target, "حتما منتظری تکس بدم؟😐چس مست کنم؟🤣", message_id=msg.get("message_id"))
							except:
								print("err hfyek")
                                
						elif msg.get("text").startswith("بیشعور") or msg.get("text").startswith("بیشعور"):
							try:
								bot.sendMessage(target, "(میدونم که دلقکم)❌\nدر حال نصب شعور...\nn██████████▓99درصد\nارور407🥀💔\nاین فرد ذاتی بیشعور است و قابلیت نصب شعور برای آن وجود ندارد.!", message_id=msg.get("message_id"))
							except:
								print("err hafdo")
                                
						elif msg.get("text").startswith("احمق") or msg.get("text").startswith("احمق"):
							try:
								bot.sendMessage(target, "به تو رفتم سید", message_id=msg.get("message_id"))
							except:
								print("err hafse")
                                
						elif msg.get("text").startswith("ربات کیه") or msg.get("text").startswith("ربات کیه"):
							try:
								bot.sendMessage(target, "ربات پدرته", message_id=msg.get("message_id"))
							except:
								print("err hafch")
                                
						elif msg.get("text").startswith("سازندت کیه") or msg.get("text").startswith("سازنده"):
							try:
								bot.sendMessage(target, "@AIi_Gamer :-)", message_id=msg.get("message_id"))
							except:
								print("err hafpang")
                                
						elif msg.get("text").startswith("جنده") or msg.get("text").startswith("جنده"):
							try:
								bot.sendMessage(target, "چرا یه گوربه باید جنده باشه ؟", message_id=msg.get("message_id"))
							except:
								print("err hafhash")
                                
						elif msg.get("text").startswith("دلم گرفته") or msg.get("text").startswith("دیلم گیرفته"):
							try:
								bot.sendMessage(target, "به چپ و راستوم😐💔", message_id=msg.get("message_id"))
							except:
								print("err hafnoh")
                                
						elif msg.get("text").startswith("ممرضا") or msg.get("text").startswith("ممد"):
							try:
								bot.sendMessage(target, "بزار کونشو بده دا مزاحمش نشو", message_id=msg.get("message_id"))
							except:
								print("err hastad")
                                
						elif msg.get("text").startswith("متین") or msg.get("text").startswith("متیو"):
							try:
								bot.sendMessage(target, "پر قدرت گپ", message_id=msg.get("message_id"))
							except:
								print("err hsyek")
                                
						elif msg.get("text").startswith("تایپره") or msg.get("text").startswith("تایپرم"):
							try:
								bot.sendMessage(target, "تویپرح لشح فرارح کنیدح", message_id=msg.get("message_id"))
							except:
								print("err hashdo")
                                
						elif msg.get("text").startswith("خشاب") or msg.get("text").startswith("خشاب"):
							try:
								bot.sendMessage(target, "داداش دمت گرم بمولا  خیلی مردی منو میخوندی به خدا داره دهنم به فاک میره ای دلم به مولا روده هام از حلقم داره میزنن بیرون میگن باو لنتی چقدر میخندی به خدا دیگه چاره ای برام نزاشتی دارم سرمو میکوبم به دیوار وایی واقعا عالی بود داداش دمت گرم که مارو میخوندی تو حرف نداری داداش یه درجه یک هستی بمولا هرکسی میگه دلقک نیستی گوه خوردی تو واقعا یه دلقک میباشی دهنت سرویس داداش تو بهترین فردی هستی که میتونه ادمارو خوشحال و خندون کنه شرافتا ادامه بدی رتبه یک دلقک رو گرفتی دهنت سرویس واقعا ببین هرچی بگم کمه خیلی خیلی خنده دار هست از بس خندیدم دیونه شدم انگار مست شدم انگار ودکا 100 درصد الکل خوردم دارم میخندم فقط بمولا لپ تاپمو یا گوشیمو دارم خورد میکنم وای اخه از کجات میاری همچین حرفای بابا دهنت سرویس  میخام شمارمو بدم بهت که هر روز برام همچین حرفای بزنی اس ام اس کن برام من بخندم داداش میرم سرکار میرم دستشویی هرجا میرم دوست دارم پیام هاتو بخونم و بخندم واقعا صورتم زیبا میشه اخه هرکی زیاد بخنده زیبا میشه و خوشگل میشه و روحیه ی بسیار عالی داره دقیقا اون فرد تو هستی داداش بمولا اگر این حرفات رو تو کتاب خنده دار ترین جک ها ثبت نکردن هیچی نیستم خیلی عالی هستی چرا داداش این کارتو حرفه ای ادامه نمیدی و به چندتا مبتدی هم یاد بدی تا بقیه رو بخندوننن باو خیلی عالی", message_id=msg.get("message_id"))
							except:
								print("err hsse")
                                
						elif msg.get("text").startswith("لینک") or msg.get("text").startswith("لینک گپ"):
							try:
								bot.sendMessage(target, "https://rubika.ir/joing/BAIDDGGD0SALTSPQMRWMVBOLHBQZLXGH", message_id=msg.get("message_id"))
							except:
								print("err hshch")
                                
						elif msg.get("text").startswith("ممه") or msg.get("text").startswith("ممه"):
							try:
								bot.sendMessage(target, "لولو برد", message_id=msg.get("message_id"))
							except:
								print("err hshpn")
                                
						elif msg.get("text").startswith("گدرت") or msg.get("text").startswith("گدرت"):
							try:
								bot.sendMessage(target, "گدرت در دست بچه ها ۱۰ ۱۲ ساله روبیکاس نه تو 😐", message_id=msg.get("message_id"))
							except:
								print("err hshshish")
                                
						elif msg.get("text").startswith("زهرمار") or msg.get("text").startswith("زرمار"):
							try:
								bot.sendMessage(target, "تو جونت😏😖", message_id=msg.get("message_id"))
							except:
								print("err hshhaf")
                                
						elif msg.get("text").startswith("خوبی عزیزم") or msg.get("text").startswith("خوبی"):
							try:
								bot.sendMessage(target, "مرسی تو خوبی قشنگم؟ اصل میدی؟🤓🫂", message_id=msg.get("message_id"))
							except:
								print("err hashhash")
                                
						elif msg.get("text").startswith("درد") or msg.get("text").startswith("درد"):
							try:
								bot.sendMessage(target, "تو جونت 😘💋", message_id=msg.get("message_id"))
							except:
								print("err hshnoh")
                                
						elif msg.get("text").startswith("افرین") or msg.get("text").startswith("عافرین"):
							try:
								bot.sendMessage(target, "بچه خر میکنی؟😐", message_id=msg.get("message_id"))
							except:
								print("err navad")
                                
						elif msg.get("text").startswith("😂😐") or msg.get("text").startswith("😐😂"):
							try:
								bot.sendMessage(target, "اوففففف تو فقط بخند🤤🙃", message_id=msg.get("message_id"))
							except:
								print("err nayek")
                                
						elif msg.get("text").startswith("نوب") or msg.get("text").startswith("نوبو"):
							try:
								bot.sendMessage(target, "یک عدد نوب یافت شد❌\nدرحال پاکسازی ویروس نوب بودن😐\n█▓▓▓▓▓▓▓▓▓10درصد \n██▓▓▓▓▓▓▓▓20درصد\n███▓▓▓▓▓▓▓30درصد\n████▓▓▓▓▓▓40درصد\n█████▓▓▓▓▓50درصد\n██████▓▓▓▓60درصد\n███████▓▓▓70درصد\n████████▓▓80درصد\n█████████▓90درصد\n██████████ 100 درصد✅\nپاکسازی رو به اتمام است...✅لطفا صبور باشید🗿\nویروس نوب از روی زمین با موفقیت پاک شد.!✅🗿\n", message_id=msg.get("message_id"))
							except:
								print("err nado")
                                
						elif msg.get("text").startswith("سجود") or msg.get("text").startswith("سجاد"):
							try:
								bot.sendMessage(target, "سگاده مث سگ میگادت", message_id=msg.get("message_id"))
							except:
								print("err nase")
                                
						elif msg.get("text").startswith("😕") or msg.get("text").startswith("😕"):
							try:
								bot.sendMessage(target, "خوبی؟", message_id=msg.get("message_id"))
							except:
								print("err nash")
                                
						elif msg.get("text").startswith("نه") or msg.get("text").startswith("ن"):
							try:
								bot.sendMessage(target, "چرا چیشده؟", message_id=msg.get("message_id"))
							except:
								print("err napn")
                                
						elif msg.get("text").startswith("هعی") or msg.get("text").startswith("هعپ"):
							try:
								bot.sendMessage(target, "درست میشه هر مشکلی هست نگران نباش😌❣", message_id=msg.get("message_id"))
							except:
								print("err nash")
                                
						elif msg.get("text").startswith("جیندا") or msg.get("text").startswith("جیندا"):
							try:
								bot.sendMessage(target, "#حق", message_id=msg.get("message_id"))
							except:
								print("err nahf")
                                
						elif msg.get("text").startswith("شاخ") or msg.get("text").startswith("شاخ"):
							try:
								bot.sendMessage(target, "ای شاخ بخاطر گودرتی که داری از اینجا لف بده و ما رو رها کن😪😭", message_id=msg.get("message_id"))
							except:
								print("err nahsh")
                                
						elif msg.get("text").startswith("عاشقتم") or msg.get("text").startswith("عاشقتم"):
							try:
								bot.sendMessage(target, "منم همینطور", message_id=msg.get("message_id"))
							except:
								print("err nano")
                                
						elif msg.get("text").startswith("حوصله ندارم") or msg.get("text").startswith("حصلم"):
							try:
								bot.sendMessage(target, "چرا؟", message_id=msg.get("message_id"))
							except:
								print("err sad")
                                
						elif msg.get("text").startswith("گوه نخور") or msg.get("text").startswith("گو نخور"):
							try:
								bot.sendMessage(target, "تو بخور😃😂", message_id=msg.get("message_id"))
							except:
								print("err sadyek")
                                
						elif msg.get("text").startswith("بات") or msg.get("text").startswith("بات"):
							try:
								bot.sendMessage(target, "هوف چیه", message_id=msg.get("message_id"))
							except:
								print("err saddo")
                                
						elif msg.get("text").startswith("ریدم") or msg.get("text").startswith("ریدم"):
							try:
								bot.sendMessage(target, "دقیقا منم ریدم😐خیلی تنذه", message_id=msg.get("message_id"))
							except:
								print("err sadse")
                                
						elif msg.get("text").startswith("عه") or msg.get("text").startswith("عع"):
							try:
								bot.sendMessage(target, "آره بمولا", message_id=msg.get("message_id"))
							except:
								print("err sadch")
								
						elif msg.get("text").startswith("😂") or msg.get("text").startswith("🤣"):
							try:
								bot.sendMessage(target, "توش رفت ؟", message_id=msg.get("message_id"))
							except:
								print("err luagh")
                                
						elif msg.get("text").startswith("🤣🤣") or msg.get("text").startswith("🤣"):
							try:
								bot.sendMessage(target, "فک کردم بره توت درد داره😐نگو ک کیف داره", message_id=msg.get("message_id"))
							except:
								print("err khikhi")
								
						elif msg.get("text") == "😐":
							try:
								bot.sendMessage(target, "درد بگیری بچه اینقدر اینو نده 😏💔", message_id=msg.get("message_id"))
							except:
								print("err poker answer")

						elif msg.get("text") == "دیوث":
							try:
								bot.sendMessage(target, "کم گوه بخور خودتی🙂💔", message_id=msg.get("message_id"))
							except:
								print("err dayuos")

						elif msg.get("text") == "تست":
							try:
								bot.sendMessage(target, "ᵀᴴᴱ ᴿᴼᴮᴼᵀ ᴵˢ ᴺᴼᵂ ᴬᶜᵀᴵⱽᴱ ✅", message_id=msg.get("message_id"))
							except:
								print("err test bot")
								
						elif msg.get("text") == "سنجاق" and msg.get("author_object_guid") in admins :
							try:
								bot.pin(target, msg["reply_to_message_id"])
								bot.sendMessage(target, "ᵀᴴᴱ ᴹᴱˢˢᴬᴳᴱ ᵂᴬˢ ˢᵁᶜᶜᴱˢˢᶠᵁᴸᴸᵞ ᴾᴵᴺᴺᴱᴰ!", message_id=msg.get("message_id"))
							except:
								print("err pin")
								
						elif msg.get("text") == "برداشتن سنجاق" and msg.get("author_object_guid") in admins :
							try:
								bot.unpin(target, msg["reply_to_message_id"])
								bot.sendMessage(target, "ᵀᴴᴱ ᴹᴱˢˢᴬᴳᴱ ᵂᴬˢ ᴿᴱᴹᴼⱽᴱᴰ ᶠᴿᴼᴹ ᵀᴴᴱ ᴾᴵᴺ!", message_id=msg.get("message_id"))
							except:
								print("err unpin")
								
						elif msg.get("text").startswith("!trans"):
							try:
								responser = get(f"https://api.codebazan.ir/translate/?type=json&from=en&to=fa&text={msg.get('text').split()[1:]}").json()
								al = [responser["result"]]
								bot.sendMessage(msg.get("author_object_guid"), "پاسخ به ترجمه:\n"+"".join(al)).text
								bot.sendMessage(target, "ᴵ ˢᴱᴺᵀ ᵞᴼᵁ ᵀᴴᴱ ᴿᴱˢᵁᴸᵀ 😘", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "ᴱᴺᵀᴱᴿ ᵀᴴᴱ ᶜᴼᴹᴹᴬᴺᴰ ᶜᴼᴿᴿᴱᶜᵀᴸᵞ 😁", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("!font"):
							try:
								response = get(f"https://api.codebazan.ir/font/?text={msg.get('text').split()[1]}").json()
								bot.sendMessage(msg.get("author_object_guid"), "\n".join(list(response["result"].values())[:110])).text
								bot.sendMessage(target, "ᴵ ˢᴱᴺᵀ ᵞᴼᵁ ᵀᴴᴱ ᴿᴱˢᵁᴸᵀ 😘", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "ᴱᴺᵀᴱᴿ ᵀᴴᴱ ᶜᴼᴹᴹᴬᴺᴰ ᶜᴼᴿᴿᴱᶜᵀᴸᵞ 😁", message_id=msg["message_id"])
						
						elif msg.get("text").startswith("جوک") or msg.get("text").startswith("jok") or msg.get("text").startswith("!jok"):
							try:
								response = get("https://api.codebazan.ir/jok/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ᵞᴼᵁ ᴱᴺᵀᴱᴿᴱᴰ ᵀᴴᴱ ᴼᴿᴰᴱᴿ ᴵᴺᶜᴼᴿᴿᴱᶜᵀᴸᵞ", message_id=msg["message_id"])
							
						elif msg.get("text").startswith("ذکر") or msg.get("text").startswith("zekr") or msg.get("text").startswith("!zekr"):
							try:
								response = get("http://api.codebazan.ir/zekr/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("حدیث") or msg.get("text").startswith("hadis") or msg.get("text").startswith("!hadis"):
							try:
								response = get("http://api.codebazan.ir/hadis/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("بیو") or msg.get("text").startswith("bio") or msg.get("text").startswith("!bio"):
							try:
								response = get("https://api.codebazan.ir/bio/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
								
						elif msg["text"].startswith("!weather"):
							try:
								response = get(f"https://api.codebazan.ir/weather/?city={msg['text'].split()[1]}").json()
								bot.sendMessage(msg["author_object_guid"], "\n".join(list(response["result"].values())[:20])).text
								bot.sendMessage(target, "نتیجه بزودی برای شما ارسال خواهد شد...", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("دیالوگ"):
							try:
								response = get("http://api.codebazan.ir/dialog/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
							
						elif msg.get("text").startswith("دانستنی"):
							try:
								response = get("http://api.codebazan.ir/danestani/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ᵞᴼᵁ ᴱᴺᵀᴱᴿᴱᴰ ᵀᴴᴱ ᴼᴿᴰᴱᴿ ᴵᴺᶜᴼᴿᴿᴱᶜᵀᴸᵞ", message_id=msg["message_id"])
                                
						elif msg.get("text").startswith("همسر"):
							try:
								response = get("https://api.codebazan.ir/name/?type=json").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ᵞᴼᵁ ᴱᴺᵀᴱᴿᴱᴰ ᵀᴴᴱ ᴼᴿᴰᴱᴿ ᴵᴺᶜᴼᴿᴿᴱᶜᵀᴸᵞ", message_id=msg["message_id"])	
								
						elif msg.get("text").startswith("پ ن پ") or msg.get("text").startswith("!pa-na-pa") or msg.get("text").startswith("په نه په"):
							try:
								response = get("http://api.codebazan.ir/jok/pa-na-pa/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("الکی مثلا") or msg.get("text").startswith("!alaki-masalan"):
							try:
								response = get("http://api.codebazan.ir/jok/alaki-masalan/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("داستان") or msg.get("text").startswith("!dastan"):
							try:
								response = get("http://api.codebazan.ir/dastan/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "There was a problem!", message_id=msg["message_id"])
							
						elif msg.get("text").startswith("!ping"):
							try:
								responser = get(f"https://api.codebazan.ir/ping/?url={msg.get('text').split()[1]}").text
								bot.sendMessage(target, responser,message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "ᴵ ˢᴱᴺᵀ ᵞᴼᵁ ᵀᴴᴱ ᴿᴱˢᵁᴸᵀ 😘", message_id=msg["message_id"])
								
						elif "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
							try:
								print("Yek ahmagh forwared Zad")
								bot.deleteMessages(target, [str(msg.get("message_id"))])
								print("tabligh forearedi pak shod")
							except:
								print("err delete forwared")
						
						elif msg.get("text") == "قوانین":
							try:
								rules = open("rules.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err ghanon")
							
						elif msg.get("text").startswith("آپدیت قوانین") and msg.get("author_object_guid") in admins:
							try:
								rules = open("rules.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت قوانین")))
								bot.sendMessage(target, "✅ Rules updated", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ ᵞᴼᵁ ᴱᴺᵀᴱᴿᴱᴰ ᵀᴴᴱ ᴼᴿᴰᴱᴿ ᴵᴺᶜᴼᴿᴿᴱᶜᵀᴸᵞ", message_id=msg.get("message_id"))

						elif msg.get("text") == "حالت آرام" and msg.get("author_object_guid") in admins:
							try:
								number = 10
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ ᵞᴼᵁ ᴱᴺᵀᴱᴿᴱᴰ ᵀᴴᴱ ᴼᴿᴰᴱᴿ ᴵᴺᶜᴼᴿᴿᴱᶜᵀᴸᵞ", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "!speak" or msg.get("text") == "ویس" or msg.get("text") == "Speak" or msg.get("text") == "بگو":
							try:
								if msg.get('reply_to_message_id') != None:
									msg_reply_info = bot.getMessagesInfo(target, [msg.get('reply_to_message_id')])[0]
									if msg_reply_info['text'] != None:
										text = msg_reply_info['text']
										speech = gTTS(text)
										changed_voice = io.BytesIO()
										speech.write_to_fp(changed_voice)
										b2 = changed_voice.getvalue()
										changed_voice.seek(0)
										audio = MP3(changed_voice)
										dur = audio.info.length
										dur = dur * 1000
										f = open('sound.ogg','wb')
										f.write(b2)
										f.close()
										bot.sendVoice(target , 'sound.ogg', dur,message_id=msg["message_id"])
										os.remove('sound.ogg')
										print('sended voice')
								else:
									bot.sendMessage(target, 'Your message has no text or caption',message_id=msg["message_id"])
							except:
								print('server gtts bug')
							
						elif msg.get("text") == "برداشتن حالت آرام" and msg.get("author_object_guid") in admins:
							try:
								number = 0
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام غیرفعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "ᵞᴼᵁ ᴱᴺᵀᴱᴿᴱᴰ ᵀᴴᴱ ᴼᴿᴰᴱᴿ ᴵᴺᶜᴼᴿᴿᴱᶜᵀᴸᵞ!", message_id=msg.get("message_id"))


						elif msg.get("text").startswith("اخطار") and msg.get("author_object_guid") in admins:
							try:
								user = msg.get("text").split(" ")[1][1:]
								guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									alert(guid,user)
									
								else :
									bot.sendMessage(target, "❌ The user is an admin", message_id=msg.get("message_id"))
									
							except IndexError:
								guid = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
								user = bot.getUserInfo(guid)["data"]["user"]["username"]
								if not guid in admins:
									alert(guid,user)
								else:
									bot.sendMessage(target, "❌ The user is an admin", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ Please enter the command correctly", message_id=msg.get("message_id"))



						elif msg.get("text") == "قفل گروه" and msg.get("author_object_guid") in admins :
							try:
								bot.setMembersAccess(target, ["AddMember"])
								bot.sendMessage(target, "🔒 The group was locked", message_id=msg.get("message_id"))
							except:
								print("err lock GP")

						elif msg.get("text") == "بازکردن گروه" or msg.get("text") == "باز کردن گروه" and msg.get("author_object_guid") in admins :
							try:
								bot.setMembersAccess(target, ["SendMessages","AddMember"])
								bot.sendMessage(target, "🔓 The group is now open", message_id=msg.get("message_id"))
							except:
								print("err unlock GP")

					else:
						if msg.get("text") == "!start" or msg.get("text") == "روشن" and msg.get("author_object_guid") in admins :
							try:
								sleeped = False
								bot.sendMessage(target, "The robot was successfully lit!", message_id=msg.get("message_id"))
							except:
								print("err on bot")
								
				elif msg["type"]=="Event" and not msg.get("message_id") in answered and not sleeped:
					name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
					data = msg['event_data']
					if data["type"]=="RemoveGroupMembers":
						try:
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"️ User {user} Successfully removed from the group.", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err rm member answer")
					
					elif data["type"]=="AddedGroupMembers":
						try:
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"Hi {user} Dear 😘🌹\n • Welcome to the {name} group 😍❤️\nPlease follow the rules.\n 💎 Send the word (rules) to see enough rules!\nManufacturer: @Sajad_Venus", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err add member answer")
					
					elif data["type"]=="LeaveGroup":
						try:
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"Bye {user} 👋 ", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err Leave member Answer")
							
					elif data["type"]=="JoinedGroupByLink":
						try:
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"Hi {user} Dear 😘🌹\n • Welcome to the {name} group 😍❤️\nPlease follow the rules.\n 💎 Send the word (rules) to see enough rules!\nManufacturer: @Sajad_Venus", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err Joined member Answer")
							
				else:
					if "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("message_id")])
						guid = msg.get("author_object_guid")
						user = bot.getUserInfo(guid)["data"]["user"]["username"]
						bot.deleteMessages(target, [msg.get("message_id")])
						alert(guid,user,True)
					
					continue
			except:
				continue

			answered.append(msg.get("message_id"))
			print("[" + msg.get("message_id")+ "] >>> " + msg.get("text") + "\n")

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue
