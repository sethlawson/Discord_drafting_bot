 #some assets we use in index_msg_funnel
import discord

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


def turncomplete(players):
  bool_list = []
  for player in players:
    bool_list.append(players[player]['chosecard'])
  turncomplete = all(bool_list)
  return turncomplete


async def index_msg_funnel(message, players, listOfPacks, username):
  if username in players:
    #this variable is reset to false with every message, and then reassigned when program gets to line 41
    bool_turncomplete = False
    
    if int(message) in range(len(listOfPacks[players[username]['pack_index']])): 
      players[username]['chosecard'] = True
      bool_turncomplete = turncomplete(players)
      players[username]['card_index'] = int(message)
      players[username]['chosencards'].append(listOfPacks[players[username]['pack_index']][players[username]['card_index']])
      await username.send('Your selection of #' + players[username]['chosencards'][-1] + ' has been logged')
      
    #heres the special sauce with bool_turncomplete. if the int from a player that the bot recieved resulted in line 41 finally getting assigned == True, we update the game. The rest of this script occurs following that last players[username]['cardchosen'] getting set to true 

    if bool_turncomplete:
      numPlayers = len(players)      
      #this bit updates all packs, then the player values, 
      for player in players:
        listOfPacks[players[player]['pack_index']].pop(players[player]['card_index'])
        players[player]['pack_index'] = (players[player]['pack_index'] + 1) % numPlayers
        players[player]['chosecard'] = False
      for player in players:
        msg = 'Turn completed\n' + packlist_formatter(listOfPacks[players[player]['pack_index']])
        await player.send(msg)

      #after we poped those cards and adjusted the player selection attributes, we check if the game is complete
      if listOfPacks[0:numPlayers] == [[] for i in range(numPlayers)]:
        del listOfPacks[0:numPlayers]
        if listOfPacks ==[]:
          print('game complete')
          for player in players:
            msg = packlist_formatter(players[player]['chosencards'])
            ###later need to replace line 74 with some function that turns the list of cards into a suitable ydk file
            await player.send('\nAll cards have been distributed to all players, here are yours:' + msg)
          
        else:
          for player in players:
            msg = 'Round completed, all players are recieving a new pack...\nPlease select a card ' + packlist_formatter(listOfPacks[players[player]['pack_index']])
            await player.send(msg)
          
  else:
    await username.send('That wasn\'t a valid index. Choose another.')


