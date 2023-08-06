import infapy
import requests as re
from infapy.exceptions import InvalidArgumentsError
import os

class ExportObject:
    def __init__(self,v3, v3BaseURL, v3SessionID):
        self._v3 = v3
        self._v3BaseURL = v3BaseURL
        self._v3SessionID = v3SessionID

    def startExport(self,name,ObjectId,includeDependencies=True):
        """Used to export an object in IICS
        This function initiates the export operation

        Args:
            name (String): Name of your export job
            id (String): This is the object id which you want to export
            use the lookup function or object function to get the object id

            includeDependencies (bool, optional): If you want to include dependencies. Defaults to True.

        Returns:
            json: confirmation or failure response from export operation
        """

        infapy.log.info("Exporting object with object id .." + ObjectId)
        infapy.log.info("Exporting object with object id .." + ObjectId)
        infapy.log.info(str(infapy.connect().v3().lookup(id=ObjectId)))

        if includeDependencies:
            includeDependenciesFlag = "true"
        else:
            includeDependenciesFlag = "false"

        exportJson = {
            "name": name,
            "objects" : [
                {
                    "id":ObjectId,
                    "includeDependencies":includeDependenciesFlag
                }
            ]
        }

        infapy.log.info("Exporting object: " + str(exportJson))

        
        url=self._v3BaseURL + "/public/core/v3/export"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        body = exportJson

        infapy.log.info("Export API URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(exportJson))

        try:
            response = re.post(url=url, json=body, headers=headers)
            data = response.json()
            infapy.log.debug(str(data))
            try:
                if ("error" in data):
                    infapy.log.error("please validate the json string and provide a valid json")
                    infapy.log.error("Export operation failed")
                    infapy.log.error(str(data))
                    raise InvalidArgumentsError
            except Exception as e:
                infapy.log.exception(e)
                raise
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Export initiated successfully")
        infapy.log.info("Check status of export to download the zip")
    
        return data

    def getStatusOfExportByExportID(self,exportID):
        """use this method to get the status of the export
        if it is a success or a failure

        Args:
            exportID (exportID): provide the export id you recieved
            from startExport Method used before this

        Returns:
            json: Export operation status
        """
        infapy.log.info("getStatusOfExport() Method called. Processing request....")
        
        url=self._v3BaseURL + "/public/core/v3/export/" + str(exportID) + "?expand=objects"
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
        infapy.log.info("Fetched the current export status from iics")
        data = response.json()
        infapy.log.info("getStatusOfExport() completed successfully")
        return data

    def getExportLogsByExportID(self,exportID):
        """use this method to get the export
        logs

        Args:
            exportID (exportID): provide the export id you recieved
            from startExport Method used before this

        Returns:
            string text: Export logs in text
        """
        infapy.log.info("getExportLogs Method called. Processing request....")
        
        url=self._v3BaseURL + "/public/core/v3/export/" + str(exportID) + "/log"
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
        infapy.log.info("Fetched the export logs from iics")
        data = response.text
        infapy.log.info("getExportLogs() completed successfully")
        return data

    def getExportZipFileByExportID(self,exportID,filePath=os.getcwd(),fileName="infapyExportDownloaded.zip"):
        """Use this method to download the export object as a zip file
        1. startExport()
        2. getStatusOfExportByExportID()
        3. getExportZipFileByExportID()
        4. getExportLogsByExportID()

        Args:
            exportID (String): You recieve this id when you startExport()
            filePath (String, optional): Path to download the object. Defaults to os.getcwd().
            fileName (str, optional): exportObjectName.zip. Defaults to "infapyExportDownloaded.zip".

        Returns:
            zipfile: downloaded to filepath/filename
        """
        infapy.log.info("getExportZipFileByExportID Method called. Processing request....")
        outputFile = filePath + "/" + fileName
        infapy.log.info("Downloading file to outputFile: " + outputFile) 
        url=self._v3BaseURL + "/public/core/v3/export/" + str(exportID) + "/package"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("get export log URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.get(url=url, headers=headers)
            # infapy.log.debug(str(response.text))
        except Exception as e:
            infapy.log.exception(e)
            raise
        with open(outputFile, 'wb') as f:
            f.write(response.content)
        infapy.log.info("Downloaded export zip file")
        infapy.log.info("getExportZipFileByExportID() completed successfully")