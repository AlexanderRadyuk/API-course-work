
# Used modules importing

from time import sleep
import os
import requests
from tqdm import tqdm
from urllib.parse import urlencode
from input_data import app_id, user_id, vktoken, oauth_token

# """Block with personal data
# данные следует держать отдельно от основного кода в файле input_data.py
# и записывать их перед выполнением """


class  URLGet:


    def __init__(self, arg_1 = app_id, auth_url = 'https://oauth.vk.com/authorize' ):
        self.app_id = arg_1
        self.url_for_request = auth_url
        # print(self.app_id, self.auth_url)


    def app_auth(self) :
        parameters_vk = {
            'client_id': self.app_id,
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'display': 'page',
            'scope': 'photos',
            'response_type': 'token',
            'v': '5.131'
        }
        oauth_url = f'{self.url_for_request}?{urlencode(parameters_vk)}'
        return print (f'{oauth_url} \n Введите это URL в адресную строку браузера\n Перейдите по адресу и из полученного адреса\n из адресной строки скопируйте токен\n введите его в input_data.py' )




# Obtaining photos from VK
class VKphoto:


    def __init__(self, token_input = vktoken, user_input = user_id, base_url = 'http://api.vk.com/method/' ):
        self.token = token_input
        self.user_id = user_input
        self.base_url = base_url
        # base_url = 'http://api.vk.com/method/'
        self.parameters_photo_get = {
            'access_token': self.token,
            'v': '5.131',
            'owner_id': self.user_id,
            'photo_sizes': '1'
        }


    def get_vk_photos(self):
        response = requests.get(self.base_url + 'photos.getAll', params=self.parameters_photo_get)
        extracted_fotos = response.json()
        list_of_photos = extracted_fotos.get('response', {}).get('items')
        idx = 0
        for photo in list_of_photos:
            url_download = photo.get('sizes')[1].get('url')
            print(url_download)
            file_name = 'photo_' + str(idx) +'.jpg'
            print(file_name)
            idx += 1
            response = requests.get(url_download)
            with open(file_name, 'wb') as file:
                file.write(response.content)


# **************Yandex upload*******************

# Folder creation

class YandexFolder:

    def __init__(self, token_input = oauth_token):
        self.yand_token= token_input

    def foldercreate(self, folder_name='Netology work'):
        self.folder_name = folder_name
        folder_creation_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        parameters_folder = {
            'path': self.folder_name
        }
        headers_dict = {
            'Authorization': self.yand_token
        }
        response = requests.put(folder_creation_url, params=parameters_folder, headers=headers_dict)
        if response.status_code > 200 and response.status_code < 300:
            outcome = 'folder was created succesfully'
        elif response.status_code == 401:
            outcome = 'check authorization token'
        else:
            outcome = 'folder creation failed'
        return print(outcome)


# *******************File upload to Yandex**********************

class YandexUpload:
    url_file_upload_request = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers_dict = {
        'Authorization': oauth_token
    }

    def __init__(self):
        self

    def load_files(self):
        file_path = os.getcwd()
        files_list = os.listdir(file_path)
        photo_for_upload = list()
        for file_ in files_list:
            if file_.endswith('jpg'):
                photo_for_upload.append(file_)
        print(photo_for_upload)
        headers_dict_upload = {
            'Authorization': oauth_token,
        }
        for file_upload in tqdm(photo_for_upload, ncols=80):
            sleep(2)
            request_params = {
                'path': 'Netology work/' + file_upload
            }
            response = requests.get(self.url_file_upload_request, params=request_params, headers=self.headers_dict)
            print(response.status_code)
            url_file_upload = response.json().get('href')
            print(url_file_upload)
            with open(file_upload, 'rb') as f:
                response = requests.put(url_file_upload, files={'file': f}, headers=headers_dict_upload)
                print(response.status_code)


if __name__ == "__main__":


    # vk_url = URLGet()
    # vk_url.app_auth()

    # photo_my = VKphoto()
    #
    # photo_my.get_vk_photos()

    # netology_folder = YandexFolder()
    # netology_folder.foldercreate()
    #
    #
    loading_files = YandexUpload()
    loading_files.load_files()











