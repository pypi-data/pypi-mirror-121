import datetime

from .base import BaseResponse
from copaco.constants.mappings import RESP_ATP_MAPPINGS, RESP_CODE_MAPPINGS

# INT
class OrderResponse(BaseResponse):
    
    def __init__(self,
        supplier=None,
        customer=None,
        customer_ordernumber=None,
        external_document_id=None,
        sequencenumber=None,
        document_source=None,
        responsecode=None,
        ordernumber=None
    ):

        self.supplier = supplier
        self.customer = customer
        self.customer_ordernumber = customer_ordernumber
        self.external_document_id = external_document_id
        self.sequencenumber = sequencenumber
        self.document_source = document_source
        self.responsecode = responsecode
        self.ordernumber = ordernumber

        self.beingProcessed = False
        self.error = None
    
    def parseJSON(self, json):
        self = super().parseJSON(json)

        if self.responsecode == '0':
            self.beingProcessed = True
        else:
            self.error = RESP_CODE_MAPPINGS[self.responsecode]
        
        return self

# OBV
class OrderConfirmation(BaseResponse):

    def __init__(self,
        documentsource=None,
        external_document_id=None,
        supplier=None,
        document_date=None,
        orderheader=None,
        Customer=None,
        ShipTo=None,
        VAT=None,
        costs=None,
        orderline=None,
        ordertrailer=None
    ):

        self.documentsource = documentsource
        self.external_document_id = external_document_id
        self.supplier = supplier
        self.document_date = document_date
        self.orderheader = orderheader if orderheader else OrderHeader()
        self.Customer = Customer if Customer else CustomerObj()
        self.ShipTo = ShipTo if ShipTo else ShipToObj()
        self.VAT = VAT if VAT else []
        self.costs = costs if costs else []
        self.orderline = orderline if orderline else []
        self.ordertrailer = ordertrailer if ordertrailer else OrderTrailer()

    def parseJSON(self, json):
        self = super().parseJSON(json)
        self.document_date = datetime.datetime.strptime(self.document_date, '%d-%M-%Y').date()
        return self    

class VATObj(BaseResponse):

    def __init__(self,
        percentage=None,
        amount=None,
        currency=None
    ):

        self.percentage = percentage
        self.amount = amount
        self.currency = currency

class Costs(BaseResponse):

    def __init__(self,
        sign=None,
        code=None,
        description=None,
        amount=None,
        currency=None,
        costsVAT=None
    ):

        self.sign = sign
        self.code = code
        self.description = description
        self.amount = amount
        self.currency = currency
        self.costsVAT = costsVAT if costsVAT else []

class CostsVAT(BaseResponse):

    def __init__(self,
        VATpercentage=None,
        VATcode=None,
        VatAmount=None,
        VatBase=None    
    ):

        self.VATpercentage = VATpercentage
        self.VATcode = VATcode
        self.VatAmount = VatAmount
        self.VatBase = VatBase

class OrderHeader(BaseResponse):

    def __init__(self,
        customer_ordernumber=None,
        order_number=None,
        sequencenumber=None,
        status=None,
        testflag=None,
        orderdate=None,
        completedelivery=None,
        currency=None,
        terms_of_payment_text=None,
        incoterms_text=None,
        recipientsreference=None,
    ):

        self.customer_ordernumber = customer_ordernumber
        self.order_number = order_number
        self.sequencenumber = sequencenumber
        self.status = status
        self.testflag = testflag
        self.orderdate = orderdate
        self.completedelivery = completedelivery
        self.currency = currency
        self.terms_of_payment_text = terms_of_payment_text
        self.incoterms_text = incoterms_text
        self.recipientsreference = recipientsreference
    
    def parseJSON(self, json):
        self = super().parseJSON(json)
        self.orderdate = datetime.datetime.strptime(self.orderdate, '%d-%M-%Y').date()
        return self  

class CustomerObj(BaseResponse):

    def __init__(self,
        customer_id=None,
        customercontact=None
    ):

        self.customer_id = customer_id
        self.customercontact = customercontact if customercontact else CustomerContact()

