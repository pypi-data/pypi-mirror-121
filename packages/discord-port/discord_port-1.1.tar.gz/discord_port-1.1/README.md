# Discord Port

## Way to make an easy Oauth2 with discord API

### How it's work?

`pip install discord-port`

# Create AuthClient

```py
import discord_port

passport = discord_port.AuthClient(c,client_id=None,client_secret=None,redirect_uri=None)
```

# Exchange for the code

```py
import discord_port

passport = discord_port.AuthClient(c,client_id=None,client_secret=None,redirect_uri=None)

#This using a framework called FLASK `pip install flask`
@app.route('/discord/api/oauth2')
def oauth():
    paylaod_recived = passport.get_code(request.args["code"])
    """
    The payload will return as 
    {
        "access_token": "6qrZcUqja7812RVdnEKjpzOL4CvHBFG",
        "token_type": "Bearer",
        "expires_in": 604800,
        "refresh_token": "D43f5y0ahjqew82jZ4NViEr2YafMKhue",
        "scope": "identify"
    }
    """
    return paylaod_recived["access_token"]
```

# Get UserLogged

```py
import discord_port

discord_port.UserAPI(code="access_token").get_user
```

### Made by 🇮🇶 Iraqi hands : airbu#1745 in `7:40AM GMT+3`
