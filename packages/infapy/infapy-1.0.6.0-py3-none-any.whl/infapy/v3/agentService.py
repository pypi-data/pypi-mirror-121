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