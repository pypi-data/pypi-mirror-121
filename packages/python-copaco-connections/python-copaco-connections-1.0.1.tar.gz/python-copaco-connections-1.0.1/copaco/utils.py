import pandas as pd
from pathlib import Path
import os
from .constants.errors import NoMethodFound, NotFoundError

def getFileExtension(path):
    """ Returns the file extension of a file, including the dot """
    return Path(path).suffix

def getHeadersAndFirstData(path):
    """
        Takes the path to a local file, returns all the headers and the first line of data

        :param path: a string pointing to the file on the local system
        :return: returns a 2D array containing the header and the first line of data 
    """

    pdFile = getFile(path)
    pdHeaders = pdFile.columns

    returnContent = []
    for header in pdHeaders:
        firstData = pdFile[header].iloc[0]
        returnContent.append([header, firstData])

    return returnContent

def getFile(path):
    """
        Takes the path to a local file (CSV, XLS) and returns a Panda File object
        Returns a NoMethodFound error if file extension is not supported

        :param path: a string pointing to the file on the local system
        :return: returns a Panda File Object if extension is supported, else NoMethodFound error
    """

    extension = getFileExtension(path)

    if extension.upper() == '.XLS':
        pdFile = pd.read_excel(path)
    elif extension.upper() == '.CSV':
        pdFile = pd.read_csv(path)
    else:
        raise NoMethodFound('No method found for this file extension. Supported extensions: XLS, CSV')
    
    return pdFile

def removeFile(path):
    """ Removes a given file from the filesystem, raises NotFoundError if file is not found """
    if os.path.exists(path):
        os.remove(path)
    else:
        raise NotFoundError('File not found.')