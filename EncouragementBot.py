import smtplib
import time
import threading
import random
import sys

random.seed(time.time())

providers = {
	"att" : "@mms.att.net",
	"verizon" : "@vzwpix.com",
	"tmobile" : "@tmomail.net",
	"sprint" : "@pm.sprint.com",
	"virgin" : "@vmpix.com",
	"cricket" : "@mms.cricketwireless.net",
	"boost" : "@myboostmobile.com",
	"email" : ""
}

encouragements = ["You're doing great sweetie keep up the good work",
				  "I can see that you're rocking it, and that's coming from a bot so you know it's true",
				  "When I grow up to be a human, I want to be just like you",
				  "I saw a strongman competition the other day and thought of you, but like emotionally",
				  "You've got this yo\nI believe in you",
				  "Remember, you have people who love you that you can lean on if you need to\nLike me, Encouragementbot!",
				  "01101100 01101111 01110110 01100101 00100000 01111001 01101111 01110101 00101100 00100000 01100010 01101111 01101111",
				  "You improve the world just by being you",
				  "You're a beacon of light in the darkness",
				  "Did you know sea otters hold hands when they sleep to keep from drifting apart?\nI know that isn't exactly encouraging but boy is it adorable",
				  "I see trees of green\nRed roses too\nBut that's just ok\nNext to the beauty in you",
				  "Here's a haiku for you:\nSo there's this person\nBrave and strong and capable\nAnd reading this text",
				  "My fortune cookie told me 'A partnership shall prove successful for you'\nI'm certain it was talking about this one",
				  "If life gives you lemons, you can make lemonade\nBut that lemonade'll suck without you, sugar",
				  ":)",
				  "I know I'm programmed to say this, but you really are a wonderful person and everyone who says different is thoroughly mistaken",
				  "Well gee golly there pardner, you make me happier than a hedgehog with a pop-proof balloon",
				  "There are doubtless subtle surprises ahead, but you are ready, whatever they may be"
]



# Used for managing people to send texts to
class client(threading.Thread):

	# string (Eric, Lisa, etc), string (att, verizon, email, etc), string (phone number or email address), int (how often, in hours), float (last message time)
	def __init__(self, name, provider, address, frequency, lastmessagetime):
		
		threading.Thread.__init__(self)

		if provider not in providers:
			print("Provider not supported")
			return
		
		self.name = name
		self.address = address + providers[provider]
		
		if frequency < 1:
			self.frequency = 168
		else:
			self.frequency = frequency
		
		temp = "From: Lloyd's Encouragementbot\n"
		temp += "To: " + name + " <" + self.address + ">\n"
		if provider == "email":
			temp += "Subject: An Encouragment Just for You!\n\n"
		self.template = temp
		
		self.active = True

		self.lastmessagetime = lastmessagetime


	# Sends an encouragement to send to the client using Google's SMTP server
	def send_message(self, encouragement):
		message = self.template
		message += "Hey, " + self.name + "!\n"
		message += encouragement + "\n<3, Encouragementbot\n"

		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login('<youremail>@<domain>', '<password>')
		server.sendmail("Lloyd's Encouragementbot", self.address, message)
		server.quit()

		self.lastmessagetime = time.time()


	# Updates the user's last message sent time in client list.
	def update_in_file(self):

		filename = ""

		if len(sys.argv) == 2:
			filename = sys.argv[1]
		else:
			filename = "Clients.txt"

		lines = None

		with open(filename, "r") as f:
			found = False
			lines = f.readlines()
			
			for i, line in enumerate(lines):
				attr = line.split('-')
				if attr[0] == self.name:
					found = True
					attr[4] = str(time.time())
					lines[i] = '-'.join(attr) + '\n'
					break

			if not found:
				lines.append(self.name + '-' + self.provider + '-' + self.address + '-' + str(self.frequency) + '-' + str(time.time()))


		with open(filename, "w") as f:
			for line in lines:
				f.write(line)



	# Loop that sends message to clients at their given frequency
	def run(self):

		if self.lastmessagetime != None:
			nextmsgtime = self.lastmessagetime + (self.frequency * 3600) - 2
			if time.time() < nextmsgtime:
				time.sleep(nextmsgtime - time.time())

		while self.active:

			threadLock.acquire()

			encouragment = random.choice(encouragements)
			self.send_message(encouragment)
			print("\nMessage sent to " + self.name + " at " + time.ctime(time.time()))
			print("encouragementbot-hub >> ", end="")

			self.update_in_file()

			threadLock.release()

			self.lastmessagetime = time.time()

			time.sleep((self.frequency * 3600) - 2)

			


# "Main method"
threadLock = threading.Lock()

clientlist = []

if len(sys.argv) == 2:
	clienttextfilename = sys.argv[1]
	with open(clienttextfilename) as file:
		lines = file.readlines()
		for line in lines:
			if line == '\n':
				continue
			attr = line.split('-')
			newc = client(attr[0], attr[1], attr[2], int(attr[3]), float(attr[4]))
			clientlist.append(newc)
			newc.start()



# Used for server operations, adding and removing clients, etc
cmd = [""]
while cmd[0] != "shutdown":

	cmd = input("encouragementbot-hub >> ").split()

	if len(cmd) == 0:
		continue

	if cmd[0] == "clientlist":
		for c in clientlist:
			print(c.name + " - msg every " + str(c.frequency) + " hours - last message sent " + time.ctime(c.lastmessagetime))
		
	elif cmd[0] == "remove":
		for c in clientlist:
			if c.name == cmd[1]:
				c.active = False
				clientlist.remove(c)
				break
		
	elif cmd[0] == "addclient":
		threadLock.acquire()
		nm = input("Name: ")
		prov = input("Provider: ")
		addr = input("Address/number: ")
		freq = int(input("Frequency (hours): "))
		threadLock.release()
		newc = client(nm, prov, addr, freq, 0.0)
		clientlist.append(newc)
		newc.start()

	else:
		print("""  clientlist -- lists clients by name and frequency of encouragement
  remove <client name> -- removes a client from the encouragment list
  addclient -- prompts for items to add a client to the list
  shutdown -- kills server
  help -- prints this message""")
