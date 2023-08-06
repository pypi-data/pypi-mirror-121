# Copyright (c) 2021-Present (Prashanth Pradeep)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import infapy
import requests as re
from infapy.exceptions import InvalidUserDetailsProvided

class Users:
    def __init__(self,v3,v3BaseURL,v3SessionID):
        self._v3 = v3
        self._v3BaseURL = v3BaseURL
        self._v3SessionID = v3SessionID
    
    def getAllUsers(self):
        """getAllUsers can be used to fetch all the user details in you iics org

        Returns:
            infaUserData: <list of dict>
        """
        infapy.log.info("getting all user details. Processing request....")
        url=self._v3BaseURL + "/public/core/v3/users"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}

        infapy.log.info("get users API URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")

        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the all the user details from IICS")
        data = response.json()
        infapy.log.info("getAllUsers() called successfully. Processing completed")
        return data

    def getUserByID(self,id):
        """We can use this method to get the user details of a particular user

        Args:
            id (string): you can use the user id to get the details

        Returns:
            json: infaUserDetails
        """
        infapy.log.info("getting details of user id " + str(id) + " . Processing request....")
        url=self._v3BaseURL + "/public/core/v3/users?q=userId=="+str(id)+"&limit=1&skip=0"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}

        infapy.log.info("get users API URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")

        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the user details of user id: " + id + " from IICS")
        data = response.json()
        infapy.log.info("getAllUsers() called successfully. Processing completed")
        return data

    def createNewUser(self,userProfileInJson):
        """create a new user by passing the user profile as a dict

        Args:
            userProfileInJson (dict): user profile in json

        Raises:
            InvalidUserDetailsProvided: if invalid json is provided

        Returns:
            json: confirmation of user created
        """
        infapy.log.info("Creating new user..")
        infapy.log.info("User Profile provided: " + str(userProfileInJson))

        url=self._v3BaseURL + "/public/core/v3/users"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        body = userProfileInJson

        infapy.log.info("get users API URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(userProfileInJson))

        try:
            response = re.post(url=url, json=body, headers=headers)
            data = response.json()
            infapy.log.debug(str(data))
            try:
                if ("error" in data):
                    infapy.log.error("please validate the json string and provide a valid json")
                    infapy.log.error("User Creation failed")
                    infapy.log.error(str(data))
                    raise InvalidUserDetailsProvided
            except Exception as e:
                infapy.log.exception(e)
                raise
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Created New User Successfully")
        infapy.log.info("createNewUser completed successfully..")
    
        return data

    def deleteUser(self,userID):
        """Use this function to delete a user

        Args:
            userID (str): user object id of user

        Returns:
            response code: 204 - success
        """
        infapy.log.info("Deleting user id: " + str(userID))

        url=self._v3BaseURL + "/public/core/v3/users/" + str(userID)
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}

        infapy.log.info("Delete User URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: There are no headers for this request" )

        try:
            response = re.delete(url=url, headers=headers)
            # data = response.json()
            infapy.log.debug(str(response))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Delete user successfully")
        # infapy.log.info(str(data))
        infapy.log.info("deleteUser completed successfully..")
    
        return response