class OrderLine(BaseResponse):

    def __init__(self,
        linenumber=None,
        customer_linenumber=None,
        item_id=None,
        item_description=None,
        manufacturer_item_id=None,
        first_requested_deliverydate=None,
        price=None,
        line_amount=None,
        currency=None,
        quantity_ordered=None,
        schedulelines=None
    ):

        self.linenumber = linenumber
        self.customer_linenumber = customer_linenumber
        self.item_id = item_id
        self.item_description = item_description
        self.manufacturer_item_id = manufacturer_item_id
        self.first_requested_deliverydate = first_requested_deliverydate
        self.price = price
        self.line_amount = line_amount
        self.currency = currency
        self.quantity_ordered = quantity_ordered
        self.schedulelines = schedulelines if schedulelines else ScheduleLines()

class ScheduleLines(BaseResponse):

    def __init__(self,
        quantity=None,
        atp_code=None,
        atp_date=None
    ):

        self.quantity = quantity
        self.atp_code = atp_code
        self.atp_date = atp_date
        self.atp_readable = None
    
    def parseJSON(self, json):
        self = super().parseJSON(json)
        self.atp_readable = RESP_ATP_MAPPINGS[self.atp_code]
        self.atp_date = datetime.datetime.strptime(self.atp_date, '%Y%M%d').date()
        return self


class OrderTrailer(BaseResponse):

    def __init__(self,
        order_amount_ex_VAT=None,
        order_VAT_amount=None,
        order_amount_incl_VAT=None
    ):

        self.order_amount_ex_VAT = order_amount_ex_VAT
        self.order_VAT_amount = order_VAT_amount
        self.order_amount_incl_VAT = order_amount_incl_VAT

class CustomerContact(BaseResponse):

    def __init__(self,
        email=None,
        telephone=None,
        fax=None
    ):

        self.email = email
        self.telephone = telephone
        self.fax = fax

class ShipToObj(BaseResponse):

     def __init__(self,
        name1=None,
        name2=None,
        name3=None,
        name4=None,
        street=None,
        postalcode=None,
        city=None,
        country=None
    ):

        self.name1 = name1
        self.name2 = name2
        self.name3 = name3
        self.name4 = name4
        self.street = street
        self.postalcode = postalcode
        self.city = city
        self.country = country

# FAC
class Invoice(BaseResponse):

    def __init__(self,
        invoiceheader=None,
        InvoiceSender=None,
        BillTo=None,
        invoicecustomer=None,
        InvoicePayer=None,
        invoiceline=None,
        invoicetrailer=None
    ):

        self.invoiceheader = invoiceheader if invoiceheader else InvoiceHeader()
        self.InvoiceSender = InvoiceSender if InvoiceSender else InvoiceSenderObj()
        self.BillTo = BillTo if BillTo else BillToObj()
        self.invoicecustomer = invoicecustomer if invoicecustomer else InvoiceCustomer()
        self.InvoicePayer = InvoicePayer if InvoicePayer else InvoicePayerObj()
        self.invoiceline = invoiceline if invoiceline else []
        self.invoicetrailer = invoicetrailer if invoicetrailer else InvoiceTrailer()

class InvoiceHeader(BaseResponse):

    def __init__(self,
        documentsource=None,
        invoice_type=None,
        supplier=None,
        document_date=None,
        supplier_vat_number=None,
        koers=None,
        TermsOfPaymentCoded=None,
        TermsOfPaymentDays=None,
        TermsOfPaymentPercentage=None,
        invoice_number=None,
        invoice_date=None,
        invoice_expiration_date=None,
        invoice_currency=None,
        invoice_terms_of_payment_text=None,
        invoice_terms_of_delivery=None
    ):

        self.documentsource = documentsource
        self.invoice_type = invoice_type
        self.supplier = supplier
        self.document_date = document_date
        self.supplier_vat_number = supplier_vat_number
        self.koers = koers
        self.TermsOfPaymentCoded = TermsOfPaymentCoded
        self.TermsOfPaymentDays = TermsOfPaymentDays
        self.TermsOfPaymentPercentage = TermsOfPaymentPercentage
        self.invoice_number = invoice_number
        self.invoice_date = invoice_date
        self.invoice_expiration_date = invoice_expiration_date
        self.invoice_currency = invoice_currency
        self.invoice_terms_of_payment_text = invoice_terms_of_payment_text
        self.invoice_terms_of_delivery = invoice_terms_of_delivery


    def parseJSON(self, json):
        self = super().parseJSON(json)
        self.document_date = datetime.datetime.strptime(self.document_date, '%Y%M%d').date()
        self.invoice_date = datetime.datetime.strptime(self.invoice_date, '%Y%M%d').date()
        self.invoice_expiration_date = datetime.datetime.strptime(self.invoice_expiration_date, '%Y%M%d').date()
        return self
    
