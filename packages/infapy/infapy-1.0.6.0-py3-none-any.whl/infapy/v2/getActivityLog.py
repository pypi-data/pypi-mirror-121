import logging
import requests as re
import infapy
import json

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class GetActivityLog:
    """This class is a handler for fetching
    the Activity Log from IICS
    """
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        self._v2 = v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
        

    def getAllActivityLog(self):
        """getAllAcitivityLog returns all the activity logs from IICS in dict format

        Returns:
            List of dict: <Activity Log in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/activity/activityLog"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("GetAllActivityLog URL - " + url)
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
        infapy.log.info("Fetched all Activity logs from IICS")
        data = response.json()
        return data

    def getActivityLogById(self,id):
        """getActivityLogById returns activity logs as specified by the log id provided in the arguments.

        Args:
            id (string): ID of Log Entry.

        Returns:
            dict: <Activity Log in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/activity/activityLog/" + id
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("GetActivityLogById URL - " + url)
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
        infapy.log.info("Fetched Activity log from IICS for Log Id " + id)
        data = response.json()
        return data

    def getActivityLogWithParams(self,offset=None,rowLimit=None,taskId=None,runId=None):
        """getActivityLogWithParams returns activity logs as specified by the optional query parameters provided in the arguments.
            If no query parameters are passed, it gives same result as getAllAcitivityLog().

        Args:
            offset (string, optional):  Number of rows to skip. Defaults to None.
            rowLimit (string, optional):  Maximum number of rows to display. Defaults to None.
            taskId (string, optional):  Task Id. Shows all activity logs for a particular task (subject to other parameters). Defaults to None.
            runId (string, optional): Run Id. Shows all activity logs for a particular run Id across all tasks(subject to other parameters). Defaults to None.

        Returns:
            List of dict: <Activity Log in dict Format>
        """
        firstParam=0
        url=self._v2BaseURL + "/api/v2/activity/activityLog"

        if offset is not None:
            if firstParam == 0:
                url=url + "?offset=" + offset
                firstParam=1
            else:
                url=url + "&offset=" + offset
        if rowLimit is not None:
            if firstParam == 0:
                url=url + "?rowLimit=" + rowLimit
                firstParam=1
            else:
                url=url + "&rowLimit=" + rowLimit
        if taskId is not None:
            if firstParam == 0:
                url=url + "?taskId=" + taskId
                firstParam=1
            else:
                url=url + "&taskId=" + taskId
        if runId is not None:
            if firstParam == 0:
                url=url + "?runId=" + runId
                firstParam=1
            else:
                url=url + "&runId=" + runId

        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("GetActivityLogWithParams URL - " + url)
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

        params=""
        if offset is not None:
                params=params + " Offset=" + offset
        if rowLimit is not None:
                params=params + " RowLimit=" + rowLimit
        if taskId is not None:
                params=params + " TaskId=" + taskId
        if runId is not None:
                params=params + " RunId=" + runId

        if params!="":
            infapy.log.info("Fetched Activity log from IICS with following Query Parameters:" + params)
        else:
            infapy.log.info("Fetched Activity log from IICS with no Query Parameters")
        data = response.json()
        return data

    def getErrorLog(self,id,location,fileName=None):
        """getErrorLog returns error logs as specified by the log id provided in the arguments.
            Writes error log to specified location with the specified filename, or default filename obtained from response.

        Args:
            id (string): ID of Log Entry.
            location (string): Location of error log to be written. Special characters such as backslashes must be escaped.
            fileName (string, optional): Custom File Name of the error log. Defaults to None.

        Returns:
            String: <Download location of error log>
        """
        url=self._v2BaseURL + "/api/v2/activity/errorLog/" + id
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("GetErrorLog URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.content))
            if fileName is None:
                fileName=response.headers.get("content-disposition").split("\"")[1]
            filePath = location.replace("\\","/") + "/" + fileName
            infapy.log.debug("Complete filename to be written: " + filePath)
            open(filePath,'wb').write(response.content)
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched Error log from IICS for Log Id " + id +"and written into: " + filePath)
        return "Error Log download complete. Download Location: " + filePath

    def getSessionLog(self,id,location,fileNameWithoutExt=None,itemId=None,childItemId=None):
        """getSessionLog returns session logs for Data Integration Tasks and Linear Taskflows as specified by the log id provided in the arguments, and optional parameters.
            Writes session log to specified location with the specified filename, or default filename obtained from response.

        Args:
            id (string): ID of Log Entry.
            location (string): Location of error log to be written. Special characters such as backslashes must be escaped.
            fileNameWithoutExt (string, optional): Custom File Name of the error log without extension. Defaults to None.
            itemId (string, optional): Item ID for subtask. Defaults to None.
            childItemId (string, optional): Item ID for sub-subtask. Defaults to None.

        Returns:
            String: <Download location of error log>
        """

        url=self._v2BaseURL + "/api/v2/activity/activityLog/" + id +"/sessionLog"

        firstParam=0
        if itemId is not None:
            if firstParam == 0:
                url=url + "?itemId=" + itemId
                firstParam=1
            else:
                url=url + "&itemId=" + itemId
        if childItemId is not None:
            if firstParam == 0:
                url=url + "?childItemId=" + childItemId
                firstParam=1
            else:
                url=url + "&childItemId=" + childItemId

        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("GetSessionLog URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.content))
            if fileNameWithoutExt is None:
                fileNameWithoutExt=response.headers.get("content-disposition").split("\"")[1].split(".")[0]
            if response.headers.get("content-type") == "application/zip;charset=UTF-8":
                extension = ".zip"
            else:
                extension = ".log"
            filePath = location.replace("\\","/") + "/" + fileNameWithoutExt + extension
            infapy.log.debug("Complete filename to be written: " + filePath)
            open(filePath,'wb').write(response.content)
        except Exception as e:
            infapy.log.exception(e)
            raise

        infapy.log.info("Fetched Session log from IICS for Log Id " + id +"and written into: " + filePath)

        params=""
        if itemId is not None:
                params=params + " itemId=" + itemId
        if childItemId is not None:
                params=params + " childItemId=" + childItemId

        if params!="":
            infapy.log.info("Query Parameters:" + params)

        return "Session Log download complete. Download Location: " + filePath  