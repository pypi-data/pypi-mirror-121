import logging
import requests as re
import infapy
import json

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class Schedule:
    """This class is a handler for fetching
    the Schedule Details from IICS and executing other V3 Schedule APIs
    """
    def __init__(self,v3,v3BaseURL,v3SessionID):
        self._v3 = v3
        self._v3BaseURL = v3BaseURL
        self._v3SessionID = v3SessionID


    def getAllSchedules(self):
        """getAllSchedules returns details for all Schedules in the Org.

        Returns:
            List of dict: <Schedule Details in dict Format>
        """
        url=self._v3BaseURL + "/public/core/v3/schedule"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("getAllSchedules URL - " + url)
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
        infapy.log.info("Fetched Details for All Schedules in the Org")
        data = response.json()
        return data

    def getScheduleById(self,id):
        """getScheduleById returns details for the schedule as specified by the Id.

        Args:
            id (string): Schedule Id.

        Returns:
            dict: <Schedule Details in dict Format>
        """

        url=self._v3BaseURL + "/public/core/v3/schedule/" + id
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("getScheduleById URL - " + url)
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
        infapy.log.info("Fetched Details for Schedule " + id )
        data = response.json()
        return data

    def getSchedulesWithQuery(self,query):
        """getScheduleWithQuery returns details for the schedules as specified by the filter query provided.

        Args:
            query (string): Filter Query to filter out Schedules.

        Returns:
            list of dict: <Schedule Details in dict Format>
        """

        url=self._v3BaseURL + "/public/core/v3/schedule?q=" + query
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("getScheduleWithQuery URL - " + url)
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
        infapy.log.info("Fetched Details for Schedules using the Query: " + query )
        data = response.json()
        return data

    def createSchedule(self,body):
        """createSchedule creates a Schedule based on the information provided in the Body. For configuration of body, please refer to: 
            https://docs.informatica.com/integration-cloud/cloud-platform/current-version/rest-api-reference/platform-rest-api-version-3-resources/schedule.html

        Args:
            body (dict): JSON body for POST request.

        Returns:
            dict: <Status of Create Schedule Request in dict Format>
        """
        url=self._v3BaseURL + "/public/core/v3/schedule"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("createSchedule URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(body))
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.post(url=url, json=body, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Created Schedule with Given Specifications in the Org")
        data = response.json()
        return data

    def updateSchedule(self,body,id):
        """updateSchedule updates a Schedule with specified Id based on the information provided in the Body. For configuration of body, please refer to: 
            https://docs.informatica.com/integration-cloud/cloud-platform/current-version/rest-api-reference/platform-rest-api-version-3-resources/schedule.html

        Args:
            body (dict): JSON body for POST request.
            id (string): Schedule Id.

        Returns:
            dict: <Status of Update Schedule Request in dict Format>
        """

        url=self._v3BaseURL + "/public/core/v3/schedule/" + id
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("updateSchedule URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(body))
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.patch(url=url, json=body, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Update Schedule " + id + "with Given Specifications in the Org")
        data = response.json()
        return data

    def deleteSchedule(self,id):
        """deleteSchedule deletes Schedule as specified by the Id.

        Args:
            id (string): Schedule Id.

        Returns:
            dict: <Status of Delete Schedule Request in dict Format>
        """

        url=self._v3BaseURL + "/public/core/v3/schedule/" + id
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("deleteSchedule URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.delete(url=url, headers=headers)
            if response.status_code==204:
                infapy.log.debug(str(response.reason))
            else:
                infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Schedule " + id + "has been deleted")
        if response.status_code==204:
            data={"Status":"Schedule " + id + " has been deleted."}
        else:
            data = response.json()
        return data    