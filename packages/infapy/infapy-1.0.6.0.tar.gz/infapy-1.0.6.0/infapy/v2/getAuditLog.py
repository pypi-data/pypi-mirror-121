import logging
import requests as re
import infapy
import json

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class GetAuditLog:
    """This class is a handler for fetching
    the Audit Logs from IICS
    """
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        self._v2 = v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID

    
    def getAuditLogs(self,batchId="0",batchSize="200"):
        """getAuditLogs returns audit logs for the org based on the batchId and batchSize specified.

        Args:
            batchId (str, optional): Id to identify the batch number. Starts with 0. Defaults to "0", since this is the default in IICS.
            batchSize (str, optional): Size of Batch. Defaults to "200", since this is default in IICS.

        Returns:
            List of dict: <Audit Logs in dict Format>
        """

        url=self._v2BaseURL + "/api/v2/auditlog?batchId=" + batchId + "&batchSize=" + batchSize
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("getAuditLogs URL - " + url)
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
        low_rownum = int(batchSize) * int(batchId) + 1
        high_rownum = int(batchSize) * (int(batchId) + 1)
        infapy.log.info("Fetched Audit Log Records " + str(low_rownum) + "-" + str(high_rownum) + " for the Org")
        data = response.json()
        return data