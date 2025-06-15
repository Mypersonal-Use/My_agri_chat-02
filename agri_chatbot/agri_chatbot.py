import re
from typing import Dict, List, Optional
import os
import google.generativeai as genai
from dotenv import load_dotenv
import csv
from rapidfuzz import process, fuzz
import pyttsx3
import tempfile
import base64

load_dotenv()

class AgriChatbot:
    def __init__(self):
        self.qa_pairs = self.load_qa_pairs()
        self.qa_questions = [q for q, a in self.qa_pairs]
        self.tts_engine = pyttsx3.init()
        # Set default voice properties
        self.tts_engine.setProperty('rate', 150)    # Speed of speech
        self.tts_engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        self.knowledge_base = {
            'crop_cultivation': {
                'rice': [
                    "Rice grows best in well-drained clay or loamy soil with a pH of 5.5-6.5.",
                    "1. Land Preparation: Plough and level the field. Maintain proper bunds to retain water.",
                    "2. Seed Selection: Use high-yielding, disease-resistant varieties.",
                    "3. Sowing: Transplant seedlings or direct sow seeds at 2-3 cm depth.",
                    "4. Water Management: Keep the field flooded (2-5 cm) during most of the growing period.",
                    "5. Fertilization: Apply NPK (80:40:40 kg/ha) and organic manure.",
                    "6. Pest & Disease Control: Monitor regularly and use integrated pest management.",
                    "7. Harvesting: Harvest when grains are mature and golden yellow (moisture 20-25%).",
                    "For more details, ask 'Tell me in detail about rice cultivation.'"
                ],
                'wheat': [
                    "Wheat prefers well-drained loamy soil with pH 6.0-7.5.",
                    "1. Land Preparation: Plough and harrow the field to a fine tilth.",
                    "2. Sowing: Use certified seeds, sow at 2-3 cm depth, spacing 20-22 cm between rows.",
                    "3. Watering: Irrigate at critical stages (crown root initiation, tillering, flowering, grain filling).",
                    "4. Fertilization: Apply NPK (120:60:40 kg/ha) and organic manure.",
                    "5. Weed & Pest Control: Use pre- and post-emergence herbicides, monitor for rust and aphids.",
                    "6. Harvesting: Harvest when grains are hard and moisture is 14-16%.",
                    "For more details, ask 'Tell me in detail about wheat cultivation.'"
                ],
                'vegetables': [
                    "Vegetable cultivation depends on the crop, but here are general steps:",
                    "1. Land Preparation: Loosen soil, add compost or manure.",
                    "2. Seed Selection: Choose disease-resistant, high-yielding varieties.",
                    "3. Sowing/Transplanting: Follow recommended spacing and depth for each vegetable.",
                    "4. Watering: Keep soil moist but not waterlogged.",
                    "5. Fertilization: Use balanced NPK and organic fertilizers.",
                    "6. Pest & Disease Control: Use crop rotation, organic pesticides, and regular monitoring.",
                    "7. Harvesting: Pick vegetables at the right maturity stage for best quality.",
                    "For more details, ask 'Tell me in detail about vegetable cultivation.'"
                ]
            },
            'crop_details': {
                'rice': [
                    "Detailed steps for rice cultivation:",
                    "- Nursery Preparation: Prepare a nursery bed for seedlings, sow pre-germinated seeds.",
                    "- Transplanting: Move 20-25 day old seedlings to the main field.",
                    "- Water Management: Maintain 2-5 cm water depth, drain before harvest.",
                    "- Fertilizer: Apply basal dose before transplanting, top-dress at tillering and panicle initiation.",
                    "- Pest Management: Use pheromone traps, neem oil, and recommended pesticides for stem borers, leaf folders, etc.",
                    "- Harvest: Cut when 80% grains are mature, dry before storage."
                ],
                'wheat': [
                    "Detailed steps for wheat cultivation:",
                    "- Seed Treatment: Treat seeds with fungicide before sowing.",
                    "- Sowing Time: Optimal time is November-December in India.",
                    "- Irrigation: 4-6 irrigations at critical stages.",
                    "- Fertilizer: Split application of nitrogen, full dose of phosphorus and potassium at sowing.",
                    "- Disease Management: Watch for rust, smut, and blight; use resistant varieties and fungicides.",
                    "- Harvest: Harvest when grains are hard, thresh and dry before storage."
                ],
                'vegetables': [
                    "Detailed steps for vegetable cultivation:",
                    "- Crop Selection: Choose crops based on season and market demand.",
                    "- Nursery Raising: For crops like tomato, brinjal, and chili, raise seedlings in a nursery.",
                    "- Transplanting: Transplant healthy seedlings at 4-6 leaf stage.",
                    "- Fertilizer: Apply compost and NPK as per crop requirement.",
                    "- Pest Management: Use sticky traps, neem oil, and crop rotation.",
                    "- Harvest: Harvest at the right stage for each crop."
                ]
            },
            'soil_management': {
                'clay': [
                    "Clay soil has high water retention but poor drainage.",
                    "Add organic matter to improve structure.",
                    "Use deep tillage to break compacted layers.",
                    "Consider raised beds for better drainage.",
                    "Monitor soil pH and adjust as needed."
                ],
                'sandy': [
                    "Sandy soil has good drainage but poor water retention.",
                    "Add organic matter to improve water retention.",
                    "Use mulch to reduce water evaporation.",
                    "Apply fertilizers in smaller, frequent doses.",
                    "Consider drip irrigation for efficient water use."
                ]
            },
            'pest_control': {
                'aphids': [
                    "Aphids are small, soft-bodied insects that suck plant sap.",
                    "Use neem oil or insecticidal soap for control.",
                    "Introduce natural predators like ladybugs.",
                    "Remove heavily infested plant parts.",
                    "Monitor regularly for early detection."
                ],
                'fungal_diseases': [
                    "Common fungal diseases include powdery mildew and rust.",
                    "Ensure proper air circulation around plants.",
                    "Use fungicides as preventive measures.",
                    "Remove and destroy infected plant parts.",
                    "Maintain proper plant spacing."
                ]
            },
            'weather': {
                'general': [
                    "Monitor weather forecasts regularly.",
                    "Plan farming activities according to weather conditions.",
                    "Implement protective measures for extreme weather.",
                    "Adjust irrigation based on rainfall.",
                    "Follow seasonal farming calendars."
                ]
            },
            'government_schemes': {
                'general': [
                    "PM-KISAN: Direct income support of ₹6000/year.",
                    "Kisan Credit Card: Easy access to credit.",
                    "Soil Health Card: Soil testing and recommendations.",
                    "Crop Insurance: Protection against crop losses.",
                    "Subsidies: For equipment, seeds, and fertilizers."
                ]
            }
        }
        
        self.patterns = {
            'greeting': r'^(hi|hello|hey|greetings)',
            'goodbye': r'^(bye|goodbye|see you)',
            'crop_query': r'(how|what|tell me|explain|steps|process|guide|detailed|detail|information|about).*(grow|cultivate|plant|produce|raise|farming|cultivation).*?(rice|wheat|vegetables?)',
            'crop_detail_query': r'(detail|detailed|explain|more|steps|process|how).*?(rice|wheat|vegetables?)',
            'soil_query': r'(how|what|tell me|explain|about).*(soil|land).*?(clay|sandy)',
            'pest_query': r'(how|what|tell me|explain|about).*(pest|disease|control).*?(aphids|fungal diseases)',
            'weather_query': r'(how|what|tell me|explain|about).*(weather|climate)',
            'scheme_query': r'(how|what|tell me|explain|about).*(scheme|subsidy|government)'
        }
        self.last_topic = None
        self.last_topic_type = None
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')

    def load_qa_pairs(self):
        qa_pairs = []
        try:
            # Try to load from the data directory first
            data_path = os.path.join('data', 'agricultural_training_data.txt')
            if not os.path.exists(data_path):
                # If not found, create a basic training data file
                with open(data_path, 'w', encoding='utf-8') as f:
                    f.write('question,answer\n')
                    f.write('"What is organic farming?","Organic farming is a method of crop and livestock production that involves much more than choosing not to use pesticides, fertilizers, genetically modified organisms, antibiotics, and growth hormones."\n')
                    f.write('"How to grow tomatoes?","Tomatoes need full sun, well-drained soil, and regular watering. Plant seeds indoors 6-8 weeks before last frost, transplant when seedlings are 6-8 inches tall, and provide support as they grow."\n')
                    f.write('"What is crop rotation?","Crop rotation is the practice of growing different types of crops in the same area across different seasons to improve soil health, optimize nutrients, and combat pest and weed pressure."\n')
            
            with open(data_path, encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # skip header
                for row in reader:
                    if len(row) >= 2:
                        question = row[0].strip().strip('"')
                        answer = row[1].strip().strip('"')
                        qa_pairs.append((question, answer))
        except Exception as e:
            print(f"Error loading Q&A pairs: {e}")
        return qa_pairs

    def speak_response(self, text: str) -> Dict[str, str]:
        """Convert text to speech and return both text and audio data."""
        try:
            # Create a temporary file to store the audio
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_filename = temp_file.name

            # Save the speech to the temporary file
            self.tts_engine.save_to_file(text, temp_filename)
            self.tts_engine.runAndWait()

            # Read the audio file and convert to base64
            with open(temp_filename, 'rb') as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode('utf-8')

            # Clean up the temporary file
            os.unlink(temp_filename)

            return {
                'text': text,
                'audio': audio_data
            }
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            return {
                'text': text,
                'audio': None
            }

    def get_response(self, user_input: str, gemini_api_key: Optional[str] = None) -> Dict[str, str]:
        user_input = user_input.lower().strip()

        # Handle greetings first
        if re.search(self.patterns['greeting'], user_input):
            return self.speak_response("Hello! Welcome to AgriConnect. How can I assist you with agriculture today?")

        # Agriculture-related keywords
        agri_keywords = [
            'crop', 'farm', 'soil', 'plant', 'harvest', 'seed', 'fertilizer',
            'pest', 'disease', 'irrigation', 'weather', 'agriculture', 'farming',
            'cultivation', 'yield', 'organic', 'pesticide', 'weed', 'tractor',
            'subsidy', 'market', 'price', 'scheme', 'loan', 'credit', 'kisan',
            'livestock', 'dairy', 'compost', 'vermicompost', 'mulch', 'manure',
            'horticulture', 'greenhouse', 'drip', 'sprinkler', 'germination', 'extension',
            'poultry', 'goat', 'sheep', 'cattle', 'paddy', 'wheat', 'rice', 'vegetable',
            'fruit', 'orchard', 'fodder', 'seedling', 'grafting', 'pruning', 'blight', 'fungus',
            'insect', 'aphid', 'mildew', 'rot', 'compost', 'hydroponic', 'aquaponic', 'vertical farm',
            'climate', 'rain', 'drought', 'monsoon', 'season', 'mandi', 'mandy', 'mandis', 'mandys'
        ]
        if not any(word in user_input for word in agri_keywords):
            return self.speak_response("I can only answer questions related to agriculture and farming. Please ask me about crops, soil, pests, or other farming-related topics.")

        # Use provided API key or get from environment
        api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            return self.speak_response("Please provide a valid Gemini API key to get accurate responses.")

        try:
            # Special case: weeds
            if 'weed' in user_input or 'weeds' in user_input:
                return self.speak_response("Weeds are unwanted plants that compete with crops. It's best to control weeds using manual weeding, mulching, or safe herbicides. Growing weeds is not recommended for farmers.")

            # 1. Try to match user input to Q&A pairs
            if self.qa_pairs:
                match, score, idx = process.extractOne(user_input, self.qa_questions, scorer=fuzz.token_sort_ratio)
                if score > 80:
                    return self.speak_response(self.qa_pairs[idx][1])

            # 2. Check knowledge base for specific topics
            for pattern_name, pattern in self.patterns.items():
                if re.search(pattern, user_input):
                    if pattern_name == 'crop_query':
                        for crop in ['rice', 'wheat', 'vegetables']:
                            if crop in user_input:
                                return self.speak_response('\n'.join(self.knowledge_base['crop_cultivation'][crop]))
                    elif pattern_name == 'crop_detail_query':
                        for crop in ['rice', 'wheat', 'vegetables']:
                            if crop in user_input:
                                return self.speak_response('\n'.join(self.knowledge_base['crop_details'][crop]))
                    elif pattern_name == 'soil_query':
                        for soil_type in ['clay', 'sandy']:
                            if soil_type in user_input:
                                return self.speak_response('\n'.join(self.knowledge_base['soil_management'][soil_type]))
                    elif pattern_name == 'pest_query':
                        for pest in ['aphids', 'fungal diseases']:
                            if pest in user_input:
                                return self.speak_response('\n'.join(self.knowledge_base['pest_control'][pest]))
                    elif pattern_name == 'weather_query':
                        return self.speak_response('\n'.join(self.knowledge_base['weather']['general']))
                    elif pattern_name == 'scheme_query':
                        return self.speak_response('\n'.join(self.knowledge_base['government_schemes']['general']))

            # 3. Fallback: Use Gemini with few-shot examples from Q&A file
            if api_key:
                few_shot_examples = self.qa_pairs[:5]
                prompt = "You are an agriculture expert. Here are some example Q&A pairs to guide your answers.\n"
                for q, a in few_shot_examples:
                    prompt += f"Q: {q}\nA: {a}\n"
                prompt += f"Q: {user_input}\nA:"
                response = self.ask_gemini(prompt, api_key)
                if response.startswith("Sorry, I couldn't"):
                    # If Gemini fails, try to provide a more helpful response
                    return self.speak_response("I understand your question about agriculture, but I'm having trouble generating a detailed response right now. Please try rephrasing your question or ask about a specific aspect of farming, crops, soil, or agricultural practices.")
                return self.speak_response(response)

            return self.speak_response("I can only answer questions related to agriculture and farming. Please ask me about crops, soil, pests, or other farming-related topics.")
        except Exception as e:
            error_message = str(e)
            if "API key" in error_message.lower():
                return {"text": "Invalid API key. Please provide a valid Gemini API key.", "error": True}
            return {"text": f"An error occurred while processing your request: {error_message}", "error": True}

    def ask_gemini(self, prompt: str, api_key: str) -> str:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-lite')
            response = model.generate_content(prompt)
            if not response or not response.text:
                raise Exception("Empty response from Gemini API")
            return response.text.strip()
        except Exception as e:
            error_message = str(e)
            if "API key" in error_message.lower():
                raise Exception("Invalid API key")
            raise Exception(f"Error generating response: {error_message}")

def main():
    chatbot = AgriChatbot()
    print("Welcome to AgriConnect! Type 'quit' to exit.")
    api_key = input("Please enter your Gemini API key (or press Enter to use rule-based only): ").strip()
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        response = chatbot.get_response(user_input, gemini_api_key=api_key if api_key else None)
        print("\nAgriConnect:", response['text'])

        # Add this block to handle TTS
        self.tts_engine.say(response['text'])
        self.tts_engine.runAndWait()

if __name__ == "__main__":
    main() 