class InvoiceSenderObj(BaseResponse):

    def __init__(self,
        name=None,
        address=None,
        postalcode=None,
        city=None,
        PObox=None,
        Postalcode_PObox=None,
        city_PObox=None,
        country=None,
        Telephone=None,
        Fax=None,
        BankAccount=None,
        IBAN=None,
        BIC=None,
        VATnumber=None,
        Website=None,
        ChamberOfCommerce=None,
        Swift=None
    ):

        self.name = name
        self.address = address
        self.postalcode = postalcode
        self.city = city
        self.PObox = PObox
        self.Postalcode_PObox = Postalcode_PObox
        self.city_PObox = city_PObox
        self.country = country
        self.Telephone = Telephone
        self.Fax = Fax
        self.BankAccount = BankAccount
        self.IBAN = IBAN
        self.BIC = BIC
        self.VATnumber = VATnumber
        self.Website = Website
        self.ChamberOfCommerce = ChamberOfCommerce
        self.Swift = Swift

class BillToObj(BaseResponse):

    def __init__(self,
        BillToNumber=None,
        BillToName=None,
        BillToName2=None,
        BillToName3=None,
        BillToName4=None,
        BillToStreet=None,
        BillToZip_city=None,
        BillToPobox=None,
        BillToPo_city=None,
        BillTocontact=None,
        BillToVat_number=None,
        BillToCountry=None,
        BillToCountryName=None
    ):


        self.BillToNumber = BillToNumber
        self.BillToName = BillToName
        self.BillToName2 = BillToName2
        self.BillToName3 = BillToName3
        self.BillToName4 = BillToName4
        self.BillToStreet = BillToStreet
        self.BillToZip_city = BillToZip_city
        self.BillToPobox = BillToPobox
        self.BillToPo_city = BillToPo_city
        self.BillTocontact = BillTocontact
        self.BillToVat_number = BillToVat_number
        self.BillToCountry = BillToCountry
        self.BillToCountryName = BillToCountryName

class InvoiceCustomer(BaseResponse):

    def __init__(self,
        customer_id=None,
        customer_name1=None,
        customer_name2=None,
        customer_name3=None,
        customer_name4=None,
        customer_street=None,
        customer_zip_city=None,
        customer_pobox=None,
        customer_country=None,
        customercontact=None,
        customer_vat_number=None,
        customer_countryname=None
    ):

        self.customer_id = customer_id
        self.customer_name1 = customer_name1
        self.customer_name2 = customer_name2
        self.customer_name3 = customer_name3
        self.customer_name4 = customer_name4
        self.customer_street = customer_street
        self.customer_zip_city = customer_zip_city
        self.customer_pobox = customer_pobox
        self.customer_country = customer_country
        self.customercontact = customercontact
        self.customer_vat_number = customer_vat_number
        self.customer_countryname = customer_countryname

class InvoicePayerObj(BaseResponse):

    def __init__(self,
        addresscode=None,
        name1=None,
        name2=None,
        name3=None,
        name4=None,
        street=None,
        postalcode=None,
        city=None,
        country=None
    ):

        self.addresscode = addresscode
        self.name1 = name1
        self.name2 = name2
        self.name3 = name3
        self.name4 = name4
        self.street = street
        self.postalcode = postalcode
        self.city = city
        self.country = country

