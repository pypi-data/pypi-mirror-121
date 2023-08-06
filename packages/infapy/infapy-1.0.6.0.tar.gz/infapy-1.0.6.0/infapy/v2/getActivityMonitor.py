import logging
import requests as re
import infapy
import json

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class GetActivityMonitor:
    """This class is a handler for fetching
    the Activity Monitor from IICS
    """
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        self._v2 = v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
    

    def getActivityMonitorLog(self,details="false"):
        """getActivityMonitorLog returns activity logs for running jobs in IICS.

        Args:
            details (str, optional): Returns log information for tasks, linear taskflows, and child objects if set to true. Defaults to "false", since it is IICS default.

        Returns:
            List of dict: <Activity Monitor Log in dict Format>
        """
        
        url=self._v2BaseURL + "/api/v2/activity/activityMonitor?details=" + details
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getActivityMonitorLog URL - " + url)
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
        infapy.log.info("Fetched Activity Logs for All Running Jobs")
        data = response.json()
        return data