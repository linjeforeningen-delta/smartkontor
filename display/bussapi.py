# Licensed under the EUPL, Version 1.2 or – as soon they will be approved by
# the European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
#   https://joinup.ec.europa.eu/software/page/eupl
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Licence for the specific language governing permissions and
# limitations under the Licence.

import json
import socket
import os
from datetime import datetime
from six.moves import urllib

# This file provides an example for calling the journeyplanner API from Python and saving the response in a file
# Please change values for ET-Client-Name and User-Agent to values that identify you, before you run this example

#Parameter busStop is a string in the form NSR:StopPlace:44085

def busApi(busStop, num_calls):
    HEADERS = {'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': 'linjeforeningen_delta - infoplakat',
                'ET-Client-Name': 'linjeforeningen_delta - infoplakat',
                'ET-Client-ID': socket.gethostname()}
    
    GRAPHQL_ENDPOINT = "https://api.entur.org/journeyplanner/2.0/index/graphql"
    CONNECT_TIMEOUT_SECONDS = 15
    
    def sendGraphqlQuery(query, variables):
        data = {'query': query, 'variables': variables}
    
        req = urllib.request.Request(GRAPHQL_ENDPOINT, json.dumps(data).encode('utf-8'), HEADERS)
    
        response = urllib.request.urlopen(req, timeout=CONNECT_TIMEOUT_SECONDS)
        return response.read().decode('utf-8')
    
    now = datetime.now().isoformat()[0:19] #Truncate the time to remove decimal places after seconds
    
    query = """
        {
          stopPlace(id: \"""" + busStop + """\") {
            id
            name
            estimatedCalls(startTime: \"""" + now + """\" timeRange: 72100, numberOfDepartures: """ + str(num_calls) + """, whiteListed: {authorities: "ATB:Authority:160"}) {     
              realtime
              aimedDepartureTime
              expectedDepartureTime
              forBoarding
              forAlighting
              destinationDisplay {
                frontText
              }
              quay {
                id
              }
              serviceJourney {
                journeyPattern {
                  line {
                    id
                    name
                  }
                }
              }
            }
          }
        }"""
    return sendGraphqlQuery(query, {})

def getBuses(busStop, num_calls):
    bus_json = busApi(busStop, num_calls)
    bus_dict = json.loads(bus_json)
    lines = []
    destinations = []
    times = []
    for i in range(num_calls):
        bus_object = bus_dict['data']['stopPlace']['estimatedCalls'][i]
        destination = bus_object['destinationDisplay']['frontText']
        destinations.append(destination)
        time = bus_object['expectedDepartureTime'][11:16]
        times.append(time)
        
        line = ""
        for j in range(9, 13):
            iterate_num = bus_object['serviceJourney']['journeyPattern']['line']['id'][j]
            if iterate_num != '0':
                line += iterate_num
        lines.append(line)        
        
            
    return lines, destinations, times