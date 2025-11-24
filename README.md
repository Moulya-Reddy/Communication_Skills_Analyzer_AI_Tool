# Communication_Skills_Analyzer_AI_Tool

An AI-powered tool for analyzing and scoring students' spoken communication skills based on self-introduction transcripts. This application combines rule-based methods, NLP-based semantic scoring, and data-driven rubric evaluation to provide comprehensive feedback.

## 🎯 Features

- **Multi-dimensional Analysis**: Evaluates transcripts across 8 criteria including content structure, language grammar, clarity, and engagement
- **Intelligent Scoring**: Combines rule-based keyword matching with advanced NLP techniques
- **Detailed Feedback**: Provides per-criterion scores and actionable insights
- **Web Interface**: Simple, intuitive user interface for easy transcript submission
- **RESTful API**: Fully documented backend API for integration

## 📊 Scoring Criteria

| Category | Criteria | Weight | Description |
|----------|----------|---------|-------------|
| **Content & Structure** | Salutation Level | 5 points | Quality of greeting and opening |
| | Keyword Presence | 30 points | Essential personal information |
| | Flow | 5 points | Logical structure and order |
| **Speech Rate** | Words per Minute | 10 points | Appropriate speaking pace |
| **Language & Grammar** | Grammar Accuracy | 10 points | Language correctness |
| | Vocabulary Richness | 10 points | Word variety and complexity |
| **Clarity** | Filler Word Rate | 15 points | Clear expression without fillers |
| **Engagement** | Sentiment/Positivity | 15 points | Positive and engaging tone |

**Total Score: 100 points**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Web browser

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd communication-analyzer
```

2. **Set up the backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Run the backend server**
```bash
python app.py
```
The backend will start on `http://localhost:5000`

4. **Serve the frontend** (in a new terminal)
```bash
cd frontend
python -m http.server 8000
```
The frontend will be available at `http://localhost:8000`

## 📁 Project Structure

```
communication-analyzer/
├── backend/
│   ├── app.py                 # Flask application and API routes
│   ├── analyzer.py            # Core analysis logic and NLP processing
│   ├── config.py              # Configuration management
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/
│   ├── index.html             # Main web interface
│   ├── style.css              # Styling and responsive design
│   └── script.js              # Frontend logic and API integration
├── README.md                  # This file
└── deployment_guide.md        # Detailed deployment instructions
```

## 🔧 API Endpoints

### `POST /analyze`
Analyze a transcript and return comprehensive scores and feedback.

**Request:**
```json
{
  "transcript": "Hello everyone, my name is John..."
}
```

**Response:**
```json
{
  "overall_score": 86,
  "criterion_scores": {
    "salutation": 4,
    "keyword_presence": 24,
    "flow": 5,
    "speech_rate": 10,
    "grammar": 8,
    "vocabulary": 6,
    "clarity": 15,
    "engagement": 12
  },
  "detailed_feedback": {
    "salutation": "Score: 4/5 - Used good level salutation",
    "keyword_presence": "Score: 24/30 - Includes essential personal details",
    "flow": "Score: 5/5 - Proper introduction structure",
    "speech_rate": "Score: 10/10 - Appropriate pacing",
    "grammar": "Score: 8/10 - Language accuracy",
    "vocabulary": "Score: 6/10 - Word variety",
    "clarity": "Score: 15/15 - Clear expression",
    "engagement": "Score: 12/15 - Positive tone"
  },
  "word_count": 156,
  "sentence_count": 8
}
```

### `GET /health`
Health check endpoint to verify service status.

### `GET /config`
Get current configuration settings.

## 🛠 Technical Stack

### Backend
- **Framework**: Flask
- **NLP Libraries**: 
  - `language-tool-python` - Grammar checking
  - `vaderSentiment` - Sentiment analysis
  - `sentence-transformers` - Semantic analysis
  - `nltk` - Text processing
- **Configuration**: Environment-based settings

### Frontend
- **Technology**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: Modern CSS with gradients and responsive design
- **Communication**: REST API integration

## 🎯 Usage

1. **Access the application** at `http://localhost:8000`
2. **Paste a self-introduction transcript** in the text area
3. **Click "Analyze Transcript"** to process the text
4. **View results** including:
   - Overall score (0-100)
   - Detailed criterion scores
   - Specific feedback for improvement

### Sample Transcript
```
Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. 
I am 13 years old. I live with my family. There are 3 people in my family, me, my mother and my father.
One special thing about my family is that they are very kind hearted to everyone and soft spoken. 
One thing I really enjoy is playing cricket and taking wickets.
My favorite subject is science because it is very interesting. 
Thank you for listening.
```

## ⚙️ Configuration

The application can be configured through environment variables in `backend/.env`:

```env
FLASK_ENV=development
API_HOST=0.0.0.0
API_PORT=5000
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
DEFAULT_DURATION_SEC=52
MAX_TRANSCRIPT_LENGTH=5000
```

## 🔍 Analysis Methods

### Rule-based Analysis
- Keyword presence checking
- Word and sentence counting
- Filler word detection
- Structure flow validation

### NLP-based Analysis
- Grammar error detection using Language Tool
- Sentiment analysis using VADER
- Vocabulary richness (Type-Token Ratio)
- Semantic similarity scoring

### Rubric-driven Scoring
- Weighted criteria based on educational rubrics
- Normalized scoring (0-100)
- Configurable weightages

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   - Change ports in configuration or kill existing processes

2. **NLTK data missing**
   - The application automatically downloads required data on first run

3. **CORS errors**
   - Ensure frontend and backend URLs match configured CORS origins

4. **Module not found**
   - Run `pip install -r requirements.txt` to install all dependencies

### Logs
- Check console output for detailed error messages
- Backend logs appear in the terminal running `app.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is developed as part of the Nirmaan AI Intern Case Study.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the deployment guide for detailed setup instructions
3. Verify all dependencies are installed correctly
