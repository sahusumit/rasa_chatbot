# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from logging import addLevelName
from typing import Any, Text, Dict, List
from importlib_metadata import metadata

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json
import random

from sanic import response


class ActionGreet(Action):
    def name(self):
        return 'action_greet'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_greet")
        return []


class actionGreetResponse(Action):

    def name(self) -> Text:
        return "greet_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        metadata = tracker.get_slot("session_started_metadata")
        userName = metadata['userName']
        print("user Name is:", userName)
         
        # messagesList=["how may I assist you?","how can I help you?", "what can I help you with?" ]
        # message = random.choice(messagesList)
        # greatMessage = "Hello {}, {}".format(userName, message) 
      #  dispatcher.utter_message(text=greatMessage)
        return [SlotSet("name", userName)]


class ActionFacilitySearch(Action):

    def name(self) -> Text:
        return "action_facility_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        facility = tracker.get_slot("facility_type")
        location = tracker.get_slot("location")

        URL = "https://astqa2.mphrx.com/minerva/location/fetchLocations?_language=en"
        response =  requests.get(url= URL)
        flow = {"flow":"location"}
        print(response)
        events = tracker.current_state()
        print("Custom event are: ", events)
        # user_events = []
        # for e in events:
        #    if e['event'] == 'user':
        #         user_events.append(e)
        #
        # custom_data = user_events[-1]['metadata']
        # print(custom_data)
        #print(location)
        flow['data'] = response.json()
        list =[]
        if facility:
            for key in flow['data']:
            # print( '->',key['name'])
                list = list +[key['name']]
        elif location and facility:
             for key in flow['data']:
                 if key['name']==location:
                     list = list + [key]
       # print(list)
        print(len(list))
        if len(list)>0:
           dispatcher.utter_message(text="Heres is the address of the {}:{}".format(facility,list))
        else:
           dispatcher.utter_message(text="No  Hospital in this location. Please Enter different Location")
        return []



class ActionLocationInfo(Action):

    def name(self) -> Text:
        return "action_location_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        URL = "https://astqa2.mphrx.com/minerva/location/fetchLocations?_language=en"
        access_token ='b4bm4rd2j3j7gg85h63qons6i1go4312'
        headers = {'Authorization' : 'Bearer {}'.format(access_token)}
        response =  requests.post(url= URL, data=json.dumps({'name': location}), headers=headers)
        flow = {"flow":"location"}
        print(response)
        #print(location)
        flow['data'] = response.json()
        list =flow['data']
        #print(response.headers)
       # print(response.content)
        #print(list)
        if len(list)>0:
           dispatcher.utter_message(text="Heres is the address of the {}:{}".format(location,list))
        else:
           dispatcher.utter_message(text="No Hospital in this location. Please Enter different Location")

        return []



class ActionFetchAllAppointments(Action):

    def name(self) -> Text:
        return "fetch_all_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        fetchAppointmnetUrl ='http://localhost:8080/minerva/moAppointment/fetchAppointments'
        access_token ='l8g6e2e02qvds4bakceuo6njvkf04fnq'
        headers = {'Authorization' : 'Bearer {}'.format(access_token),
        'api-info':'V2|appVerson|deviceBrand|deviceModel|deviceScreenResolution|deviceOs|deviceOsVersion|deviceNetworkProvider|deviceNetworkType'
        }
        requestBody={"constraints":{"_count":10,"_skip":0,"associatedTaskCriteria":{"constraints":{"status":"requested","basedOn":[{"resourceType":"Appointment"}],"visible":"true"},"sendTaskDetails":"false"},"languageCode":"en","endDate":"<=2021-10-21T08:54:10.095Z","status:not-in":"cancelled","_sort:desc":"start.value"},"includePatientProfile":"true"}
        response =  requests.post(url= fetchAppointmnetUrl, data=json.dumps(requestBody), headers=headers)
        flow = {"flow":"location"}
        print(response)
       # print(location)
        flow['data'] = response.json()
        list =flow['data']
        # print(response.headers)
       # print(response.content)
        for key in flow['data']:
                 if key['name']==location:
                     list = list + [key]
        print(list)
        if len(list)>0:
           dispatcher.utter_message(text="Heres is the address of the {}:{}".format(location,list))
        else:
           dispatcher.utter_message(text="No Hospital in this location. Please Enter different Location")

        return []


class actionFetchDiagnosticOrderStatus(Action):

    def name(self) -> Text:
        return "report_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        reportType = tracker.get_slot("report_type")
        # reportStatusUrl ='https://webdev2.mphrx.com/minerva/MoDiagnosticOrder/fetchPdfByteStream'
        # #'https://webdev2.mphrx.com/minerva/fhir/r4/DiagnosticReport?_sort=-issued&_count=1'
        # access_token ='nsf63agrq4rfb5j2cqnftq7g960pmjtm'
        # api_info ='V3|appVerson|deviceBrand|deviceModel|deviceScreenResolution|deviceOs|deviceOsVersion|deviceNetworkProvider|deviceNetworkType'
        # headers = {'Authorization' : 'Bearer {}'.format(access_token), 'api-info':api_info, 'content-type':'application/pdf'}
        # print(reportStatusUrl)
        # requestBody= {"constraints":{"diagnosticOrderId":1640110182,"fileName":"report.pdf"}}
        # response =  requests.post(url= reportStatusUrl, data= json.dumps(requestBody),headers=headers)

        #print("Report type is:", response.json(),)
        #print("status code", response.status_code)
        response = 200
        if response == 200:
            #list = response.json()
            # print(response.content)
            # with open("response.pdf", "wb") as f:
            #   f.write(response.content)
            # print(list['entry'][0])
            # resources = list['entry'][0]['resource']['status']
            #print(resources)
            link="https://www.google.com"
            adad= "Sure, please []({}) to view the report".format(link)
            dispatcher.utter_message(text="report fecthced")
        else: dispatcher.utter_message(text="Please try again later")
        # reportLink="https://rasa.com/"
        # reportStatus = "Declared, please click this link to check the status:{}".format(reportLink) 
        # dispatcher.utter_message(text=reportStatus)
        return []


class actionViewReport(Action):

    def name(self) -> Text:
        return "action_view_declared_report"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        reportType = tracker.get_slot("view_report")
        print("Report type is:",reportType)
        reportLink="https://rasa.com/"
        carousel = {
            "type": "template",
            "payload": {
                # "template_type": "generic",
                "elements": [
                  {
                        # "title": "Title1",
                        "buttons": [{
                            "title": "Item1",
                            "url": reportLink,
                            "type": "web_url",
                            "linkTarget":"_self"
                            }
                        ]
                  },
                ],
                "metadata": {
                    "linkTarget": "_self",
                }
            }
        }
        reportStatus = "please click this link to check the status:{}".format(reportLink) 
        buttons = [
                {"payload": reportLink, "title": "Yes","target":"_top"},
                {"payload": "/deny", "title": "No"},
            ]
        metadata={'linkTarget':"sadfdsafsa"}
       
        #dispatcher.utter_message(text=reportLink)
        
        # print("Link: ",tracker.get_slot('LINK'))
        # text=tracker.latest_message['text']
        # print(text)
        dispatcher.utter_message(response="utter_happy", LINK=reportLink)
        return []