import requests
from urllib.parse import quote_plus


def ydkgenerator(decklist):
  request_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php?name="
  parsedTCGP = ['#main\n']
  
  #Open file to read, create api request URL and createintermidiary list before name-to-ID
  try:
      for cname in decklist:
        request_URL += f"{quote_plus(cname)}|"
        
  
  except OSError:
      print(f"Can't open {fname}!\nCheck name/path spelling,file is from TCGPlayer or make sure the file exists.")
      exit(1) 
  #Condensed API call and name-to-ID conversion 
  
  request_URL = request_URL[:-1]
  api_get = requests.get(request_URL)
  api_json = api_get.json()
  
 
  for card in decklist:
    for item in api_json['data']:
      if item['name'] == card:
        parsedTCGP.append((str(item['id']) + '\n'))
        
  
  parsedTCGP.append('#extra\n' + '!side')
  ydkfile = ''.join(parsedTCGP)

  return ydkfile

  


