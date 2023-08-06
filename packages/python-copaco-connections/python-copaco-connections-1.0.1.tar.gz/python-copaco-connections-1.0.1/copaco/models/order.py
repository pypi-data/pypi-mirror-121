from .base import BaseModel, ObjectListModel, BaseProperty

class Order(BaseModel):
    
    def __init__(self,
        external_document_id=None,
        supplier=None,
        orderheader=None,
        orderlines=None,
    ):
        super().__init__()

        self.external_document_id = external_document_id
        self.supplier = supplier
        self.orderheader = orderheader
        self.orderlines = orderlines
        self.documentsource = BaseProperty(value='order_in', type='ATTRIBUTE')

        self.attributes = ['external_document_id', 'supplier']
        self.elements = ['orderheader']
        self.lists = ['orderlines']
        self.exclude = ['orderLineCount']

        self.commonName = 'XML_order'
        self.orderLineCount = 1

    def addOrderLine(self, 
        item_id,
        tag,
        quantity,
        price=None,
        currency=None,
        deliverydate=None,
        textqualifier=None,
        text=None
    ):

        ''' Adds an orderline to the order, returns nothing '''

        item_id = ItemId().create(text=item_id, tag=tag)
        quantity = Quantity().create(text=quantity)
        if price: price = Price().create(text=price, currency=currency)
        orderlinetext = OrderLineText()

        line = OrderLine().create(orderlinetext=orderlinetext, linenumber=self.orderLineCount, item_id=item_id, quantity=quantity, price=price, deliverydate=deliverydate)
        if textqualifier and text: line.setOrderLineText(textqualifier, text)

        self.orderlines.value.add(line)
        self.orderLineCount += 1
    
    def setShippingAdress(self,
        name1,
        name2,
        street,
        postalcode,
        city,
        country
    ):
        ''' Sets the shipping adress of the order, returns nothing '''

        adress = Adress().create(name1=name1, name2=name2, street=street, postalcode=postalcode, city=city, country=country)
        shipTo = ShipTo().create(adress=adress)

        self.orderheader.value.ship_to.value = shipTo
    
    def setOrderText(self,
        textqualifier,
        text
    ):

        ordertext = OrderText().create(textqualifier=textqualifier, text=text)
        self.orderheader.value.ordertext.value = ordertext

class OrderHeader(BaseModel):

    def __init__(self,
        sender_id=None,
        customer_ordernumber=None,
        orderdate=None,
        completedelivery=None,
        requested_deliverydate=None,
        recipientsreference=None,
        customer=None,
        ship_to=None,
        ordertext=None
    ):

        super().__init__()

        self.sender_id = sender_id
        self.customer_ordernumber = customer_ordernumber
        self.orderdate = orderdate
        self.completedelivery = completedelivery
        self.requested_deliverydate = requested_deliverydate
        self.recipientsreference = recipientsreference
        self.customer = customer
        self.ship_to = ship_to
        self.ordertext = ordertext
        
        self.attributes = ['sender_id', 'customer_ordernumber', 'orderdate', 'completedelivery', 'requested_deliverydate', 'recipientsreference']
        self.elements = ['customer', 'ship_to', 'ordertext']
        self.commonName = 'orderheader'

class OrderText(BaseModel):
    
    def __init__(self,
        textqualifier=None,
        text=None
    ):

        super().__init__()

        self.textqualifier = textqualifier
        self.text = text

        self.properties = ['textqualifier', 'text']
        self.commonName = 'ordertext'

class Customer(BaseModel):

    def __init__(self,
        customerid=None
    ):

        super().__init__()
        
        self.customerid = customerid

class ShipTo(BaseModel):

    def __init__(self,
        adress=None
    ):
        super().__init__()

        self.adress = adress

        self.elements = ['adress']

class Adress(BaseModel):

    def __init__(self,
        name1=None,
        name2=None,
        street=None,
        postalcode=None,
        city=None,
        country=None
    ):
        super().__init__()

        self.name1 = name1
        self.name2 = name2
        self.street = street
        self.postalcode = postalcode
        self.city = city
        self.country = country

        self.properties = ['name1', 'name2', 'street', 'postalcode', 'city', 'country']
        self.commonName = 'adress'

class OrderLines(ObjectListModel):

    def __init__(self):
        super().__init__(list=[], listObject=OrderLine)

class OrderLine(BaseModel):

    def __init__(self,
        linenumber=None,
        item_id=None,
        quantity=None,
        deliverydate=None,
        price=None,
        orderlinetext=None
    ):
        super().__init__()

        self.linenumber = linenumber
        self.item_id = item_id
        self.quantity = quantity
        self.deliverydate = deliverydate
        self.price = price
        self.orderlinetext = orderlinetext

        self.commonName = 'orderline'
        self.elements = ['item_id', 'quantity', 'price', 'orderlinetext']
    
    def setOrderLineText(self,
        textqualifier,
        text
    ):

        orderlinetext = OrderLineText().create(textqualifier=textqualifier, text=text)
        self.orderlinetext.value = orderlinetext

class OrderLineText(BaseModel):

    def __init__(self,
        textqualifier=None,
        text=None
    ):

        super().__init__()

        self.textqualifier = textqualifier
        self.text = text

        self.commonName = 'orderlinetext'

class ItemId(BaseModel):

    def __init__(self,
        text=None,
        tag=None
    ):

        super().__init__()

        self.text = text
        self.tag = tag

        self.texts = ['text']
        self.attributes = ['tag']
        self.commonName = 'item_id'

class Quantity(BaseModel):

    def __init__(self,
        text=None,
        unit=None
    ):

        super().__init__()

        self.text = text
        self.unit = unit

        self.texts = ['text']
        self.attributes = ['unit']
        self.commonName = 'quantity'

class Price(BaseModel):

    def __init__(self,
        text=None,
        currency=None
    ):

        super().__init__()

        self.text = text
        self.currency = currency

        self.texts = ['text']
        self.attributes = ['currency']
        self.commonName = 'price'