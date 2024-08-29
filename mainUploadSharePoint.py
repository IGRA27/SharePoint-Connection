from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.sharepoint.folders.folder import Folder
from office365.sharepoint.lists.list import List

#Configuración de la autenticación
#Es importante poner caracteres especiales
site_url = 'https://EMPRESA.sharepoint.com/sites/Server/Quito/Caracteresespecialestenercuent%C3%B3a'

ctx_auth = AuthenticationContext(site_url)
if ctx_auth.acquire_token_for_user('rpa.admin.sharepoint@empresa.com.io', 'passworddelusuario123'):
    ctx = ClientContext(site_url, ctx_auth)
    web = ctx.web
    ctx.load(web)
    ctx.execute_query()
    print("Autenticación exitosa")

    #Subir archivo
    file_path = "docs/sumario.pdf"
    with open(file_path, "rb") as file:
        file_content = file.read()
    folder_url = "/sites/Server/Quito/SitioCarpetaNormal/CarpetasConEspacios Nada mas/"
    target_folder = ctx.web.get_folder_by_server_relative_url(folder_url)
    target_file = target_folder.upload_file("sumario.pdf", file_content).execute_query()
    print("Archivo subido con éxito")
else:
    print("Error de autenticación")
