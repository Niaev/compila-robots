"""Handle stuff"""

# General imports
import json

def clean_code(code: str) -> str:
    """Remove dots, hifens and slashes from codes"""
    return code.replace('.', '').replace('/', '').replace('-', '')

def generate_filename(cnpj: str, nnf: str) -> str:
    """Create a file name containing CNPJ and NF number"""
    clean_cnpj = clean_code(cnpj)
    return f'{clean_cnpj}_{nnf}.pdf'

def get_form_data(file='data/data.json') -> list:
    """Get data from data/data.json"""
    with open(file, 'r') as f:
        data = json.load(f)
    
    return data