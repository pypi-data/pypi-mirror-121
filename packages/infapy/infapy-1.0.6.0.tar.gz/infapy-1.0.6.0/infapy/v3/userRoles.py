import infapy
import requests as re
from infapy.exceptions import InvalidArgumentsError

class UserRoles:
    def __init__(self,v3, v3BaseURL, v3SessionID):
        self._v3 = v3
        self._v3BaseURL = v3BaseURL
        self._v3SessionID = v3SessionID

    def getAllUserRoles(self):
        """Method for fetching all the user roles in IICS

        Returns:
            list of dict: List of all user roles in IICS
        """
        infapy.log.info("getting all user roles. Processing request....")
        url=self._v3BaseURL + "/public/core/v3/roles"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}

        infapy.log.info("get all user roles API URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")

        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the all the user role details from IICS")
        data = response.json()
        infapy.log.info("getAllUserroles() called successfully. Processing completed")
        return data

    def getUserRoleByName(self,userRoleName):
        """Method for fetching the user role details
        by name in IICS

        Args:
            userRoleName (string): name of the userrole

        Returns:
            dict: userrole Details
        """
        
        infapy.log.info("getting the requested user role. Processing request....")
        infapy.log.info("User role Requested: " + str(userRoleName))
        url=self._v3BaseURL + "/public/core/v3/roles?q=roleName==\"" + str(userRoleName) + "\"&expand=privileges"
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
        infapy.log.info("Fetched the requested user role details from IICS")
        data = response.json()
        infapy.log.info("getUserRoleByName() called successfully. Processing completed")
        return data

    def createNewUserRole(self,name, description, privileges):
        """You can use this method to create a new user role

        Args:
            userRoleJson (dict): please read the documentation

        Raises:
            InvalidArgumentsError: if invalid args are passed

        Returns:
            dict: user role created response
        """

        infapy.log.info("Creating new user role..")


        try:
            if not (isinstance(privileges, list)):
                infapy.log.error("Privileges is not a valid list")
                infapy.log.error("Privileges: List of IDs of the privileges to assign to the role.")
                raise InvalidArgumentsError(str(privileges))
        except Exception as e:
            infapy.log.exception(e)
            raise

        userRoleJson = {
            "name":name,
            "description":description,
            "privileges":privileges
        }
        infapy.log.info("Creating User role: " + str(userRoleJson))

        
        url=self._v3BaseURL + "/public/core/v3/roles"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        body = userRoleJson

        infapy.log.info("get users API URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(userRoleJson))

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
        infapy.log.info("Created New User role created Successfully")
        infapy.log.info("createNewUserRole() completed successfully..")
    
        return data

    def deleteUserrole(self,userRoleID):
        """The function deletes the user role in informatica cloud

        Args:
            userRoleID (string): User role ID
        """
        infapy.log.info("Deleting user role with id: " + str(userRoleID))

        url=self._v3BaseURL + "/public/core/v3/roles/" + str(userRoleID)
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}

        infapy.log.info("Delete User roles URL - " + url)
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
        infapy.log.info("Deleted user roled successfully")
        # infapy.log.info(str(data))
        infapy.log.info("deleteUserrole() completed successfully..")
    
        return response

