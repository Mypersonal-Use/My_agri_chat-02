from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ActionValidateAgricultureQuery(Action):
    def name(self) -> Text:
        return "action_validate_agriculture_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest message
        message = tracker.latest_message.get('text', '')
        
        # List of agriculture-related keywords
        agri_keywords = [
            'crop', 'farm', 'soil', 'plant', 'harvest', 'seed', 'fertilizer',
            'pest', 'disease', 'irrigation', 'weather', 'agriculture', 'farming',
            'cultivation', 'yield', 'organic', 'pesticide', 'weed', 'tractor',
            'subsidy', 'market', 'price', 'scheme', 'loan', 'credit', 'kisan'
        ]
        
        # Check if the message contains any agriculture-related keywords
        is_agri_query = any(keyword in message.lower() for keyword in agri_keywords)
        
        if not is_agri_query:
            dispatcher.utter_message(text="I can only answer questions related to agriculture and farming. Please ask me about crops, soil, pests, or other farming-related topics.")
            return []
        
        return []

class ActionProvideCropInfo(Action):
    def name(self) -> Text:
        return "action_provide_crop_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        crop_type = next(tracker.get_latest_entity_values("crop_type"), None)
        
        if crop_type:
            # Here you would typically query a database or API for crop-specific information
            response = f"I can help you with {crop_type} cultivation. Here are some key points:\n\n"
            response += "1. Soil Preparation: Ensure well-drained soil with proper pH levels\n"
            response += "2. Planting: Follow recommended spacing and depth\n"
            response += "3. Watering: Maintain consistent moisture levels\n"
            response += "4. Fertilization: Use appropriate NPK ratio\n"
            response += "5. Pest Control: Monitor regularly and use integrated pest management\n"
            response += "6. Harvesting: Follow recommended harvesting time and methods"
            
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Please specify which crop you're interested in, and I'll provide detailed information about its cultivation practices.")
        
        return []

class ActionProvideSoilInfo(Action):
    def name(self) -> Text:
        return "action_provide_soil_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        soil_type = next(tracker.get_latest_entity_values("soil_type"), None)
        
        if soil_type:
            response = f"Here's information about {soil_type} soil management:\n\n"
            response += "1. Characteristics: Understand soil composition and properties\n"
            response += "2. Improvement: Add organic matter and proper amendments\n"
            response += "3. Testing: Regular soil testing for pH and nutrients\n"
            response += "4. Conservation: Implement erosion control measures\n"
            response += "5. Maintenance: Regular monitoring and maintenance"
            
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="I can guide you on soil management. Would you like to know about soil types, testing, or improvement techniques?")
        
        return []

class ActionProvidePestInfo(Action):
    def name(self) -> Text:
        return "action_provide_pest_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        pest_name = next(tracker.get_latest_entity_values("pest_name"), None)
        disease_name = next(tracker.get_latest_entity_values("disease_name"), None)
        
        if pest_name or disease_name:
            target = pest_name or disease_name
            response = f"Here's information about {target} control:\n\n"
            response += "1. Identification: Learn to identify symptoms and signs\n"
            response += "2. Prevention: Implement preventive measures\n"
            response += "3. Control: Use appropriate control methods\n"
            response += "4. Monitoring: Regular inspection and monitoring\n"
            response += "5. Treatment: Follow recommended treatment protocols"
            
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="I can help you with pest control. Please let me know which pest or disease you're dealing with, and I'll provide appropriate solutions.")
        
        return []

class ActionProvideWeatherInfo(Action):
    def name(self) -> Text:
        return "action_provide_weather_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        region = next(tracker.get_latest_entity_values("region"), None)
        season = next(tracker.get_latest_entity_values("season"), None)
        
        if region or season:
            response = "Here's weather-related farming advice:\n\n"
            response += "1. Monitor weather forecasts regularly\n"
            response += "2. Plan farming activities according to weather conditions\n"
            response += "3. Implement protective measures for extreme weather\n"
            response += "4. Adjust irrigation based on rainfall\n"
            response += "5. Follow seasonal farming calendars"
            
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="I can help you with weather-related farming decisions. Please specify your region for localized weather information.")
        
        return []

class ActionProvideSchemeInfo(Action):
    def name(self) -> Text:
        return "action_provide_scheme_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = "Here are the main government schemes for farmers:\n\n"
        response += "1. PM-KISAN: Direct income support of ₹6000/year\n"
        response += "2. Kisan Credit Card: Easy access to credit\n"
        response += "3. Soil Health Card: Soil testing and recommendations\n"
        response += "4. Crop Insurance: Protection against crop losses\n"
        response += "5. Subsidies: For equipment, seeds, and fertilizers"
        
        dispatcher.utter_message(text=response)
        return []

class ActionProvideMarketInfo(Action):
    def name(self) -> Text:
        return "action_provide_market_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        crop_type = next(tracker.get_latest_entity_values("crop_type"), None)
        
        if crop_type:
            response = f"Here's market information for {crop_type}:\n\n"
            response += "1. Current Market Prices: Check local mandi rates\n"
            response += "2. Market Trends: Analyze price patterns\n"
            response += "3. Best Time to Sell: Consider seasonal factors\n"
            response += "4. Market Channels: Explore different selling options\n"
            response += "5. Price Optimization: Strategies for better returns"
            
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="I can provide market information. Would you like to know about current prices, market trends, or trading advice?")
        
        return []

class ActionProvideCropHealthInfo(Action):
    def name(self) -> Text:
        return "action_provide_crop_health_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        disease_name = next(tracker.get_latest_entity_values("disease_name"), None)
        
        if disease_name:
            response = f"Here's information about {disease_name}:\n\n"
            response += "1. Symptoms: Learn to identify the signs\n"
            response += "2. Causes: Understand the factors\n"
            response += "3. Prevention: Implement preventive measures\n"
            response += "4. Treatment: Follow recommended protocols\n"
            response += "5. Monitoring: Regular health checks"
            
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="I can help with crop health issues. Please describe the symptoms you're seeing, and I'll guide you on diagnosis and treatment.")
        
        return []

class ActionProvideSmartFarmingInfo(Action):
    def name(self) -> Text:
        return "action_provide_smart_farming_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = "Here's information about smart farming:\n\n"
        response += "1. IoT Applications: Sensors for monitoring\n"
        response += "2. Precision Agriculture: Data-driven farming\n"
        response += "3. Automated Systems: Irrigation and equipment\n"
        response += "4. Sustainable Practices: Eco-friendly methods\n"
        response += "5. Modern Techniques: Latest farming innovations"
        
        dispatcher.utter_message(text=response)
        return []

class ActionProvideEducationInfo(Action):
    def name(self) -> Text:
        return "action_provide_education_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = "Here are educational resources for farming:\n\n"
        response += "1. Online Courses: Agricultural training programs\n"
        response += "2. Best Practices: Modern farming techniques\n"
        response += "3. Workshops: Hands-on training sessions\n"
        response += "4. Documentation: Farming guides and manuals\n"
        response += "5. Expert Consultation: Professional guidance"
        
        dispatcher.utter_message(text=response)
        return [] 