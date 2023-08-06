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
import sys
import traceback

# All exceptions should subclass from InfapyError in this module.
class InfapyError(Exception):
    """Base class for all infapy errors."""
    

# Will be called when we are providing an invalid region
class InvalidRegionError(InfapyError):
    def __init__(self, region):
    
        msg = (
            "The region '%s' is not a valid region \n"
            "Valid regions are: us, em, ap"
            % (region)
        )
        
        InfapyError.__init__(self,msg)

class DummyInfapyErrorWithNoMessage(InfapyError):
    pass

class ConfigFileReadError(InfapyError):
    def __init__(self, region):
        
        msg = (
            "Review documentation for config file format"
        )
        
        InfapyError.__init__(self,msg)

class CredentialFileReadError(InfapyError):
    def __init__(self, region):
        
        msg = (
            "Review documentation for config file format"
        )
        
        InfapyError.__init__(self,msg)

class LimitExceededError(InfapyError):
    def __init__(self, limit):
        
        msg = (
            "Limit provided exceeds max allowed: \n"  
            "Value Currently Provided: " + str(limit)
        )
        
        InfapyError.__init__(self,msg)

class InvalidArgumentsError(InfapyError):
    def __init__(self,message=None):
        if message is not None:
            msg = (
                "Invalid Arguments for method provided\n" + message
            )
        else:
            msg = (
                "Invalid Arguments for method provided"
            )
            
        InfapyError.__init__(self,msg)

class InvalidUserDetailsProvided(InfapyError):
    def __init__(self):
        
        msg = (
            "Invalid json body for method provided. Please read the docs"
            )
        
        InfapyError.__init__(self,msg)
        
class InvalidDetailsProvided(InfapyError):
    def __init__(self, limit):
        
        msg = (
            "Json body provided for method is invalid. Please refer the doc"  
        )
        
        InfapyError.__init__(self,msg)
