"""Module for elements handling"""

# Web crawling imports
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException

class JustFind(object):
    """Search for an specific element

    This class just returns an HTML element if it is found, by the 
    given identifiers, when it is called. In case of failure, it 
    returns False.
    
    Instance Variables:
    params {list} -- Containing, respectively, the element 
                     identification string and a secondary parameter
                     string
    """

    def __init__(self,params):
        self.el = params[0]
        self.pa = params[1]
    
    def __call__(self,b):
        if self.pa:
            p = b.find_element(by=By.ID, value=self.pa)
            e = p.find_element(by=By.ID, value=self.el)
        else: e = b.find_element(by=By.ID, value=self.el)
        if e: return e
        return False

class Click(object):
    """Try to click a given object

    When the class is called, it tries to click the given object five
    times in maximum before failing completely or succeding in any of the
    tryings.

    Instance Variables:
    el {selenium.WebElement} -- A clickable HTML element
    """

    def __init__(self,el):
        self.el = el
    
    def __call__(self,b):
        tries = 5
        while tries:
            try: 
                btn = b.find_element(by=By.CSS_SELECTOR, value=self.el)
                btn.click()
            except ElementClickInterceptedException as e:
                tries = tries - 1
            else:
                return True
        return False