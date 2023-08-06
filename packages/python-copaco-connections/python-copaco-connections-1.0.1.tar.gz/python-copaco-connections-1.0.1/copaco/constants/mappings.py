PRICELISTITEM_MAPPINGS = {
    'article' : ['Artikel', 'Copaco artikelnummer'],
    'vendorCode' : ['Fabrikantscode'],
    'description' : ['Omschrijving'],
    'price' : ['Prijs'],
    'priceWithLevies' : ['Prijs_incl_heffingen'],
    'stock' : ['Voorraad'],
    'hierarchy' : ['produktindeling'],
    'unspscCode' : ['UNSPSC_code'],
    'EAN' : ['EAN_code'],
    'statusCode' : ['status'],
    'auvibel' : ['Auvibel'],
    'reprobel' : ['Reprobel'],
    'recupel' : ['Recupel'],
    'bebat' : ['Bebat']
}

STOCK_MAPPINGS = {
    'nextDelivery' : ['Copaco datum eerstvolgende ontvangst'],
    'nextDeliveryAmount' : ['Copaco aantal eerstvolgende ontvangst'],
    'inventoryStatusCode' : ['Copaco ATP kwalificaties']
}

RESP_ATP_MAPPINGS = {
    '010' : 'Already sent',
    '030': 'At expedition',
    '050' : 'At ICT Services',
    '090' : 'Cancelled',
    '100' : 'Appointed stock',
    '200' : 'Confirmed',
    '300' : 'Expected supplier',
    '400' : 'Expected',
    '500' : 'Unknown delivery',
    '600' : 'Indication',
    '700' : 'Out of stock',
    '800' : 'Not available yet'
}

RESP_CODE_MAPPINGS = {
    '0' : 'Being processed',
    '1' : 'The order contains an error. Copaco will take further actions to correct the order.',
    '2' : 'The order contains an error. Copaco will take further actions to correct the order.',
    '98' : 'Order not processed. An order with the same customer order number is already present.',
    'X' : 'Order rejected. Sender-ID is not correct'
}