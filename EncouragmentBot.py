import smtplib
import time

server = smtplib.SMTP("smtp.gmail.com", 587)

server.starttls()

server.login('lloydblacktrash@gmail.com', 'dtincjsaaaeirxft')

message = """From: Lloyd's encouragement bot <lloydblacktrash@gmail.com>
To: Valued encouragement bot client <8582487066@vtext.com>

You're doing great sweetie keep up the good work <3
"""

while True:
	server.sendmail("Lloyd's encouragement bot", '8582487066@vtext.com', message)
	print("Text sent")
	time.sleep(60)

server.quit()
