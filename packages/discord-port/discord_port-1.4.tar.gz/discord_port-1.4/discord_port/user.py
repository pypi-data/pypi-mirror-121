import requests

class UserAPI:
    def __init__(self,code:str) -> None:
        """Make the UserAPI is much easier than every and you can reach and edit the data very easily now :0"""
        if not id:
            print("No ID provided! Check your code!")
            return
        self.code = code

    @property
    def get_user(self):
        "Get the user json from the discord api by sending a get request!"
        request = requests.get('https://discord.com/api/v9/users/@me',headers={"Authorization": f"Bearer {self.code}"})
        return request.json()