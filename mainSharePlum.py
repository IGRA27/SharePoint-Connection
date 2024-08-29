import logging 
logging.basicConfig(filename="log.txt", level = logging.DEBUG,
                        format="%(asctime)s %(message)s")
import requests
import datetime
import bs4 as bs
import os
import json
import schedule
import time
from sharepointSharePlum import SHAREPOINT_SITE, SHAREPOINT_URL, SharePoint
from datetime import date
from shareplum import Office365
from dotenv import load_dotenv

load_dotenv()
FIDUCIA_USER = os.getenv('USER')
PASSWD = os.getenv('PASSWD')

def get_petro_link():
    """ Obtiene el link del pdf. """
    link = "https://www.eppetroecuador.ec/?p=3721"
    try: 
        data = requests.get(link).content
        soup = bs.BeautifulSoup(data, "html.parser")
        pdf_link = soup.find('a', string='Sumario de Operaciones').get('href')
        logging.info("Se encontró el link de descarga.")
        return pdf_link
    except:
        logging.info("El link de descarga no se encontró en el scraping.")
        return None

def get_summary(text)->None:
    """Descarga el sumario de operaciones de Petroecuador"""
    link = get_petro_link()
    data = requests.get(link).content
    with open('docs/sumario.pdf', 'wb') as file:
        file.write(data)

def upload_to_sharepoint(text):
    """Sube el archivo descargado a SharePoint"""
    file_name = f"{str(date.today().day-1).zfill(2)}-{str(date.today().day).zfill(2)}_Resumen{str(date.today().year)}{str(date.today().month).zfill(2)}.pdf"
    path_to_file = 'docs/sumario.pdf'

    try: 
        sp = SharePoint(FIDUCIA_USER, PASSWD)
        sp.upload_file(path_to_file, file_name, str(date.today().year) + "/" + str(date.today().month))
        logging.info('Login Exitoso.')
        logging.info(f"Documento {str(date.today().year)}/{str(date.today().month)}/{file_name} subido a SharePoint.")
    except FileNotFoundError as e:
        logging.error(f'Proceso terminado, credenciales no válidas, error: {e}')
    except Exception as e:
        logging.error(f"El documento no se ha subido a SharePoint: {e}")

def main():
    # Programar tareas
    schedule.every().day.at("09:38:10").do(get_summary, "")
    schedule.every().day.at("09:38:15").do(upload_to_sharepoint, "")

    # Bucle para correr las tareas
    while True:
        schedule.run_pending()
        time.sleep(1)  # Esperar un segundo

if __name__ == '__main__':
    main()

 
    
    
   




