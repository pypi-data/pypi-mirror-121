import logging
import requests as re
import infapy
import json

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class GetAgent:
    """This class is a handler for fetching
    the Agent Details from IICS
    """
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        self._v2 = v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
    

    def getAllAgentDetails(self):
        """getAllAgentDetails returns details for all Agents in the Org.

        Returns:
            List of dict: <Agent Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/agent"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getAllAgentDetails URL - " + url)
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
        infapy.log.info("Fetched Agent Details for All Agents in the Org")
        data = response.json()
        return data
    
    def getInstallerToken(self,platform):
        """getInstallerToken returns installer link depending on platform, and installer token for registering the secure agent.

        Args:
            platform (string): Operating system type. Valid values: win64 OR linux64

        Returns:
            dict: <Installer link and registration token in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/agent/installerInfo/" + platform
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getInstallerToken URL - " + url)
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
        infapy.log.info("Fetched Installer Link and Registration Token")
        data = response.json()
        return data

    def getAgentDetailsById(self,id):
        """getAgentDetailsById returns details for the Agent specified by the Id.

        Args:
            id (string): Agent Id.

        Returns:
            dict: <Agent Details in dict Format>
        """
    
        url=self._v2BaseURL + "/api/v2/agent/" + id
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getAgentDetailsById URL - " + url)
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
        infapy.log.info("Fetched Agent Details for Agent ID: " + id)
        data = response.json()
        return data

    def getAgentDetailsByName(self,name):
        """getAgentDetailsByName returns details for the Agent specified by the Name.

        Args:
            name (string): Agent Name.

        Returns:
            List of dict: <Agent Details in dict Format>
        """
    
        url=self._v2BaseURL + "/api/v2/agent/name/" + name.replace(" ","%20")
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getAgentDetailsByName URL - " + url)
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
        infapy.log.info("Fetched Agent Details for Agent Name: " + name)
        data = response.json()
        return data
    
    def getAllAgentServiceDetails(self):
        """getAllAgentServiceDetails returns details for enabled services on all Agents in the Org.

        Returns:
            List of dict: <Agent Service Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/agent/details"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getAllAgentServiceDetails URL - " + url)
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
        infapy.log.info("Fetched Agent Service Details for All Agents in the Org")
        data = response.json()
        return data

    def getAgentServiceDetailsById(self,id):
        """getAgentServiceDetailsById returns details for enabled service on the Agent specified by the Id.

        Args:
            id (string): Agent Id.

        Returns:
            dict: <Agent Service Details in dict Format>
        """
    
        url=self._v2BaseURL + "/api/v2/agent/details/" + id
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getAgentServiceDetailsById URL - " + url)
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
        infapy.log.info("Fetched Agent Service Details for Agent ID: " + id)
        data = response.json()
        return data

    def deleteAgent(self,id):
        """deleteAgent deletes Secure Agent specified by the Id, and returns response/status.

        Args:
            id (string): Agent Id.

        Returns:
            dict: <Response of Delete Request in dict Format>
        """
    
        url=self._v2BaseURL + "/api/v2/agent/" + id
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("deleteAgent URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.delete(url=url, headers=headers)
            if response.status_code==200:
                infapy.log.debug(str(response.reason))
            else:
                infapy.log.debug(str(response.json()))
            
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Delete request completed for Agent ID: " + id)
        if response.status_code==200:
            data={"Status":"Agent " + id + " has been deleted."}
        else:
            data = response.json()
        return data