from .ftphandler import FTPHandler
from .types.pricelist import PriceListType

class CopacoConnectionBE:

    def __init__(self, host, login, passwd):

        self.host = host
        self.login = login
        self.passwd = passwd

        self.ftpHandler = FTPHandler(self.host, self.login, self.passwd)
        self.priceList = PriceListType(self)