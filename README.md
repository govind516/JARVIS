# Jarvis AI Assistant

## Table of Contents
- [Jarvis AI Assistant](#jarvis-ai-assistant)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Key Features](#key-features)
    - [Conversational Intelligence](#conversational-intelligence)
    - [System Automation](#system-automation)
    - [Real-Time Information](#real-time-information)
    - [Multimodal Capabilities](#multimodal-capabilities)
    - [Content Creation](#content-creation)
  - [Installation](#installation)
  - [Environment Configuration](#environment-configuration)
    - [Required API Keys](#required-api-keys)
    - [Configuration Options](#configuration-options)
  - [Usage](#usage)
    - [Example Commands](#example-commands)
      - [General Queries](#general-queries)
      - [Real-Time Information](#real-time-information-1)
      - [Automation](#automation)
      - [Image Generation Commands](#image-generation-commands)
  - [Demo](#demo)
  - [Technical Architecture](#technical-architecture)
  - [Requirements](#requirements)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Overview
Jarvis is an advanced AI assistant designed to streamline your daily tasks through natural language interactions. Combining powerful language processing capabilities with system automation, real-time information retrieval, and multimodal interactions, Jarvis serves as your personal digital assistant.

## Key Features

### Conversational Intelligence
- Advanced natural language processing via the Groq API
- Contextual understanding for meaningful, human-like conversations
- Assistance with general knowledge queries and complex problem-solving

### System Automation
- Launch applications and perform system operations through voice or text commands
- Open specific websites (Instagram, WhatsApp, etc.) on request
- Execute routine tasks with simple prompts

### Real-Time Information
- Retrieve current stock prices and market data
- Provide up-to-date news, weather, and time information
- Search the web for real-time information and summarize findings

### Multimodal Capabilities
- Speech recognition for hands-free operation
- Text-to-speech for audible responses
- Image generation based on text descriptions

### Content Creation
- Draft emails, applications, and other written content
- Generate creative text formats like poems, scripts, and stories
- Take notes during conversations

## Installation

```bash
# Clone the repository
git clone https://github.com/govind516/JARVIS.git
cd JARVIS

# Install dependencies
pip install -r requirements.txt
```

## Environment Configuration

Jarvis requires several API keys and configuration settings to function properly. Create a `.env` file in the root directory with the following variables:

```
CohereAPIKey=your_cohere_api_key
GroqAPIKey=your_groq_api_key
Username=Your Name
Assistantname=JARVIS
InputLanguage=en
AssistantVoice=en-CA-LiamNeural
HuggingFaceAPIKey=your_huggingface_api_key
```

### Required API Keys

1. **Groq API Key**: Required for the core language processing capabilities. Get it from [Groq's website](https://groq.com).
2. **Cohere API Key**: Used for enhanced text understanding and generation. Register at [Cohere's platform](https://cohere.com).
3. **HuggingFace API Key**: Needed for accessing various AI models. Sign up at [HuggingFace](https://huggingface.co).

### Configuration Options

- **Username**: Your name for personalized responses
- **Assistantname**: Name of the assistant (default: JARVIS)
- **InputLanguage**: Language code for speech recognition (default: en)
- **AssistantVoice**: Voice model for speech synthesis (default: en-CA-LiamNeural)

## Usage

```bash
# Start Jarvis
python main.py
```

### Example Commands

#### General Queries
- "What is the capital of France?"
- "Who invented the telephone?"

#### Real-Time Information
- "What is the current stock price of Tesla?"
- "Show me the latest news about AI."

#### Automation
- "Open Notepad and write an application."
- "Launch Instagram and WhatsApp."

#### Image Generation Commands
- "Generate an image of a sunset over mountains."

## Demo

A demonstration video of Jarvis in action is available in the `/demos` directory. This video showcases Jarvis's key features and provides a practical example of how to interact with the assistant.

```
/demos/jarvis-demo.mp4
```

You can also view the demo on [YouTube](https://youtu.be/your-demo-link) to see the assistant's capabilities before installation.

## Technical Architecture

Jarvis integrates several technologies:
- **Language Processing**: Groq API for understanding and generating human language
- **Web Integration**: APIs for real-time data retrieval
- **System Interaction**: Python modules for operating system automation
- **Speech Processing**: Libraries for voice recognition and synthesis
- **Image Generation**: AI models for creating images from text descriptions

## Requirements

- Python 3.8+
- Internet connection for real-time features
- Microphone (for voice commands)
- Speakers (for voice responses)
- API keys for Groq, Cohere, and HuggingFace

## Contributing

Contributions to Jarvis are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Groq for their powerful language processing API
- Cohere for text understanding capabilities
- HuggingFace for access to state-of-the-art AI models
- Contributors and maintainers of the libraries used in this project