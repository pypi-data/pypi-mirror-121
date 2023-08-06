import importlib
from typing_extensions import OrderedDict

#==============[HELPER FUNCTIONS]=================#
def getIndexWithValue(list, attribute, value):

    for index, obj in enumerate(list):
        if hasattr(obj, attribute):
            if getattr(obj, attribute) == value:
                return index
    
    return None

def getObjectWithValue(list, attribute, value):

    for index, obj in enumerate(list):
        if hasattr(obj, attribute):
            if getattr(obj, attribute) == value:
                return obj
    
    return None

def formatKey(key):
    key = key.replace('@', '')
    key = key.replace('-', '')
    return key

#==============[BASE MODELS]=================#

class BaseResponse:

    def parseJSON(self, json):
        import copaco.models.responses as responses
        CLASS_MAPPINGS = { 
            'VAT' : responses.VATObj,
            'costs' : responses.Costs,
            'orderline' : responses.OrderLine,
            'item_vat' : responses.ItemVAT,
            'item_costs' : responses.ItemCosts,
            'serialnumbers' : responses.SerialNumbers,
            'serial_numbers' : responses.SerialNumbers,
            'invoiceline' : responses.InvoiceLine,
            'costsVAT' : responses.CostsVAT,
            'tracking_numbers' : responses.TrackingNumbers,
            'dispatchline' : responses.DispatchLine
        }

        for key, value in json.items():
            key = formatKey(key)
            attrVal = getattr(self, key)

            if isinstance(attrVal, BaseResponse):
                setattr(self, key, attrVal.parseJSON(value))
            elif isinstance(attrVal, list):
                classObj = CLASS_MAPPINGS[key]
                if isinstance(value, list):
                    for v in value:
                        attrVal.append(classObj().parseJSON(v))
                else:
                    attrVal.append(classObj().parseJSON(value))
            else:
                if isinstance(value, OrderedDict):
                    value = value['#text']
                setattr(self, key, value)
        
        return self

class BaseModel:
    
    def __init__(self):

        self.hasError = False
        self.error = None

        self.attributes = []
        self.properties = []
        self.elements = []
        self.texts = []
        self.lists = []
        self.exclude = []

        self.commonName = str(type(self).__name__)
    
    def getJSON(self):
        """ Converts the object to a JSON representation, which can be used as input for the parseJSON function of the xmlHandler """

        dikt = {}
        for k, v in self.__dict__.items():

            # Skip the default properties
            if (k in ['attributes', 'properties', 'elements', 'hasError', 'error', 'commonName', 'texts', 'lists', 'exclude']) or (k in self.exclude): continue

            if v:
                if isinstance(v, BaseModel):
                    json = v.getJSON()
                    if json: dikt[k] = json
                else:
                    dikt[k] = v

        topLevel = { self.commonName : dikt }

        return topLevel

    def create(self, **kwargs):

        for key, value in kwargs.items():
            if value is None: continue

            type = 'PROPERTY'
            if key in self.attributes: type = 'ATTRIBUTE'
            elif key in self.texts: type = 'TEXT'
            elif key in self.elements: type = 'ELEMENT'
            elif key in self.lists: type = 'LIST'

            obj = BaseProperty(value=value, type=type)
            setattr(self, key, obj)

        return self


class BaseProperty(BaseModel):

    def __init__(self, value=None, type=None):

        self.value = value
        self.type = type
    
    def getJSON(self):
        """ Converts the object to a JSON representation, which can be used as input for the parseJSON function of the xmlHandler """

        if (self.type == 'ATTRIBUTE') or (self.type ==  'PROPERTY') or (self.type == 'TEXT'):
            return { 'value' : str(self.value), 'type' : self.type }
        
        if (self.type == 'ELEMENT'):
            if len(self.value.getJSON()[self.value.commonName]) > 0:
                return {'value' : type(self.value).__name__, 'type' : self.type, 'values' : self.value.getJSON() }
        
        if (self.type == 'LIST'):
            if len(self.value.items()) > 0:
                return {'value' : type(self.value).__name__, 'type' : self.type, 'values' : self.value.getJSON() }


class ObjectListModel(BaseModel):

    def __init__(self, list=[], listObject=None):
        super().__init__()

        self.list = list
        self.listObject = listObject
        self.hasError = False
        self.error = None
    
    def add(self, item):
        self.list.append(item)
        return self.list
    
    def remove(self, item):
        self.list.remove(item)
        return self.list
    
    def getJSON(self):
        list = []

        for item in self.list:
            list.append(item.getJSON())
        
        return list if len(list) > 0 else None

    def items(self):
        return self.list