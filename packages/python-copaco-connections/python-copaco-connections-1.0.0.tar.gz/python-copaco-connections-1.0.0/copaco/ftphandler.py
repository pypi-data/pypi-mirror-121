import ftplib
import os
from pathlib import Path

from .constants.errors import NotFoundError

class FTPHandler:

    def __init__(self, host, login, passwd):
        self.host = host
        self.login = login
        self.passwd = passwd

        self.ftpClient = None

        self.rootDir = Path(__file__).parent.absolute()
        self.tempDir = '{root}/temp'.format(root=self.rootDir)

    def checkClient(self):
        """ Checks if an FTP client is initialized, returns the client if found, else init new one """
        if not self.ftpClient: self.initClient()
        return self.ftpClient

    def initClient(self):
        self.ftpClient = ftplib.FTP(self.host, self.login, self.passwd)
    
    def closeClient(self):
        """ Closes FTP client if open """

        if self.ftpClient:
            self.ftpClient.quit()
            self.ftpClient = None
    
    def retrFile(self, path):
        """
        Downloads a file from a remote FTP server and saves it in the temp folder
        Opens and closes FTP connection automatically.
        
        :param path: a string pointing to the path of the file on the remote FTP server
        :return: returns the path to the local file inside the temp folder
        """

        self.checkClient()

        fileName = os.path.basename(path)
        tempPath = '{temp}/{fileName}'.format(temp=self.tempDir, fileName=fileName)

        with open(tempPath, 'wb') as tempFile:
            self.ftpClient.retrbinary('RETR ' + path, tempFile.write)
        
        self.closeClient()

        return tempPath