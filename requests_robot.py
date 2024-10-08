"""Automate NF PDF gathering from Belém of Pará website using Requests Library"""

# General imports
from time import time

# Automation imports 
import requests

# Web scraping imports
from bs4 import BeautifulSoup

# Project imports 
from utils.robot import Robot

class RequestsRobot(Robot):
    def __init__(self, file='data/data.json', verbose=False):
        super().__init__(file)

        self.__v = verbose

        self.base_url = 'http://siat.nota.belem.pa.gov.br:8180'
        self.validacao_url = self.base_url + '/sistematributario/jsp/validacaoNota/validacaoNota.jsf'

    def initialize_session(self):
        """Initialize requests session object"""

        if self.__v: print('[+] RequestsRobot started!\n[+] Preparing session...')

        # Start session to have a session cookie
        self.session = requests.Session()
        response = self.session.get(self.validacao_url)

        if self.__v: print('[+] Session ok!')

        # Start beautiful soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for view state hidden input
        self.viewState = soup.find('input', id='javax.faces.ViewState').get('value')
    
    def post_nf_form(self, nf_data: dict):
        """Do POST request to Belém of Pará SEFIN SIAT to download PDF"""

        if self.__v: print('[+] Posting NF form')

        # Define base request payload
        form_data = {
            'AJAXREQUEST': '_viewRoot',
            'form': 'form',
            'form:prestador': nf_data['cnpj_prestador'],
            'form:tomador': nf_data['cpf_tomador'],
            'form:j_id26': nf_data['numero_nota'],
            'form:codigoValidacao': nf_data['codigo_verificacao'],
            'javax.faces.ViewState': self.viewState,
            'form:j_id34': 'form:j_id34',
            'AJAX:EVENTS_COUNT': '1'
        }

        # Post to validate NF data
        response = self.session.post(
            self.validacao_url,
            data=form_data
        )

        if self.__v: print('[+] Requesting NF download')

        # Update payload to indicate we want to download
        form_data['form:btImprimir'] = 'form:btImprimir'
        # Post again to request download
        response = self.session.post(
            self.validacao_url,
            data=form_data
        )

        if self.__v: print('[+] Getting NF download location')

        # Start beautiful soup to read XML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get redirection location and build download URL
        location = soup.find_all('meta')[1].get('content')
        download_url = self.base_url + location

        if self.__v: print('[+] Downloading PDF')

        # Get PDF chunks
        response = self.session.get(download_url)

        # Write PDF
        with open('./data/pdfs/' + nf_data['filename'], 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        if self.__v: print(f'[+] Downloaded {nf_data["filename"]}')
        
    def execute_all(self):
        """Execute post_nf_form for all loaded data"""

        for nf in self.data:
            self.post_nf_form(nf)

if __name__ == '__main__':
    robot = RequestsRobot(verbose=True)

    ini = time()

    robot.initialize_session()
    robot.execute_all()

    fin = time()
    print(f'[+] Total time execution: {fin-ini} seconds')
