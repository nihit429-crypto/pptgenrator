# 🎬 PPT Generator

An AI-powered PowerPoint presentation generator that creates professional, detailed presentations from just a topic. Built with **FastAPI**, **Groq LLM**, and **python-pptx**.

## ✨ Features

- **AI-Powered Content Generation**: Uses Groq LLM (Llama 3.1/3.3) to create detailed, informative slide content
- **Beautiful Presentations**: Auto-generates professional PPTX files with:
  - Styled title slide with dark blue theme
  - Color-coded content slides
  - Bullet points with relevant information
  - Auto-fetched images from Unsplash
  - Slide numbers and accents
- **Web Interface**: Simple, user-friendly web UI to generate and preview presentations
- **Fast Downloads**: Presentations are pre-built during preview, enabling instant downloads
- **Thread-Safe Caching**: Multiple users can generate presentations simultaneously
- **Configurable**: Supports 1-30 slides with dynamic content adaptation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key ([Get one free](https://console.groq.com))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/nihit429-crypto/pptgenrator.git
cd pptgenrator

Install dependencies:
bash
pip install -r requirements.txt
Run setup to create initial directories and .env file:
bash
python setup.py
Configure your Groq API key in .env:
env
LLM_PROVIDER=groq
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
Start the server:
bash
uvicorn app.main:app --reload
Open your browser and go to http://localhost:8000
📝 How to Use
Enter Topic: Type the presentation topic (3-120 characters)
Set Slides: Choose number of slides (1-30)
Generate: Click "Generate" to create content
Preview: View slides with images and bullet points
Download: Download the PPTX file instantly
🏗️ Project Structure
Code
pptgenrator/
├── app/
│   ├── __init__.py           # Empty init file
│   ├── main.py               # FastAPI app & routes
│   ├── groq_llm.py           # LLM content generation
│   ├── pptx_builder.py       # PPTX file builder
│   ├── schemas.py            # Pydantic data models
│   └── templates/            # HTML frontend
├── scripts/                  # PowerShell setup scripts
├── setup.py                  # Initial setup script
├── requirements.txt          # Python dependencies
├── run.bat                   # Windows batch runner
└── README.md                 # This file
🔧 Core Components
groq_llm.py - Content Generation
Generates presentation outlines using Groq API
Parses JSON responses with robust error handling
Normalizes content to ensure quality
pptx_builder.py - Presentation Building
Creates beautiful PPTX files using python-pptx
Fetches images in parallel from Unsplash
Applies professional styling with color themes
Responsive layout (adapts when images are present)
main.py - Web Server
FastAPI endpoints for /, /preview, and /download
Thread-safe caching for concurrent users
Jinja2 templating for frontend
schemas.py - Data Validation
Pydantic models for request/response validation
Type-safe data handling
📦 Dependencies
fastapi - Web framework
uvicorn - ASGI server
python-dotenv - Environment variables
groq - LLM API client
python-pptx - PowerPoint generation
pydantic - Data validation
requests - HTTP client for images
Jinja2 - Template engine
⚙️ Configuration
Edit .env file:

env
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.1-8b-instant  # or llama-3.3-70b-versatile for better quality
Model Options:

llama-3.1-8b-instant - Fast, good for simple topics
llama-3.3-70b-versatile - Better quality, more detailed content
mixtral-8x7b-32768 - Alternative option
📊 Presentation Quality
Generated presentations include:

Title Slide: Dark blue theme with presentation title & subtitle
Content Slides:
Colored header bars (cycling through 5 professional colors)
Slide titles (large, bold, white text)
5-7 detailed bullet points per slide
Relevant images fetched from Unsplash
Slide numbers
Bottom accent bar
🎨 Slide Design
Title Slide: Dark navy background (RGB: 20, 40, 80)
Content Colors: Rotating teal, cyan, steel blue tones
Typography: Clean, readable fonts with proper spacing
Images: 800x600 resolution, auto-fitted alongside content
🐛 Troubleshooting
Q: "Missing GROQ_API_KEY" error

Ensure .env file exists with valid API key
Run python setup.py to recreate .env
Q: Images not appearing

Check internet connection
Images may fail silently; content will still display
Unsplash search terms are auto-generated from keywords
Q: Presentation won't download

Ensure server is running
Try generating again (cache may have expired)
Check browser console for errors
Q: Timeout/Slow generation

Groq API may be rate-limited
Try smaller number of slides
Wait a moment and try again
📄 License
MIT License - Feel free to use and modify!

🤝 Contributing
Contributions welcome! Feel free to:

Report bugs
Suggest improvements
Submit pull requests
Made with ❤️ by nihit429-crypto

Code

The README is now live in your repository! It provides:
- ✅ Clear project description & features
- ✅ Step-by-step setup instructions
- ✅ Usage guide with screenshots hints
- ✅ Complete project structure explanation
- ✅ Component descriptions
- ✅ Configuration details
- ✅ Troubleshooting section
- ✅ Professional formatting
