# Generative AI Platform

A FastAPI-based platform designed to generate utterances and automate intelligent text processing with data privacy protection through entity masking.

## Overview

This project creates a Generative AI platform with the capability of:
- Generating utterances for various intents
- Automating intelligent text processing
- Protecting sensitive data through entity masking
- Caching responses to reduce redundancy
- Integrating multiple AI models (Phi3, OpenAI, etc.)

## Project Phases

### Phase 1 (Current)
- ✅ Cache implementation to reduce query redundancy
- ✅ Generate utterances from user prompts
- ✅ Create maintainable templates
- ✅ Data masking for sensitive information (Input/Output Guardians)
- ✅ FastAPI integration for API and frontend
- ✅ Phi3 model invocation with templates

### Phase 2 (Planned)
- Model jailbreak prevention strategies
- Enhanced data masking using GLiNER
- Additional model integrations

### Phase 3 (Future)
- chatbot project plan creation

## Architecture

### Core Components

#### 1. **Main Application** (`main.py`)
- FastAPI REST API server
- GET endpoint: `/getResponse` - Takes user input text and model name
- Intelligent routing based on user intent (e.g., "generate" keyword detection)

#### 2. **Cache Layer** (`reducelatency.py`)
- `FirstCache` class manages response caching using Redis
- Reduces redundancy by storing and retrieving previously generated responses
- Falls back to template generation if cache miss occurs

#### 3. **Template Generation** (`getTemplates.py`)
- `TemplateCreator` class creates intent templates
- Integrates with LangChain for prompt template management
- Applies data masking before template generation

#### 4. **Data Protection** (`Guardial.py`)
- `InputGuardial` class masks sensitive information
- Uses HuggingFace model: `Isotonic/distilbert_finetuned_ai4privacy_v2`
- Entity extraction and replacement (e.g., phone numbers → [PHONE_NUMBER])
- Supports various entity types: names, emails, account numbers, etc.

#### 5. **Model Invocation** (`models.py`)
- `InvokeGenAI` class handles model execution
- Extensible model registry for different AI models
- Current support: Phi3, OpenAI
- Returns responses in JSON format

## Installation

### Prerequisites
- Python 3.8+
- Redis server running on localhost:6379

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd genAiPlatform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Redis** (if not already installed)
   - Windows: Download from https://github.com/microsoftarchive/redis/releases
   - Linux: `sudo apt-get install redis-server`
   - macOS: `brew install redis`

## Usage

### Running the Server

```bash
python main.py
```

The FastAPI server will start on `http://localhost:8000`

### API Endpoints

#### Get Response
- **Endpoint**: `GET /getResponse`
- **Parameters**:
  - `text` (string, required): User input text
  - `model` (string, required): AI model name (e.g., "phi3", "openAI")

**Example Request**:
```bash
curl "http://localhost:8000/getResponse?text=Generate%20Utterances%20for%20Login%20Intent&model=phi3"
```

**Response**:
```json
{
  "response": "Phi3 model response for generated utterances template"
}
```

### Data Flow

1. **User Input** → FastAPI endpoint receives text and model name
2. **Intent Detection** → Checks if text contains "generate" keyword
3. **Cache Check** → FirstCache checks Redis for existing response
4. **Template Generation** → If cache miss:
   - InputGuardial masks sensitive data
   - TemplateCreator generates prompt template
5. **Model Invocation** → InvokeGenAI calls appropriate AI model
6. **Response Return** → Result returned to user

## Dependencies

Key dependencies include:
- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server
- **Redis**: Caching layer
- **Transformers**: HuggingFace model integration
- **LangChain**: Prompt template management
- **TensorFlow/Keras**: ML framework for entity extraction
- **Pydantic**: Data validation

See `requirements.txt` for complete list.

## File Structure

```
genAiPlatform/
├── main.py                    # FastAPI application entry point
├── reducelatency.py          # Cache management (FirstCache)
├── getTemplates.py           # Template creation (TemplateCreator)
├── Guardial.py               # Data masking (InputGuardial)
├── models.py                 # Model invocation (InvokeGenAI)
├── requirements.txt          # Python dependencies
├── info.txt                  # Project documentation
├── libraries.txt             # Library information
└── README.md                 # This file
```

## Configuration

### Redis Configuration
- **Host**: localhost
- **Port**: 6379
- **Decode Responses**: True

### Model Configuration
- **Entity Masking Model**: `Isotonic/distilbert_finetuned_ai4privacy_v2`
- **Device**: CPU (-1)

Modify `Guardial.py` to change model or device settings.

### FastAPI Configuration
- **Host**: 0.0.0.0
- **Port**: 8000
- **Reload**: Enabled for development

Modify `main.py` to change server configuration.

## Development

### Adding New Models

To add a new AI model:

1. Implement a method in `models.py` InvokeGenAI class:
   ```python
   def new_model(self):
       # Implementation here
       return response
   ```

2. Register in the `model_functions` dictionary:
   ```python
   self.model_functions = {
       "phi3": self.phy3Model,
       "new_model": self.new_model,
   }
   ```

### Extending Entity Masking

The `InputGuardial` class can be extended to support additional entity types or custom masking strategies by modifying the entity replacement logic.

## Performance Optimization

- **Caching**: Redis caching reduces redundant model calls
- **Device Selection**: CPU mode for better compatibility (modify for GPU if available)
- **Batch Processing**: Future enhancement for handling multiple requests

## Security Considerations

- Sensitive data is automatically masked before processing
- Entity masking prevents data leakage through model outputs
- Input validation through FastAPI/Pydantic
- Future: Jailbreak prevention strategies (Phase 2)

## Troubleshooting

### Redis Connection Error
- Ensure Redis server is running: `redis-cli ping`
- Verify connection parameters in `reducelatency.py`

### Model Loading Issues
- Download required HuggingFace models first time (automatic)
- Requires internet connection for initial setup
- Check disk space for model files

### FastAPI Server Won't Start
- Check if port 8000 is already in use
- Verify all dependencies are installed
- Check Python version compatibility

## Future Enhancements

- [ ] GPU support for faster inference
- [ ] Advanced caching strategies
- [ ] Model jailbreak prevention
- [ ] GLiNER integration for improved entity extraction
- [ ] Kore AI project plan generation
- [ ] Additional AI model integrations
- [ ] API authentication and rate limiting
- [ ] Comprehensive logging and monitoring

## Contributing

To contribute to this project:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

[Add your license information here]

## Support

For issues, questions, or suggestions, please create an issue in the repository.

---

**Project Status**: Phase 1 - Active Development
