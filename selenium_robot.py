"""Automate NF PDF gathering from Belém of Pará website using Selenium"""

# General imports
import os
import glob
from time import sleep, time

# Automation imports 
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

# Project imports 
from utils.elements import JustFind
from utils.robot import Robot

class SeleniumRobot(Robot):
    def __init__(self, file='data/data.json', verbose=False, headless=True):
        super().__init__(file)

        self.__v = verbose
        self.__headless = headless

    def initialize_browser(self):
        """Initialize webdrizer Firefox browser"""

        if self.__v: print('[+] SeleniumRobot started!\n[+] Preparing webdriver...')

        # Configure browser options
        options = Options()
        options.set_preference("browser.cache.disk.enable", False)
        options.set_preference("browser.cache.memory.enable", False)
        options.set_preference("browser.cache.offline.enable", False)
        options.set_preference("network.http.use-cache", False)
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", os.getcwd() + "\data\pdfs")
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        if self.__headless:
            options.add_argument('--headless')

        # Point browser engine (Firefox geckodriver)
        service = Service('data/geckodriver.exe')

        # Instanciate web driver
        proceed = False
        while not proceed:
            try:
                b = Firefox(options=options, service=service)
            except WebDriverException as e:
                pass
            else:
                proceed = True
        b.delete_all_cookies()

        if self.__v: print('[+] Webdriver ok!')

        self.driver = b

    def submit_nf_form(self, nf_data: dict):
        """Enter Belém of Pará SEFIN SIAT to fill, submit the form and download NF"""

        # Access
        url = 'http://siat.nota.belem.pa.gov.br:8180/sistematributario/jsp/validacaoNota/validacaoNota.jsf'
        if self.__v: print('[+] Opening Belém PA SEFIN SIAT')
        self.driver.get(url)

        # Get form fields
        prestador_input = self.driver.find_element(by=By.ID, value='form:prestador')
        tomador_input = self.driver.find_element(by=By.ID, value='form:tomador')
        nnf_input = self.driver.find_element(by=By.NAME, value='form:j_id26')
        codver_input = self.driver.find_element(by=By.ID, value='form:codigoValidacao')
        submit_btn = self.driver.find_element(by=By.ID, value='form:j_id34')

        # Fill form fields
        prestador_input.send_keys(nf_data['cnpj_prestador'])
        tomador_input.send_keys(nf_data['cpf_tomador'])
        nnf_input.send_keys(nf_data['numero_nota'])
        codver_input.send_keys(nf_data['codigo_verificacao'])
        if self.__v: print('[+] Form filled up')

        # Click 'Verificar Nota' button
        submit_btn.click()
        if self.__v: print('[+] Submit button clicked')

        # Wait for print button to appear
        try: 
            WebDriverWait(self.driver, 30).until(JustFind(('form:btImprimir', '')))
        except Exception as e:
            raise e

            # In case of any error with the authentication
            if self.__v: print('[-] Print button did not appear 30 seconds after submission\n[-] Aborting...')
            return
        
        # Get and click print button to download
        print_btn = self.driver.find_element(by=By.ID, value='form:btImprimir')
        print_btn.click()
        if self.__v: print('[+] Print button clicked')

        if self.__v: print('[+] Waiting two seconds...')
        sleep(2)

        # Rename PDF
        self.rename_filename(nf_data)
        if self.__v: print(f'[+] File renamed\n[+] Downloaded {nf_data["filename"]}')

    def rename_filename(self, nf_data: dict):
        """Rename last downloaded PDF"""

        # Get last saved file path
        list_of_files = glob.glob('./data/pdfs/*.pdf')
        latest_file_path = max(list_of_files, key=os.path.getctime)

        # New path name
        filename = './data/pdfs/' + nf_data['filename']
        try:
            os.rename(latest_file_path, filename)
        except FileExistsError:
            os.remove(filename)
            os.rename(latest_file_path, filename)
        
    def execute_all(self):
        """Execute submit_nf_form for all loaded data"""

        for nf in self.data:
            self.submit_nf_form(nf)

if __name__ == '__main__':
    robot = SeleniumRobot(verbose=True, headless=False)

    ini = time()

    try:
        robot.initialize_browser()
        robot.execute_all()
    finally:
        robot.driver.quit()

    fin = time()
    print(f'[+] Total time execution: {fin-ini} seconds')