class InvoiceLine(BaseResponse):

    def __init__(self,
        invoicelinenumber=None,
        part_of_linenumber=None,
        invoiceorder=None,
        customerorder=None,
        invoice_item=None
    ):

        self.invoicelinenumber = invoicelinenumber
        self.part_of_linenumber = part_of_linenumber
        self.invoiceorder = invoiceorder if invoiceorder else InvoiceOrder()
        self.customerorder = customerorder if customerorder else CustomerOrder()
        self.invoice_item = invoice_item if invoice_item else InvoiceItem()

class InvoiceOrder(BaseResponse):

    def __init__(self,
        ordernumber=None,
        ShipTo=None,
        linenumber=None,
        orderdate=None,
        dispatchnumber=None,
        dispatchlinenumber=None,
        dispatchdate=None
    ):

        self.ordernumber = ordernumber
        self.ShipTo = ShipTo if ShipTo else ShipToObj()
        self.linenumber = linenumber
        self.orderdate = orderdate
        self.dispatchnumber = dispatchnumber
        self.dispatchlinenumber = dispatchlinenumber
        self.dispatchdate = dispatchdate

    def parseJSON(self, json):
        self = super().parseJSON(json)
        self.orderdate = datetime.datetime.strptime(self.orderdate, '%Y%M%d').date()
        self.dispatchdate = datetime.datetime.strptime(self.dispatchdate, '%Y%M%d').date()
        return self

class CustomerOrder(BaseResponse):
     
     def __init__(self,
        recipientsreference=None,
        customer_ordernumber=None,
        customer_linenumber=None,
        document_id=None
     ):

        self.recipientsreference = recipientsreference
        self.customer_ordernumber = customer_ordernumber
        self.customer_linenumber = customer_linenumber
        self.document_id = document_id

class InvoiceItem(BaseResponse):

    def __init__(self,
        item_id=None,
        customer_item_id=None,
        manufacturer_item_id=None,
        quantity_ordered=None,
        item_description=None,
        price=None,
        discount_percentage=None,
        net_price=None,
        quantity_invoiced=None,
        line_amount=None,
        item_vat=None,
        item_costs=None,
        serialnumbers=None
    ):


        self.item_id = item_id
        self.customer_item_id = customer_item_id
        self.manufacturer_item_id = manufacturer_item_id
        self.quantity_ordered = quantity_ordered
        self.item_description = item_description
        self.price = price
        self.discount_percentage = discount_percentage
        self.net_price = net_price
        self.quantity_invoiced = quantity_invoiced
        self.line_amount = line_amount
        self.item_vat = item_vat if item_vat else []
        self.item_costs = item_costs if item_costs else []
        self.serialnumbers = serialnumbers if serialnumbers else SerialNumbers()

class ItemVAT(BaseResponse):

    def __init__(self,
        percentage=None,
        amount=None,
        vatcode=None,
        vatbase=None
    ):

        self.percentage = percentage
        self.amount = amount
        self.vatcode = vatcode
        self.vatbase = vatbase

class ItemCosts(BaseResponse):

    def __init__(self,
        ItemCostSign=None,
        ItemCostCode=None,
        ItemCostDescription=None,
        ItemCostPrice=None,
        ItemCostAmount=None,
        ItemCostQuantity=None,
        ItemCostVATPercentage=None,
        ItemCostVATcode=None,
        ItemCostVATamount=None,
        ItemCostVatBase=None
    ):

        self.ItemCostSign = ItemCostSign
        self.ItemCostCode = ItemCostCode
        self.ItemCostDescription = ItemCostDescription
        self.ItemCostPrice = ItemCostPrice
        self.ItemCostAmount = ItemCostAmount
        self.ItemCostQuantity = ItemCostQuantity
        self.ItemCostVATPercentage = ItemCostVATPercentage
        self.ItemCostVATcode = ItemCostVATcode
        self.ItemCostVATamount = ItemCostVATamount
        self.ItemCostVatBase = ItemCostVatBase

