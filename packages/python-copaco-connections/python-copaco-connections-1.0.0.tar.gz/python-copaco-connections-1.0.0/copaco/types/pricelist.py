import datetime

from .base import ConnectionType

from copaco.utils import getFile
from copaco.constants.mappings import PRICELISTITEM_MAPPINGS, STOCK_MAPPINGS
from copaco.constants.constants import PRICELISTITEM_STATUS
from copaco.models.pricelist import PriceListItem, PriceList

class PriceListType(ConnectionType):

    def __init__(self, connection):
        super().__init__(connection)
    
    def get(self):
        """
            Retrieves the pricelist from the Copaco FTP server and creates objects for each row in the list.
            Looks at the mapping to determine which column in the file maps to which attribute on the object.
            Returns a PriceList object that contains a list of PriceListItem objects.
        """

        # 1: Retrieve the price list for the specific customer
        customerPricelistPath = '{login}/Out/CopacoBE_prijslijst_{loginNoBE}.csv'.format(login=self.connection.login, loginNoBE=self.connection.login.replace('BE', ''))
        internalPath = self.connection.ftpHandler.retrFile(customerPricelistPath)
        pdFile = getFile(internalPath)

        priceList = PriceList()
        for index, row in pdFile.iterrows():
            item = PriceListItem()

            for mAttr, mValues in PRICELISTITEM_MAPPINGS.items():

                for value in mValues:
                    if value in row: setattr(item, mAttr, row[value])
            
            if item.statusCode >= 0:
                if item.statusCode in PRICELISTITEM_STATUS:
                    item.status = PRICELISTITEM_STATUS[item.statusCode]

            priceList.add(item)

        # 2: Retrieve the stock list/details for articles and add to existing PriceListItem objects
        stockListPath = 'CopacoBE/6010_ATP.CSV'
        internalPath = self.connection.ftpHandler.retrFile(stockListPath)
        pdFile = getFile(internalPath)

        for index, row in pdFile.iterrows():
            
            articleNumber = None
            for aKey in PRICELISTITEM_MAPPINGS['article']:
                if aKey in row: articleNumber = row[aKey]
            
            if articleNumber:
                item = priceList.getItemByNumber(articleNumber)
                if item:
                    for mAttr, mValues in STOCK_MAPPINGS.items():
                        for value in mValues:
                            if value in row: setattr(item, mAttr, row[value])
                
                    item.nextDelivery = datetime.datetime.strptime(item.nextDelivery, '%m-%d-%Y').date()


        # 3: retrieve ATP status and add human-readable format to PriceListItem objects
        atpListPath = 'CopacoBE/6010_ATP_KWALIFICATIES.CSV'
        internalPath = self.connection.ftpHandler.retrFile(atpListPath)
        pdFile = getFile(internalPath)

        mappings = {}
        for index, row in pdFile.iterrows():
            mappings[row[0]] = row[1]
        
        for key, item in priceList.items.items():
            if item.inventoryStatusCode: item.inventoryStatus = mappings[item.inventoryStatusCode]

        return priceList.toList()