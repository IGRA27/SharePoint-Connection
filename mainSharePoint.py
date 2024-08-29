#Autor:Isaac Reyes
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.sharepoint.folders.folder import Folder
import logging
import os
import requests

# Configurar el archivo de log
logging.basicConfig(filename='logsSharePoint.txt', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def authenticate(site_url, username, password):
    ctx_auth = AuthenticationContext(site_url)
    try:
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(site_url, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            logging.info("Autenticación exitosa")
            return ctx
        else:
            logging.error("Error de autenticación: No se pudo adquirir el token.")
            return None
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Error de conexión: {e}")
        return None
    except Exception as e:
        logging.error(f"Error inesperado durante la autenticación: {e}")
        return None


def list_and_create_folder(ctx, folder_url, new_folder_name):
    try:
        # Obtener la carpeta objetivo
        target_folder = ctx.web.get_folder_by_server_relative_url(folder_url)
        ctx.load(target_folder)
        ctx.execute_query()

        # Listar carpetas existentes
        folders = target_folder.folders
        ctx.load(folders)
        ctx.execute_query()

        logging.info(f"Carpetas en la carpeta '{folder_url}':")
        folder_names = [folder.properties['Name'] for folder in folders]
        for folder_name in folder_names:
            logging.info(f"- {folder_name}")

        # Verificar si la carpeta nueva ya existe
        if new_folder_name not in folder_names:
            new_folder = target_folder.folders.add(new_folder_name)
            ctx.execute_query()
            logging.info(f"Carpeta '{new_folder_name}' creada exitosamente.")
        else:
            logging.info(f"La carpeta '{new_folder_name}' ya existe.")
            # Obtener la carpeta existente
            new_folder = ctx.web.get_folder_by_server_relative_url(f"{folder_url}/{new_folder_name}")
            ctx.load(new_folder)
            ctx.execute_query()

        return new_folder

    except Exception as e:
        logging.error(f"Error al acceder a la carpeta o listar su contenido: {e}")
        return None

def upload_file(ctx, target_folder, file_path, file_name):
    try:
        # Obtener archivos existentes en la carpeta
        files = target_folder.files
        ctx.load(files)
        ctx.execute_query()

        # Listar archivos existentes
        existing_files = [file.properties['Name'] for file in files]
        logging.info(f"Archivos en la carpeta '{target_folder.serverRelativeUrl}': {existing_files}")

        # Verificar si el archivo ya existe y ajustar el nombre si es necesario
        original_file_name = file_name
        counter = 1
        while file_name in existing_files:
            file_name = f"{os.path.splitext(original_file_name)[0]} ({counter}){os.path.splitext(original_file_name)[1]}"
            counter += 1
            logging.info(f"El archivo '{original_file_name}' ya existe. Subiendo como '{file_name}'.")

        # Subir el archivo
        with open(file_path, "rb") as file:
            file_content = file.read()
        target_folder.upload_file(file_name, file_content).execute_query()
        logging.info(f"Archivo '{file_name}' subido con éxito.")
    except Exception as e:
        logging.error(f"Error al subir el archivo: {e}")

def main():
    # Configuración de la autenticación
    site_url = 'https://empresa.sharepoint.com/sites/Sitio/SubSitio/SubSubsitio' #TENER EN CUENTA CARACTERES ESPECIALES %20 - Contenidos del sitio / PARAMETROS DE ENTRADA
    folder_url = "/sites/Sitio/Subsitio/SubSubsitio/Biblioteca de Documentos/Carpetas/Sub Carpetas" #Aqui se separa con espacios, Y PARAMETROS DE ENTRADA
    username = 'rpa.admin.sharepoint@empresa.com.ec' #El usuario debe estar como administrador de sharepoint, se puede crear con el admin de TI de la empresa un usuario especificamente para esto, asi se vera los movimientos
    password = 'Password123' #definir todo esto en un .env preferible o en el control room quemado en seco
    new_folder_name = "Nombre_Carpeta_nueva"  #Variable
    file_path = "docs/pdf.pdf"
    file_name = "pdf.pdf" #definir variables para subir.

    # Autenticación y operaciones
    ctx = authenticate(site_url, username, password)
    if ctx:
        target_folder = list_and_create_folder(ctx, folder_url, new_folder_name)
        if target_folder:
            upload_file(ctx, target_folder, file_path, file_name)

if __name__ == '__main__':
    main()
