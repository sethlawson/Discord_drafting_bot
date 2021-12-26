token = ''

'''
PHILOSOPHY OF GAME.PY, not necessary to read prior to running the code, but good to check out

index msg funnel now handles everything. 

Upon recieving a valid message from any player: 
1. it initializes a variable 'bool_turncomplete' to be False. 
2. it appends a players card choice to their dictionary 
3     and sets that players 'cardchosen' boolean to be True. 
4. It then reassigns bool_turncomplete using our turncomplete() function, which only returns true if 100% of cardchosen booleans are True. Otherwise it returns false and nothing happens, i.e. we are still waiting for more repsonses for this turn

the index funnel continues, as it is still triggered by that last player having sent their messsage...

if bool_turncomplete is true: 
  we pop the chosen cards from listofpacks and update all the values in our players' dictionary
  if the last pop made our pack lists empty, we delete those packs so future use of listOfPacks[0:numPlayers] returns fresh packs 
     if, by removing those pack lists, listOfPacks is completely empty then we say the game is complete

'''

import discord
import os
import random
import tracemalloc
from replit import db
from math import floor
from game import *
from ydkgenerator import *

client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


#permissions = (cube is running, starting/config/joining stage, , etc.)
permissions = [False for i in range(4)]
#list of names of players
players = {}
#identifies the host
host = ''
#shows which cube is chosen
activelist = ''
cubelist = []
listOfPacks = [] 
#turncomplete = [True for i in range(numPlayers)]

def packlist_formatter(packlist):
  x = 0 
  br = '' 
  newlist = [] 
  msg = ''
  for j in packlist: 
    newlist.append('\n' + '[' + str(x) + '] ' + str(j)) 
    x += 1 
    msg = br.join(newlist) 
  return msg

with open("small pool for testing.txt","r") as File2011:
  activelist = File2011.readlines()
  cubeLength = len(activelist)
  
  for i in range(cubeLength):
    activelist[i] = activelist[i][:-1]
  print('The cube being used has ' + str(cubeLength) + ' cards.') 

random.shuffle(activelist)

@client.event
async def on_message(message):
    username = message.author
    bool_turncomplete = False
    
    
    if message.author == client.user:
        return
##

#########                     START CUBE                       #######
### Host starts cube with !start, and the cube selection begins    ###
### Permissions 0 is set to true to show cube is running           ###
### Permissions 1 is set to True to show the joining stage is open ### 
### Permissions 2 is set to true during cube startup               ###
### Permissions 3 is set to true to show draft has started         ###

    if message.content.startswith('!qoob') and not permissions[1]:
        permissions[0] = True
        permissions[1] = True
        host = username
        print('New qoob started, ' + str(host) + ' is the host!')
        #await message.channel.send(cardlist.keys())
        #await host.send(cardlist.keys())
        await host.send('Input !join to join, then input !begin to start cubin')
        await message.channel.send('A new cube has started, type !join to join.')
        
 
      ###### JOINING STAGE #########

    if message.content.startswith('!join') & permissions[1]:
      print(str(username) + ' has joined the qoob!')
      players[username] = {'chosencards': [], 'pack_index': int(0), 'chosecard': False, 'card_index':0}
      await username.send('Thank you for joining, awaiting the host to start')
      ##print(players) [no longer being used for diagnostics]

      ##### DRAFT STAGE ########

    if message.content.startswith('!begin') & permissions[1]: 
      print(players)
      host = username
      permissions[1] = False
      permissions[2] = True

      #assign pack_indexes for all players in players dict
      i = 0
      for player in players:
        players[player]['pack_index'] = i
        i += 1

        

      numPlayers = len(players)
      playerDeckSize = floor(cubeLength / numPlayers)
      numRounds = 5
      numPacks = numPlayers * numRounds
      packSize = floor(playerDeckSize / numPacks)
      print('---------------------')
      print('numPlayers is ' +     str(numPlayers))
      print('numRounds is ' +      str(numRounds))
      print('playerdecksize is ' + str(playerDeckSize)) 
      print('packSize is ' +       str(packSize))
      print('---------------------')

 
      
      ###code that makes individual pack lists (of length packSize)
      j = 0
      
      for q in range(numPacks):
        alist = []
      
        for i in range(packSize):
          
          alist.append(activelist[j])
          j += 1
        listOfPacks.append(alist)
      for player in players:

        msg = 'The game has started! Type \'!mylist\' at any time to see all the cards you have selected.\n\nFirst turn!' + packlist_formatter(listOfPacks[players[player]['pack_index']])
        await player.send(msg)
      

    #collect messages corresponding to turn information, and send them off to game.py for processing
    if permissions[2] and players[username]['chosecard'] == False and message.content.isnumeric() and listOfPacks != []: 
      #print(players[username])
      await index_msg_funnel(message.content, players, listOfPacks, username)

    #command to get qoob bot to send current list of cards for a player
    if permissions[2] and message.content =='!mylist':
      await username.send(players[username]['chosencards'])
    
    if permissions[2] and message.content =='!myfile':
      with open("result.txt", "w") as file:
        file.write(ydkgenerator(players[username]['chosencards']))
    
    # send file to Discord in message
      with open("result.txt", "rb") as file:
        await username.send("Your file is:", file=discord.File(file, "decklist.ydk"))


client.run(token)
