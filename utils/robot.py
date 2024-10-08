"""Generic robot class"""

# Project imports
from utils.handle_stuff import get_form_data, generate_filename

class Robot:

    def __init__(self, file='data/data.json'):
        self.data = get_form_data(file)

        for i,nf in enumerate(self.data):
            cnpj = nf['cnpj_prestador']
            nnf = nf['numero_nota']
            self.data[i]['filename'] = generate_filename(cnpj, nnf)

        self.__n_data = len(self.data)