# Lunar

Lunar is a Discord chatbot built with OpenAI's API and Rasa that can perform various tasks such as generating responses based on user inputs, translating text, and telling jokes. 

## Prerequisites
- latest version of python
- OpenAI API credentials
- Discord bot token

## Installation
1. Clone the repository: `git clone https://github.com/your-username/lunar.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Set up your OpenAI API credentials and Discord bot token in `main.py`
4. Train a Rasa model and store it in the `models/nlu` directory using rasa.train.

## Usage
1. Run the bot: `python main.py`
2. Start chatting with the bot in a Discord channel where the bot is present

## Features
- Generates AI responses using Rasa based on the user's input
- Translates text to a specified language using Google Translate API
- Tells jokes using the PyJokes library

## Future Work
- Add more functionality to the bot, such as providing weather updates or news summaries
- Improve the accuracy of the language detection and translation capabilities
- Refactor the code to improve modularity and scalability

## Contributors
- Alteclipse


## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
