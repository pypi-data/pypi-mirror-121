import logging
import requests as re
import infapy
import json

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class License:
    """This class is a handler for fetching
    the License Details from IICS and updating License for Sub Orgs
    """
    def __init__(self,v3,v3BaseURL,v3SessionID):
        self._v3 = v3
        self._v3BaseURL = v3BaseURL
        self._v3SessionID = v3SessionID

    def getLicenseDetails(self,orgId):
        """getLicenseDetails returns license details for the specified Org Id.

        Args:
            orgId (string): Org Id.

        Returns:
            dict: <License Details in dict Format>
        """

        url=self._v3BaseURL + "/public/core/v3/license/org/" + orgId
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("getLicenseDetails URL - " + url)
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
        infapy.log.info("Fetched License Details for Org " + orgId )
        data = response.json()
        return data

    def updateSubOrgLicense(self,body,orgId):
        """updateSubOrgLicense can be used to update license for subOrg specified by the orgId, using the provided JSON body.

        Args:
            orgId (string): Sub Org Id.
            body (dict): JSON body for POST request.

        Returns:
            dict: <License Details in dict Format>
        """

        url=self._v3BaseURL + "/public/core/v3/license/org/" + orgId
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("updateSubOrgLicense URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(body))
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.put(url=url, headers=headers, json=body)
            if response.status_code==200:
                infapy.log.debug(str(response.reason))
            else:
                infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Licenses for Sub Org " + orgId + " have been updated")
        if response.status_code==200:
            data={"Status":"Licenses for Sub Org " + orgId + " have been updated."}
        else:
            data = response.json()
        return data