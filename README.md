# 🤖 LLM API Response Generator

A simple Streamlit web application for generating intelligent responses using the Perplexity API.

## Features

- 🎯 Clean and intuitive user interface
- 🔐 Secure API key input (password field)
- 📝 Support for long-form prompts and questions
- 🚀 Multiple Perplexity models (sonar, sonar-pro)
- 📊 Token usage statistics for each request
- ⚡ Real-time response streaming
- 🎨 Dark theme with modern design

## Prerequisites

- Python 3.8 or higher
- Perplexity API key (get one at [https://www.perplexity.ai/settings/api](https://www.perplexity.ai/settings/api))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hellohacker143/llm-api-response.git
cd llm-api-response
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the template:
```bash
cp .env.example .env
```

5. Add your Perplexity API key to `.env`:
```
PERPLEXITY_API_KEY=your_api_key_here
```

## Usage

### Local Development

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Create a new app and connect your repository
4. Add secrets (API keys) in the Streamlit Cloud dashboard

## Configuration

### Environment Variables

- `PERPLEXITY_API_KEY` - Your Perplexity API key (required)
- `PERPLEXITY_MODEL` - Model selection (default: sonar)

### Streamlit Config

The app includes custom Streamlit configuration in `.streamlit/config.toml` for:
- Dark theme styling
- Custom color scheme
- Minimal toolbar

## Project Structure

```
llm-api-response/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── README.md             # This file
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## Available Models

- **sonar** - Fast and efficient model
- **sonar-pro** - Advanced model with enhanced capabilities

## API Response Structure

The app displays:
- Generated response text
- Token usage metrics (input, output, total)
- Response time

## Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
- Install dependencies: `pip install -r requirements.txt`

### "Error: Invalid API key"
- Verify your API key at [https://www.perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
- Ensure it's properly set in `.env` file

### Connection timeout
- Check your internet connection
- Verify Perplexity API is accessible

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open a GitHub issue.

---

**Made with ❤️ using Streamlit and Perplexity API**
