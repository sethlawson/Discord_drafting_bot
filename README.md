# Discord_drafting_bot
A discord bot for multiplayer card drafting, with deck mapping functionality for Yugioh! cards

All of this bot's events occur asynchronously in response to messages. 
To use, replace token with your own, ideally pulling it from a seperate file.
Replace 2011list1.txt with your list of cards. 
Replace all instances of embed_listformatter with packlist_formatter to play with non-Yugioh cards.
Change any varaibles to fit the dimensions of your desired game, specifically numRounds and packsize.

Gameplay goes as follows:
A member of a discord with this botcan either pm the bot or publicly post '!qoob'
Any member of the channel can '!join' the cube by pming the bot, including (its not done automatically!) the host
Once ready, the host can pm the bot '!start' to begin the drafting process.
The bot will shuffle the strings and will 'deal' packsize number of strings to each player by pm, with indexes next to each string. Players will draft a string by pming the bot the number's index. Once all players have submitted a choice, the bot will rotate the packs, and the next round will begin.  

!mylist at any time to see the cards you've chosen. 
!myfile at any time to recieve a PM of your ydk file corresponding to those chosen cards.
