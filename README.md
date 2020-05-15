# encouragement-bot
Lloyd Black
May 15, 2020

# v1
A simple python script that uses Google's SMTP server to send out encouraging texts every so often.

# v2
## v2.0
Adds ability to support multiple clients with multiple message frequencies, plus adds some randomization to encouragement messages.
Server shell is fairly janky, but is more or less functional.

## v2.1
Adds tracking of time last message was sent, which allows for shutting down the Encouragementbot Server without sending clients in a client file messages pre-emptively on startup.
Server shell still janky, threading with shared resources is hard.

## v2.2
Moves the list of encouraging messages to a text file named "Encouragements.txt", which can be refreshed while the server is running without shutting down the program