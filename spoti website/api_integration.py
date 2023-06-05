import base64
import datetime
import random

import requests


class Client:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiration = None

    def get_access_token(self):
        if self.access_token and datetime.datetime.now() < self.token_expiration:
            print("Token is valid")
            return False
        else:
            client_creds = f"{self.client_id}:{self.client_secret}"
            encoded_client_creds = base64.b64encode(client_creds.encode())
            request_data = {'grant_type': 'client_credentials'}
            request_headers = {'Authorization': f'Basic {encoded_client_creds.decode()}'}
            request_url = 'https://accounts.spotify.com/api/token'
            req = requests.post(request_url, data=request_data, headers=request_headers)
            if req.status_code != 200:
                raise Exception("error")
            req = req.json()
            self.token_expiration = datetime.datetime.now() + datetime.timedelta(seconds=req['expires_in'])
            self.access_token = req['access_token']
            return req

    def get_random_artist(self):
        self.get_access_token()
        current_year = datetime.datetime.now().year
        min_year = 1950  #arbitrary and should be decided later
        # spotify suggests a workaround in order to get a random artist
        # https://developer.spotify.com/documentation/web-api/reference/artists/get-artist/#frequently-asked-questions
        random_year = random.randint(min_year, current_year)
        artist_req_header = {"Authorization": f"Bearer {self.access_token}"}
        artist_by_year_req_data = {"q": f"year:{random_year}", "type": 'artist'}
        artist_req_url = "https://api.spotify.com/v1/search"
        req_artists_in_year = requests.get(artist_req_url, params=artist_by_year_req_data, headers=artist_req_header)
        if req_artists_in_year.status_code != 200:
            raise Exception("error")
        random_artist_req_data = artist_by_year_req_data
        random_artist_req_data.update({'limit': 1, 'offset': random.randint(0, 2000)})
        # spotify limits max offset you are able to do  
        random_artist = requests.get(artist_req_url, params=random_artist_req_data, headers=artist_req_header)
        return random_artist.json()




