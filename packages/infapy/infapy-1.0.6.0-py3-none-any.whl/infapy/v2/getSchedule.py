import logging
import requests as re
import infapy
import json

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class GetSchedule:
    """
    This class is a handler for fetching the details of the Schedules from IICS
    """
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        self._v2 = v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
        
    def getAllSchedules(self):
        """getAllSchedule returns the details of All the Schedules

        Returns:
            List of dict: <All Schedules Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/schedule"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getAllSchedule URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the details of all the Schedules from IICS")
        data = response.json()
        return data

    def getScheduleById(self, scheduleId):
        """getScheduleById returns the details of the Schedule with the Id passed as 'scheduleId'

        Args:
            scheduleId (string): Schedule Id

        Returns:
            List of dict: <Schedule Details in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/schedule/" + scheduleId
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getScheduleById URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the details of the Schedule from IICS")
        data = response.json()
        return data

    def getScheduleByName(self, scheduleName):
        """getScheduleByName returns the details of the Schedule with the name passed as 'scheduleName'

        Args:
            scheduleName (string): Schedule Name

        Returns:
            List of dict: <Schedule Details in dict Format>
        """
        scheduleNameSpaceReplaced = scheduleName.replace(" ","%20")
        url=self._v2BaseURL + "/api/v2/schedule/name/" + scheduleNameSpaceReplaced
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getScheduleByName URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the details of the Schedule from IICS")
        data = response.json()
        return data