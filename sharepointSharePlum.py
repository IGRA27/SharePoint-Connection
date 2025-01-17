from shareplum import Site, Office365
from shareplum.site import Version
from requests_ntlm import HttpNtlmAuth
from dotenv import load_dotenv



import json, os

# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# config_path = '/'.join([ROOT_DIR, 'config.json'])

# read config file
# with open(config_path) as config_file:
#     config = json.load(config_file)
#     config = config['share_point']

load_dotenv()
#SHAREPOINT_URL = config['url']
SHAREPOINT_URL = os.getenv('URL')
#SHAREPOINT_SITE = config['site']
SHAREPOINT_SITE = os.getenv('SITE')
#SHAREPOINT_DOC = config['doc_library']
SHAREPOINT_DOC = '/sites/server'

class SharePoint:

    def __init__(self, usr:str, password:str):
        self.user = usr 
        self.password = password

    def auth(self):
         
        self.authcookie = Office365(SHAREPOINT_URL, username=self.user, password=self.password).GetCookies()
        

        self.site = Site(SHAREPOINT_SITE, version=Version.v365, authcookie=self.authcookie)
        return self.site
    
            
    def connect_folder(self, folder_name):
        
        self.auth_site = self.auth()

        self.sharepoint_dir = '/'.join([SHAREPOINT_DOC, folder_name])
        self.folder = self.auth_site.Folder(self.sharepoint_dir)
        return self.folder
    


    def upload_file(self, file, file_name, folder_name):
         
        self._folder = self.connect_folder(folder_name)

        with open(file, mode='rb') as file_obj:
            file_content = file_obj.read()

        self._folder.upload_file(file_content, file_name)
        

    def delete_file(self, file_name, folder_name):

        self._folder = self.connect_folder(folder_name)

        self._folder.delete_file(file_name)

    

    