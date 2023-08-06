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
from infapy.exceptions import InvalidArgumentsError

class GetSecurityLogs:
    def __init__(self,v3, v3BaseURL, v3SessionID):
        self._v3 = v3
        self._v3BaseURL = v3BaseURL
        self._v3SessionID = v3SessionID

    def getSecurityLogsForLastOneDay(self):
        """getSecurityLogsForLastOneDay

        Returns:
            list of dict: The response of the security logs in the last one day
        """
        infapy.log.info("getting security logs for the last one day. Processing request....")
        url=self._v3BaseURL + "/public/core/v3/securityLog"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}

        infapy.log.info("URL to get security logs for the last one day - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")

        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the security logs for the last one day")
        data = response.json()
        infapy.log.info("getSecurityLogsForLastOneDay() completed execution")
        return data


    def getSecurityLogsByCustomQuery(self,query):
        """getSecurityLogsByCustomQuery

        Args:
            query (String): Pass the query string

        Returns:
            list of dict: The response of the security logs in json
        """
        infapy.log.info("getting security logs by query. Processing request....")
        url=self._v3BaseURL + "/public/core/v3/securityLog?q=" + str(query)
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}

        infapy.log.info("getting the security logs by query - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")

        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the security logs by query")
        data = response.json()
        infapy.log.info("getSecurityLogsByCustomQuery() completed execution")
        return data