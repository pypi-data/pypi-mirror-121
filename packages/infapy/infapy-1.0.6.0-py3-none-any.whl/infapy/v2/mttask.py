import logging
import requests as re
import infapy
import json

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class MTTask:
    """This class is a handler for running IICS mttask APIs
    """
    def __init__(self,cdi,cdiBaseURL,cdiSessionID):
        self._cdi=cdi
        self._cdiSessionID = cdiSessionID
        self._cdiBaseURL = cdiBaseURL

    def getAllMTTasks(self):
        """getAllMTTasks returns details for all Mapping tasks in the Org.

        Returns:
            List of dict: <Mapping Task Details in dict Format>
        """
        url=self._cdiBaseURL + "/api/v2/mttask"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionId":self._cdiSessionID}
        infapy.log.info("getAllMTTasks URL - " + url)
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
        infapy.log.info("Fetched List of All Mapping Tasks in the Org")
        data = response.json()
        return data

    def getMTTaskById(self,id):
        """getMTTaskById returns details for the Mapping Task specified by the Id.

        Args:
            id (string): Mapping Task Id.

        Returns:
            dict: <Mapping Task Details in dict Format>
        """
        url=self._cdiBaseURL + "/api/v2/mttask/" + id
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionId":self._cdiSessionID}
        infapy.log.info("getMTTaskById URL - " + url)
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
        infapy.log.info("Fetched Details of Mapping Task with Id: " + id)
        data = response.json()
        return data

    def getMTTaskByName(self,name):
        """getMTTaskByName returns details for the Mapping Task specified by the Name.

        Args:
            name (string): Mapping Task Name.

        Returns:
            dict: <Mapping Task Details in dict Format>
        """
        url=self._cdiBaseURL + "/api/v2/mttask/name/" + name.replace(" ","%20")
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionId":self._cdiSessionID}
        infapy.log.info("getMTTaskByName URL - " + url)
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
        infapy.log.info("Fetched Details of Mapping Task with Name: " + name)
        data = response.json()
        return data   

    def createMTTask(self,body):
        """createMTTask creates a Mapping Task based on the information provided in the Body. For configuration of body, please refer to: 
            https://docs.informatica.com/integration-cloud/cloud-platform/current-version/rest-api-reference/data-integration-rest-api/mttask.html

        Args:
            body (dict): JSON body for POST request.

        Returns:
            dict: <Details of Create Mapping Task Request in dict Format>
        """
        url=self._cdiBaseURL + "/api/v2/mttask/"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionId":self._cdiSessionID}
        infapy.log.info("createMTTask URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(body))
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.post(url=url, headers=headers, json=body)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Mapping Task Create Request Complete")
        data = response.json()
        return data 

    def updateMTTaskFull(self,body,id):
        """updateMTTaskFull updates an existing Mapping Task with specified ID based on the information provided in the Body, with Partial Mode Disabled. For configuration of body, please refer to: 
            https://docs.informatica.com/integration-cloud/cloud-platform/current-version/rest-api-reference/data-integration-rest-api/mttask.html

        Args:
            body (dict): JSON body for POST request.

        Returns:
            dict: <Details of Update Mapping Task Request in dict Format>
        """
        url=self._cdiBaseURL + "/api/v2/mttask/" + id
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionId":self._cdiSessionID}
        infapy.log.info("updateMTTaskFull URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(body))
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.post(url=url, headers=headers, json=body)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Mapping Task Full Update Request Complete")
        data = response.json()
        return data

    def updateMTTaskPartial(self,body,id):
        """updateMTTaskPartial updates an existing Mapping Task with specified ID based on the information provided in the Body, with Partial Mode Enabled. For configuration of body, please refer to: 
            https://docs.informatica.com/integration-cloud/cloud-platform/current-version/rest-api-reference/data-integration-rest-api/mttask.html

        Args:
            body (dict): JSON body for POST request.

        Returns:
            dict: <Details of Partial Update Mapping Task Request in dict Format>
        """
        url=self._cdiBaseURL + "/api/v2/mttask/" + id
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionId":self._cdiSessionID, "Update-Mode": "PARTIAL"}
        infapy.log.info("updateMTTaskPartial URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(body))
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.post(url=url, headers=headers, json=body)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Mapping Task Partial Update Request Complete")
        data = response.json()
        return data

    def deleteMTTask(self,id):
        """getMTTaskById deletes the Mapping Task specified by the Id.

        Args:
            id (string): Mapping Task Id.

        Returns:
            dict: <Details of Delete Mapping Task Request in dict Format>
        """

        url=self._cdiBaseURL + "/api/v2/mttask/" + id
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionId":self._cdiSessionID}
        infapy.log.info("deleteMTTask URL - " + url)
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
        infapy.log.info("Mapping Task " + id + " has been deleted")
        if response.status_code==200:
            data={"Status":"Mapping Task " + id + " has been deleted."}
        else:
            data = response.json()
        return data   