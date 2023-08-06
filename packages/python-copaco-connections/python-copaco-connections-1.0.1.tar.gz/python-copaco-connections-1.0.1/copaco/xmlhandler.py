from pathlib import Path
import xml.etree.ElementTree as ET

class XMLHandler:

    def __init__(self):

        self.rootDir = Path(__file__).parent.absolute()
        self.tempDir = '{root}/temp'.format(root=self.rootDir)

    
    def getRoot(self, filePath):
        """ Takes the path to an XML file and returns an ElementTree object """

        path = '{root}/{filePath}'.format(root=self.rootDir, filePath=filePath)
        return ET.parse(path).getroot()
    

    def parseJSON(self, json):
        """ Takes the JSON representation of an object and converts it to XML, returns an ElementTree object """

        # We can only have one root element, which is the first key in the dictionary
        firstKey = next(iter(json))
        parentElement = ET.Element(firstKey)

        for k1, v1 in json[firstKey].items():

            if v1['type'] == 'ATTRIBUTE':
                parentElement.set(k1, v1['value'])
            elif v1['type'] == 'PROPERTY':
                ET.SubElement(parentElement, k1).text = v1['value']
            elif v1['type'] == 'ELEMENT':
                element = self.parseJSON(v1['values'])
                parentElement.append(element)
            elif v1['type'] == 'LIST':
                for v in v1['values']:
                    element = self.parseJSON(v)
                    parentElement.append(element)
            elif v1['type'] == 'TEXT':
                parentElement.text = v1['value']
        
        return parentElement
    
    def writeToFile(self, filename, xml):
        """ 
            Takes a filename and an ElementTree object, writes the XML to the specified file inside the temp folder 
            Returns the path to the created file

            :param filename: the filename to be used, including extension
            :param xml: the ElementTree object that will be used to generate the file
            :return: the path to the created XML file
        """
        
        path = '{tempDir}/{filename}'.format(tempDir=self.tempDir, filename=filename)
        tree = ET.ElementTree(xml)
        tree.write(path)

        return path