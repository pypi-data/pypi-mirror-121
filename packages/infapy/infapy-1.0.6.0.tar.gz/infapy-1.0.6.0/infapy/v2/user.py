import logging
import requests as re
import infapy
import json
from infapy.exceptions import InvalidDetailsProvided

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class User:
    """
    This class is a handler for fetching the details of the Users from IICS
    """
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        self._v2 = v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
        
    def getAllUsers(self):
        """getAllUsers returns the details of All the Users

        Returns:
            List of dict: <All Users Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/user"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getAllUsers URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the details of all the Users from IICS")
        data = response.json()
        return data

    def getUserById(self, userId):
        """getUserById returns the details of the User with the Id passed as 'userId'

        Args:
            userId (string): User Id

        Returns:
            List of dict: <User Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/user/" + userId
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getUserById URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the details of the User from IICS")
        data = response.json()
        return data

    def getUserByName(self, userName):
        """getUserByName returns the details of the User with the name passed as 'userName'

        Args:
            userName (string): User Name

        Returns:
            List of dict: <User Details in dict Format>
        """
        userNameSpaceReplaced = userName.replace(" ","%20")
        url=self._v2BaseURL + "/api/v2/user/name/" + userNameSpaceReplaced
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getUserByName URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the details of the User from IICS")
        data = response.json()
        return data

    def updateUserDetails(self, userId, userDetailsInJson):
        """The function updateUserDetails can be used to update the details of an IICS User

        Args:
            userId (steing): User Id
            userDetailsInJson (dict): User details in json format 

        Raises:
            InvalidDetailsProvided: [description]

        Returns:
            List of dict: <Updated User Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/user/" + userId
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        body = userDetailsInJson
        infapy.log.info("updateUserDetails URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(userDetailsInJson))
        try:
            response = re.post(url=url, json=body, headers=headers)
            data = response.json()
            infapy.log.debug(str(data))
            try:
                if ("error" in data):
                    infapy.log.error("Please validate the json string and provide a valid json")
                    infapy.log.error("User Details update failed")
                    infapy.log.error(str(data))
                    raise InvalidDetailsProvided
            except Exception as e:
                infapy.log.exception(e)
                raise
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Updated the User Details from IICS")
        data = response.json()
        return data
    
    def deleteUser(self, userId):
        """The function deleteUser is used to delete the update with id 'userId'

        Args:
            userId (string): User Id

        Returns:
            code: API Response Code
        """
        url=self._v2BaseURL + "/api/v2/user/" + userId
        headers = {"icSessionID":self._v2icSessionID}
        infapy.log.info("deleteUser URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.delete(url=url, headers=headers)
            infapy.log.debug("API Response Code " + str(response.status_code))
            infapy.log.debug(str(response.json))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("User with id " + userId + " deleted")
        code = response.status_code
        return code