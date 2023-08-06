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


import requests as re
import infapy
from infapy.exceptions import InvalidDetailsProvided

class AgentService():
    def __init__(self,v3,v3BaseURL,v3SessionID):
        self._v3 = v3
        self._v3BaseURL = v3BaseURL
        self._v3SessionID = v3SessionID
    
    def updateAgentService(self,serviceName, serviceAction, agentId):
        url=self._v3BaseURL + "/public/core/v3/agent/service"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        body = {
            'serviceName':serviceName,
            'serviceAction':serviceAction,
            'agentId':agentId}

        infapy.log.info("agentService API URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + str(body))

        try:
            response = re.post(url=url, json=body, headers=headers)
            data = response.json()
            infapy.log.debug(str(data))
            try:
                if ("error" in data):
                    infapy.log.error("Please validate the details passed")
                    infapy.log.error(str(data))
                    raise InvalidDetailsProvided
            except Exception as e:
                infapy.log.exception(e)
                raise
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info(data["message"])    
        return data