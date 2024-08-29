from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

# Configuración de la autenticación
site_url = 'https://empresa.sharepoint.com/sites/Server'
ctx_auth = AuthenticationContext(site_url)

if ctx_auth.acquire_token_for_user('user', 'pwd'):
    ctx = ClientContext(site_url, ctx_auth)
    web = ctx.web
    ctx.load(web)
    ctx.execute_query()
    print("Autenticación exitosa")

    # Intentar acceder al subsitio 'Quito'
    try:
        subsitio_url = '/sites/Server/'
        ctx = ClientContext(f'{site_url}/Quito/', ctx_auth)
        web = ctx.web
        ctx.load(web)
        ctx.execute_query()
        print("Acceso al subsitio 'Quito/' exitoso")

        # Obtener todas las carpetas en la biblioteca 'FID ADMIN'
        library_url = 'Quito/'
        library = ctx.web.get_folder_by_server_relative_url(library_url)
        ctx.load(library)
        ctx.execute_query()

        folders = library.folders
        ctx.load(folders)
        ctx.execute_query()

        print("Carpetas en la biblioteca 'FID ADMIN':")
        if len(folders) == 0:
            print("No se encontraron carpetas en la biblioteca 'FID ADMIN'.")
        for folder in folders:
            print(folder.properties["Name"])

    except Exception as e:
        print(f"Error al acceder al subsitio o biblioteca: {e}")

else:
    print("Error de autenticación")
