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

import logging
import requests as re
import infapy
import json

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class JobControl:
    """This class is a handler for controlling
    Jobs in IICS
    """
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        self._v2 = v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID


    def startJob(self,body):
        """startJob starts Data Integration Jobs based on the JSON body specification.

        Args:
            body (dict): JSON body for POST request.

        Returns:
            dict: <Response of Start Job Request in dict Format>
        """

        url=self._v2BaseURL + "/api/v2/job"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("startJob URL - " + url)
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
        infapy.log.info("Job Start Request completed.")        
        data = response.json()
        return data

    def stopJob(self,body):
        """stopJob stops running Data Integration Jobs based on the JSON body specification.

        Args:
            body (dict): JSON body for POST request.

        Returns:
            dict: <Response of Stop Job Request in dict Format>
        """

        url=self._v2BaseURL + "/api/v2/job/stop"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("stopJob URL - " + url)
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
        infapy.log.info("Job Stop Request completed.")        
        data = response.json()
        return data