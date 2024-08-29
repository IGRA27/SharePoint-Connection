from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.sharepoint.folders.folder import Folder

# Configuración de la autenticación
site_url = 'https://empresa.sharepoint.com/sites/Server/'
ctx_auth = AuthenticationContext(site_url)

if ctx_auth.acquire_token_for_user('user', 'pwd'):
    ctx = ClientContext(site_url, ctx_auth)
    web = ctx.web
    ctx.load(web)
    ctx.execute_query()
    print("Autenticación exitosa")

    # Obtener la carpeta específica
    folder_url = "/sites/Server/SITIO CON ESPACIOS"
    target_folder = ctx.web.get_folder_by_server_relative_url(folder_url)
    ctx.load(target_folder)
    ctx.execute_query()

    # Listar todas las carpetas dentro de la carpeta objetivo
    folders = target_folder.folders
    ctx.load(folders)
    ctx.execute_query()

    print(f"Carpetas en la carpeta '{folder_url}':")
    for folder in folders:
        print(f"- {folder.properties['Name']}")
else:
    print("Error de autenticación")
