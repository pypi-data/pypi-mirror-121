import infapy
import requests as re
from infapy.exceptions import InvalidArgumentsError
import os

class ImportObject:
    def __init__(self,v3, v3BaseURL, v3SessionID):
        self._v3 = v3
        self._v3BaseURL = v3BaseURL
        self._v3SessionID = v3SessionID

    def uploadZipToGetJobID(self,filePath=os.getcwd(),fileName="infapyExportDownloaded.zip"):
        

        infapy.log.info("Importing the objects")
        zipFile = filePath + "\\" + fileName
        fileObj = None
        try:
            with open(zipFile,'rb') as zipFileBin:
                fileObj=zipFileBin
        except Exception as e:
            infapy.log.exception(e)
            raise
        
        try:
            if fileObj is None:
                infapy.log.error("zip file not found")
                raise InvalidArgumentsError(zipFile)
        except Exception as e:
            infapy.log.exception(e)
            raise

        infapy.log.info("Read is successful")
        infapy.log.info("Read file: " + zipFile)

        infapy.log.info("Importing object ....")

        
        url=self._v3BaseURL + "/public/core/v3/import/package"
        headers = {'Content-Type': "multipart/form-data","INFA-SESSION-ID":self._v3SessionID}

        infapy.log.info("Import API URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        
        try:
            
            header = {"INFA-SESSION-ID":self._v3SessionID}
            files = {'package': (fileName, open(zipFile, 'rb'),'application/zip')}
            # print(files)
            response = re.post(url, headers=header, files=files)
            # print(response)
            data = response.json()
            try:
                if ("error" in data):
                    infapy.log.error("please validate the form data and provide a valid form data")
                    infapy.log.error("Import operation failed")
                    infapy.log.error(str(data))
                    raise InvalidArgumentsError
            except Exception as e:
                infapy.log.exception(e)
                raise
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Job ID: " + data["jobId"])
        infapy.log.info("Import initiated successfully")
        return data

    def startImportByJobID(self,jobID,importBody):

        infapy.log.info("Starting the import job...")
        infapy.log.info("import job id: " + jobID )

        url=self._v3BaseURL + "/public/core/v3/import/" + jobID
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        body = importBody 

        infapy.log.info("import API URL is:  - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(importBody))

        try:
            response = re.post(url=url, json=body, headers=headers)
            data = response.json()
            infapy.log.debug(str(data))
            try:
                if ("error" in data):
                    infapy.log.error("please validate the json string and provide a valid json")
                    infapy.log.error("User Creation failed")
                    infapy.log.error(str(data))
                    raise InvalidArgumentsError
            except Exception as e:
                infapy.log.exception(e)
                raise
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Import operation has been initiated successfully")
        infapy.log.info("startImportByJobID() has been initiated successfully..!!")
    
        return data


    def getStatusOfImportByImportID(self,importID):
        """use this method to get the status of the import
        if it is a success or a failure

        Args:
            importID (importID): provide the import id you recieved
            from uploadZipToGetJobID Method used before this

        Returns:
            json: import operation status
        """
        infapy.log.info("getStatusOfImportByImportID() Method called. Processing request....")
        
        url=self._v3BaseURL + "/public/core/v3/import/" + str(importID) + "?expand=objects"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("get status of export URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the current import status from iics")
        data = response.json()
        infapy.log.info("getStatusOfImportByImportID() completed successfully")
        return data

    def getImportLogsByImportID(self,importID):
        """use this method to get the import
        logs

        Args:
            importID (importID): provide the import id you recieved
            from uploadZipToGetJobID Method used before this

        Returns:
            string text: import logs in text
        """
        infapy.log.info("getImportLogsByImportID() Method called. Processing request....")
        
        url=self._v3BaseURL + "/public/core/v3/import/" + str(importID) + "/log"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("get export log URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.text))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the import logs from iics")
        data = response.text
        infapy.log.info("getImportLogsByImportID() completed successfully")
        return data

