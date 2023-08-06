import datetime
import requests
import xmltodict
from typing_extensions import OrderedDict

from .xmlhandler import XMLHandler
from .models.order import *
from .models.responses import *
from .constants.errors import FailedRequest
from .utils import removeFile

class CopacoOrders:

    def __init__(self, customerId, senderId):

        self.senderId = senderId
        self.customerId = customerId
        self.method = 'HTTP'
        self.xmlHandler = XMLHandler()

        self.testRequestUrl = 'https://connect.copaco.com/xmlorder-test'
        self.requestUrl = 'https://connect.copaco.com/xmlorder'

        self.testResponseUrl = 'http://connect.copaco.com/xmlresponses-test'
        self.responseUrl = 'http://connect.copaco.com/xmlresponses'
    
    def create(self,
        external_document_id,
        supplier,
        customer_ordernumber,
        completedelivery,
        requested_deliverydate=None,
        recipientsreference=None,
    ):
        ''' Simplified create function to create a basic Order object, returns an Order object '''

        today = datetime.datetime.today().strftime('%d-%m-%Y')
        customer = Customer().create(customerid=self.customerId)
        ship_to = ShipTo()
        ordertext = OrderText()
        header = OrderHeader().create(ship_to=ship_to, ordertext=ordertext, requested_deliverydate=requested_deliverydate, recipientsreference=recipientsreference, sender_id=self.senderId, orderdate=today, customer_ordernumber=customer_ordernumber, customer=customer, completedelivery=completedelivery)
        orderlines = OrderLines()
        
        order = Order().create(
            external_document_id=external_document_id,
            supplier=supplier,
            orderheader=header,
            orderlines=orderlines,
        )

        return order
    
    def sendToCopaco(self, order):
        ''' 
            Takes an Order object, generates XML file and sends the file to Copaco
            Deletes the file in the temp folder afterwards to save space
            Returns True if HTTP 200 is received, raises FailedRequest with response content otherwise
        '''
        
        json = order.getJSON()
        xml = self.xmlHandler.parseJSON(json)

        filePath = self.xmlHandler.writeToFile('test.xml', xml)
        with open(filePath, 'rb') as f: data = f.read()
        removeFile(filePath)

        response = requests.post(self.testRequestUrl, data=data)
        if response.status_code == 200: return True
        else: raise FailedRequest(response.content)
    

    def getResponses(self, distributor='6010', type='ALL'):
        '''
            Retrieves the responses from Copaco and parses the given XML

            :param distributor: the distributor code (6010 = Copaco BE, COPACO = Copaco NL). Default is Copaco BE.
            :param type: the type of response to fetch (INT, OBV, FAC, PAK). Default is ALL.
            :return: an array of all the responses if type is ALL, array of a specified type if type is not ALL
        '''

        respTypes = {
            'orderresponse' : {
                'list' : [],
                'object' : OrderResponse,
            },
            'orderconfirmation' : {
                'list' : [],
                'object' : OrderConfirmation,
            },
            'invoice' : {
                'list' : [],
                'object' : Invoice,
            },
            'dispatchadvice' : {
                'list' : [],
                'object' : DispatchAdvice,
            }
        }

        url = '{respUrl}/?distributor_id={distributor}&customer_id={customer_id}&sender_id={sender_id}&type={type}'.format(respUrl=self.testResponseUrl, distributor=distributor, customer_id=self.customerId, sender_id=self.senderId, type=type)
        
        response = requests.get(url)
        if response.status_code == 200: data = response.content
        else: raise FailedRequest(response.content)

        # The line below is for testing, should be deleted/commented in production
        # with open('responses/pak-dispatchadvice.xml', 'r') as f: data = f.read() 

        dikt = xmltodict.parse(data)
        orderresponses = dikt['orderresponses']

        for key, value in respTypes.items():
            list = value['list']
            object = value['object']
            responses = orderresponses[key] if key in orderresponses else None

            if responses:
                if isinstance(responses, OrderedDict): responses = [responses]

                for resp in responses:
                    obj = object().parseJSON(resp)
                    list.append(obj)

        return {
            'INT' : respTypes['orderresponse']['list'],
            'OBV' : respTypes['orderconfirmation']['list'],
            'FAC' : respTypes['invoice']['list'],
            'PAK' : respTypes['dispatchadvice']['list'],
            'ALL' : {
                'INT' : respTypes['orderresponse']['list'], 
                'OBV' : respTypes['orderconfirmation']['list'],
                'FAC' : respTypes['invoice']['list'],
                'PAK' : respTypes['dispatchadvice']['list']
            }
        }[type]