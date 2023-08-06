import logging
import requests as re
import infapy
import json

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class TaskList:
    """This class is a handler for fetching
    the Task List from IICS
    """
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        self._v2 = v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID

    
    def getTaskListByType(self,type):
        """getTaskListByType returns list of tasks from IICS based on the task type specified.

        Args:
            type (string): Type of tasks. List of valid values available at https://docs.informatica.com/integration-cloud/cloud-platform/current-version/rest-api-reference/platform-rest-api-version-2-resources/task.html

        Returns:
            List of dict: <List of tasks in dict Format>
        """
        
        url=self._v2BaseURL + "/api/v2/task?type=" + type
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getTaskListByType URL - " + url)
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
        infapy.log.info("Fetched List of Tasks from IICS of type " + type)
        data = response.json()
        return data