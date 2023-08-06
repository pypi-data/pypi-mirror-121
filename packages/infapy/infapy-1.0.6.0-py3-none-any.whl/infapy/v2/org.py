import logging
import requests as re
import infapy
import json
from infapy.exceptions import InvalidDetailsProvided

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class Org:
    """
    This class is a handler for fetching the Org and Sub-org Details from IICS
    """
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        self._v2 = v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
        
    def getOrgDetails(self):
        """getOrgDetails returns the details of the IICS Organization

        Returns:
            List of dict: <Organization Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/org"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("GetOrgDetails URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the Organization Details from IICS")
        data = response.json()
        return data

    def getSubOrgDetailsById(self, subId):
        """getSubOrgDetailsById returns the details of the Sub Organization with the Id passed as 'subId'

        Args:
            subId (string): Sub Organization Id

        Returns:
            List of dict: <Sub Organization Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/org/" + subId
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("GetSubOrgDetailsById URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the Sub Organization Details from IICS")
        data = response.json()
        return data

    def getSubOrgDetailsByName(self, subName):
        """getSubOrgDetailsByName returns the details of the Sub Organization with the name passed as 'subName'

        Args:
            subName (string): Sub Organization Name

        Returns:
            List of dict: <Sub Organization Details in dict Format>
        """
        subNameSpaceReplaced = subName.replace(" ","%20")
        url=self._v2BaseURL + "/api/v2/org/name/" + subNameSpaceReplaced
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("GetSubOrgDetailsByName URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the Sub Organization Details from IICS")
        data = response.json()
        return data
    
    def updateSubOrgDetails(self, suborgId, subOrgDetailsInJson):
        """The function updateSubOrgDetails can be used to update the details of a Sub-org

        Args:
            suborgId (steing): Sub Org Id
            subOrgDetailsInJson (dict): Sub-Org details in json format 

        Raises:
            InvalidDetailsProvided: [description]

        Returns:
            List of dict: <Updated Sub Org Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/org/" + suborgId
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        body = subOrgDetailsInJson
        infapy.log.info("updateSubOrgDetails URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(subOrgDetailsInJson))
        try:
            response = re.post(url=url, json=body, headers=headers)
            data = response.json()
            infapy.log.debug(str(data))
            try:
                if ("error" in data):
                    infapy.log.error("Please validate the json string and provide a valid json")
                    infapy.log.error("Org Details update failed")
                    infapy.log.error(str(data))
                    raise InvalidDetailsProvided
            except Exception as e:
                infapy.log.exception(e)
                raise
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Updated the Sub Organization Details from IICS")
        data = response.json()
        return data

    def registerSubOrg(self, subOrgRegInfoInJson):
        """The function registerSubOrg can be used register a new sub org

        Args:
            subOrgRegInfoInJson (dict): Details for Sub-org Registeration in json format 

        Raises:
            InvalidDetailsProvided: [description]

        Returns:
            List of dict: <Sub Org Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/user/register"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        body = subOrgRegInfoInJson
        infapy.log.info("registerSubOrg URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(subOrgRegInfoInJson))
        try:
            response = re.post(url=url, json=body, headers=headers)
            data = response.json()
            infapy.log.debug(str(data))
            try:
                if ("error" in data):
                    infapy.log.error("Please validate the json string and provide a valid json")
                    infapy.log.error("Sub Org creation failed")
                    infapy.log.error(str(data))
                    raise InvalidDetailsProvided
            except Exception as e:
                infapy.log.exception(e)
                raise
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Sub Org created successfully")
        data = response.json()
        return data