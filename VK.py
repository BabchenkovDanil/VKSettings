from urllib.parse import urlencode
import requests
import os
from dotenv import load_dotenv
from pprint import pprint

# VK_ID = 53612501
# AUT_BASE_URL = 'https://oauth.vk.com/authorize'
# params = {
#     'client_id': VK_ID,
#     'redirect_uri': 'https://oauth.vk.com/blank.html',
#     'v': 5.199,
#     'response_type': 'token',
#     'display': 'page',
#     'scope': 'friends, status, wall, photos'
# }
#
# AUT_URL = f'{AUT_BASE_URL}?{urlencode(params)}'
# print(AUT_URL)

load_dotenv()
token_danil = os.getenv('VK_TOKEN')


class VKSettings:
    API_URL = 'https://api.vk.com/method'
    API_V = 5.199

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': self.API_V,
            'user_id': self.user_id
        }

    def build_url(self, api_method):
        return f'{self.API_URL}/{api_method}'

    def get_all_info(self):
        params = self.get_common_params()
        params.update({
            'fields': 'first_name, last_name, sex, bdate, city, country'
        })
        response = requests.get(self.build_url('users.get'), params=params)
        return response.json()

    def get_my_friends(self):
        params = self.get_common_params()
        params.update({
            'fields': 'first_name, last_name, registration_date',
            'count': 1000
        })
        response = requests.get(self.build_url('friends.get'), params=params)
        friends = response.json()
        return friends['response']['items']

    def get_status(self):
        params = self.get_common_params()
        response = requests.get(self.build_url('status.get'), params=params)
        return response.json()

    def get_post(self):
        params = self.get_common_params()
        params.update({
            'owner_id': self.user_id,
            'count': 10,
            'filter': 'owner'
        })
        response = requests.get(self.build_url('wall.get'), params=params)
        return response.json()

    def get_photos(self):
        params = self.get_common_params()
        params.update({
            'owner_id': self.user_id,
            'album_id': 'profile',
            'extended': 1
        })
        response = requests.get(self.build_url('photos.get'), params=params)
        return response.json()

    def get_very_likes_photo(self, photos):
        photo = photos
        photo = photo['response']['items']
        for i in photo:
            return f'фотографии {i['likes'].get('count')} лайков'









if __name__ == '__main__':
    vk_user = VKSettings(token_danil, 195322662)

    info = vk_user.get_my_friends()
    status = vk_user.get_status()
    post = vk_user.get_post()
    post_count = post['response']['count']
    photo = vk_user.get_photos()
    likes = vk_user.get_very_likes_photo(photo)
    pprint(likes)