import logging
import requests as re
import infapy
import json

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class GetRuntimeEnvironment:
    """
    This class is a handler for fetching the details of the Runtime Environments from IICS
    """
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        self._v2 = v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
        
    def getAllRuntimeEnvironments(self):
        """getAllRuntimeEnvironments returns the details of All the Runtime Environments

        Returns:
            List of dict: <All Runtime Environment Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/runtimeEnvironment"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("GetAllRuntimeEnvironments URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the details of all the Runtime Environments from IICS")
        data = response.json()
        return data

    def getRuntimeEnvironmentById(self, runEnvId):
        """getRuntimeEnvironmentById returns the details of the Runtime Environment with the Id passed as 'runEnvId'

        Args:
            runEnvId (string): Runtime Environment Id

        Returns:
            List of dict: <Runtime Environment Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/runtimeEnvironment/" + runEnvId
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getRuntimeEnvironmentById URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the details of the Runtime Environment from IICS")
        data = response.json()
        return data

    def getRuntimeEnvironmentByName(self, runEnvName):
        """getRuntimeEnvironmentById returns the details of the Runtime Environment with the name passed as 'runEnvName'

        Args:
            runEnvName (string): Runtime Environment Name

        Returns:
            List of dict: <Runtime Environment Details in dict Format>
        """
        runEnvNameSpaceReplaced = runEnvName.replace(" ","%20")
        url=self._v2BaseURL + "/api/v2/runtimeEnvironment/name/" + runEnvNameSpaceReplaced
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getRuntimeEnvironmentByName URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the details of the Runtime Environment from IICS")
        data = response.json()
        return data