class SerialNumbers(BaseResponse):

    def __init__(self,
        serialnumber=None
    ):

        self.serialnumber = serialnumber

class InvoiceTrailer(BaseResponse):

    def __init__(self,
        costs=None,
        invoice_amount_ex_VAT=None,
        invoice_VAT_amount=None,
        invoice_amount_incl_VAT=None,
        COD_amount=None,
        VATS=None
    ):

        self.costs = costs if costs else []
        self.invoice_amount_ex_VAT = invoice_amount_ex_VAT
        self.invoice_VAT_amount = invoice_VAT_amount
        self.invoice_amount_incl_VAT = invoice_amount_incl_VAT
        self.COD_amount = COD_amount
        self.VATS = VATS if VATS else VATSObj()

class VATSObj(BaseResponse):

    def __init__(self,
        TotalVAT=None
    ):

        self.TotalVAT = TotalVAT if TotalVAT else TotalVATObj()

class TotalVATObj(BaseResponse):

    def __init__(self,
        percentage=None,
        amount=None,
        vatcode=None,
        vatbase=None
    ):

        self.percentage = percentage
        self.amount = amount
        self.vatcode = vatcode
        self.vatbase = vatbase


# PAK
class DispatchAdvice(BaseResponse):

    def __init__(self,
        route=None,
        dispatchheader=None,
        Customer=None,
        ShipTo=None,
        dispatchline=None,
        dispatchtrailer=None
    ):

        self.route = route
        self.dispatchheader = dispatchheader if dispatchheader else DispatchHeader()
        self.Customer = Customer if Customer else CustomerObj()
        self.ShipTo = ShipTo if ShipTo else ShipToObj()
        self.dispatchline = dispatchline if dispatchline else []
        self.dispatchtrailer = dispatchtrailer if dispatchtrailer else DispatchTrailer()

class DispatchHeader(BaseResponse):

    def __init__(self,
        supplier=None,
        dispatchnumber=None,
        dispatchdate=None
    ):

        self.supplier = supplier
        self.dispatchnumber = dispatchnumber
        self.dispatchdate = dispatchdate

    def parseJSON(self, json):
        self = super().parseJSON(json)
        self.dispatchdate = datetime.datetime.strptime(self.dispatchdate, '%Y%M%d').date()
        return self

class DispatchLine(BaseResponse):

    def __init__(self,
        dispatchlinenumber=None,
        item=None,
        serial_numbers=None,
        tracking_numbers=None,
        order=None,
        customerorder=None
    ):

        self.dispatchlinenumber = dispatchlinenumber
        self.item = item if item else Item()
        self.serial_numbers = serial_numbers if serial_numbers else SerialNumbers()
        self.tracking_numbers = tracking_numbers if tracking_numbers else []
        self.order = order if order else Order()
        self.customerorder = customerorder if customerorder else CustomerOrder()

class Item(BaseResponse):

    def __init__(self,
        item_id=None,
        customer_item_id=None,
        manufacturer_item_id=None,
        quantity=None,
        item_description=None
    ):

        self.item_id = item_id
        self.customer_item_id = customer_item_id
        self.manufacturer_item_id = manufacturer_item_id
        self.quantity = quantity
        self.item_description = item_description

class TrackingNumbers(BaseResponse):

    def __init__(self,
        tracking_carrier=None,
        tracking_number=None
    ):

        self.tracking_carrier = tracking_carrier
        self.tracking_number = tracking_number

class Order(BaseResponse):

    def __init__(self,
        ordernumber=None,
        linenumber=None,
        orderdate=None
    ):

        self.ordernumber = ordernumber
        self.linenumber = linenumber
        self.orderdate = orderdate

    def parseJSON(self, json):
        self = super().parseJSON(json)
        self.orderdate = datetime.datetime.strptime(self.orderdate, '%Y%M%d').date()
        return self

class DispatchTrailer(BaseResponse):

    def __init__(self,
        total_number_of_units=None
    ):

        self.total_number_of_units = total_number_of_units