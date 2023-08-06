from .base import BaseModel

class PriceList(BaseModel):

    def __init__(self,
        items=None
    ):
        self.items = items if items else {}
    
    def add(self, item):
        self.items[item.article] = item
    
    def toList(self):
        return list(self.items.values())
    
    def getItemByNumber(self, code):
        if code in self.items:
            return self.items[code]
        return None

class PriceListItem(BaseModel):
    
    def __init__(self,
        article=None,
        vendorCode=None,
        description=None,
        price=None,
        priceWithLevies=None,
        stock=None,
        hierarchy=None,
        unspscCode=None,
        EAN=None,
        statusCode=None,
        status=None,
        auvibel=None,
        reprobel=None,
        recupel=None,
        bebat=None,
        nextDelivery=None,
        nextDeliveryAmount=None,
        inventoryStatusCode=None,
        inventoryStatus=None
    ):
        super().__init__()

        self.article = article
        self.vendorCode = vendorCode
        self.description = description
        self.price = price
        self.priceWithLevies = priceWithLevies
        self.stock = stock
        self.hierarchy = hierarchy
        self.unspscCode = unspscCode
        self.EAN = EAN
        self.statusCode = statusCode
        self.status = status
        self.auvibel = auvibel
        self.reprobel = reprobel
        self.recupel = recupel
        self.bebat = bebat
        self.nextDelivery = nextDelivery
        self.nextDeliveryAmount = nextDeliveryAmount
        self.inventoryStatusCode = inventoryStatusCode
        self.inventoryStatus = inventoryStatus