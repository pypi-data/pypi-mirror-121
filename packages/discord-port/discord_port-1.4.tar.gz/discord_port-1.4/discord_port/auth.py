import requests
import json
import os

class AuthClient:
    def __init__(self,client_id:str=None,client_secret:str=None,redirect_uri:str=None) -> None:
        """
        This is the AuthClient class where you bot your bot info or get it from 
        `/settings/discord-passport.json`

        `JSON file structure`
        
        ```json
        {
            "client_id":"",
            "client_secret":"",
            "redirect_uri":""
        }
        ```

        """
        if os.path.isfile('./config/discord_port.json'): data = json.load(open('./config/discord_port.json','r'))
        else: data = {'client_id':client_id,'client_secret':client_secret,'redirect_uri':redirect_uri}
        "Make the data globally in the class functions "
        self.data = data

    def get_code(self,code:str):
        payload = {
            'client_id':self.data.get('client_id'),
            'client_secret':self.data.get('client_secret'),
            'grant_type':'authorization_code',
            'code':code,
            'redirect_uri':self.data.get('redirect_uri')
        }
        request = requests.post('https://discord.com/api/v9/oauth2/token',data=payload,headers={'Content-Type': 'application/x-www-form-urlencoded'})
        return request.json()
        