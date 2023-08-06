import infapy
import requests as re
from infapy.exceptions import InvalidArgumentsError

class UserGroups:
    def __init__(self,v3, v3BaseURL, v3SessionID):
        self._v3 = v3
        self._v3BaseURL = v3BaseURL
        self._v3SessionID = v3SessionID

    def getAllUserGroups(self):
        """Method for fetching all the user groups in IICS

        Returns:
            list of dict: List of all user groups in IICS
        """
        infapy.log.info("getting all user groups. Processing request....")
        url=self._v3BaseURL + "/public/core/v3/userGroups"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}

        infapy.log.info("get all user groups API URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")

        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the all the user group details from IICS")
        data = response.json()
        infapy.log.info("getAllUserGroups() called successfully. Processing completed")
        return data

    def getUserGroupByName(self,userGroupName):
        """Method for fetching the user group details
        by name in IICS

        Args:
            userGroupName (string): name of the usergroup

        Returns:
            dict: userGroup Details
        """
        
        infapy.log.info("getting the requested user group. Processing request....")
        infapy.log.info("User Group Requested: " + str(userGroupName))
        url=self._v3BaseURL + "/public/core/v3/userGroups?q=userGroupName==" + str(userGroupName)
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}

        infapy.log.info("Requested user API URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")

        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the requesteduser group details from IICS")
        data = response.json()
        infapy.log.info("getUserGroupByName() called successfully. Processing completed")
        return data

    def createNewUserGroup(self,userGroupJson):
        """You can use this method to create a new user group

        Args:
            userGroupJson (dict): please read the documentation

        Raises:
            InvalidArgumentsError: if invalid args are passed

        Returns:
            dict: user group created response
        """
        infapy.log.info("Creating new user group..")
        infapy.log.info("Creating User Group: " + str(userGroupJson))

        url=self._v3BaseURL + "/public/core/v3/userGroups"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        body = userGroupJson

        infapy.log.info("get users API URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(userGroupJson))

        try:
            response = re.post(url=url, json=body, headers=headers)
            data = response.json()
            infapy.log.debug(str(data))
            try:
                if ("error" in data):
                    infapy.log.error("please validate the json string and provide a valid json")
                    infapy.log.error("User Creation failed")
                    infapy.log.error(str(data))
                    raise InvalidArgumentsError(str(userGroupJson))
            except Exception as e:
                infapy.log.exception(e)
                raise
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Created New User Group created Successfully")
        infapy.log.info("createNewUserGroup completed successfully..")
    
        return data

    def deleteUserGroup(self,userGroupID):
        """The function deletes the user group in informatica cloud

        Args:
            userGroupID (string): User Group ID
        """
        infapy.log.info("Deleting user group with id: " + str(userGroupID))

        url=self._v3BaseURL + "/public/core/v3/userGroups/" + str(userGroupID)
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}

        infapy.log.info("Delete User Groups URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: There is no body for this request" )

        try:
            response = re.delete(url=url, headers=headers)
            # data = response.json()
            infapy.log.debug(str(response))
            # raise
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Deleted user groupd successfully")
        # infapy.log.info(str(data))
        infapy.log.info("deleteUserGroup() completed successfully..")
    
        return response

