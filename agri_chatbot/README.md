# AgriConnect Chatbot

A specialized agriculture-focused chatbot built with Rasa that provides accurate and relevant information about farming, crops, soil management, and other agricultural topics.

## Features

- Domain-specific knowledge base for agriculture
- Intent classification for agriculture-related queries
- Integration with OpenAI GPT for enhanced responses
- Support for multiple agricultural domains:
  - Crop Cultivation & Farming Techniques
  - Soil & Water Management
  - Pests, Diseases & Treatment
  - Fertilizers & Pesticides
  - Weather & Climate Insights
  - Government Schemes & Subsidies
  - Agriculture Tools & Market Info
  - Crop Health & Doctor AI Integration
  - Sustainable & Smart Farming
  - Agri-Education & Knowledge Sharing

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download spaCy model:
```bash
python -m spacy download en_core_web_md
```

4. Train the model:
```bash
rasa train
```

5. Run the chatbot:
```bash
rasa run --enable-api
```

## Project Structure

- `data/`: Contains training data and NLU data
- `actions/`: Custom action server code
- `models/`: Trained model files
- `config.yml`: Rasa configuration
- `domain.yml`: Domain configuration
- `endpoints.yml`: Endpoint configurations
- `credentials.yml`: API credentials

## Usage

The chatbot can be accessed through:
- REST API
- Command line interface
- Web interface (when configured)

## Contributing

Feel free to contribute to this project by:
1. Adding new intents and training data
2. Improving response templates
3. Adding new features and integrations 

## Additional Instructions

If you encounter the error `ModuleNotFoundError: No module named 'google'`, you need to install the `google-generativeai` package.

To install the package, run:
```bash
pip install google-generativeai
```

After installation, run your app again:
```bash
python app.py
```

If you see any errors during installation or when running the app, please copy and paste them here so I can help you further! 

To verify the installation, you can run:
```bash
pip show google-generativeai
```

You should see details about the package if it is installed. 