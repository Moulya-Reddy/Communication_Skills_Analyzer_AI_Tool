import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    # Flask settings
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = os.getenv('FLASK_TESTING', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # API settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:8000').split(',')
    
    # NLP Model settings
    SENTENCE_MODEL = os.getenv('SENTENCE_MODEL', 'all-MiniLM-L6-v2')
    LANGUAGE_TOOL_LANG = os.getenv('LANGUAGE_TOOL_LANG', 'en-US')
    
    # Analysis settings
    DEFAULT_DURATION_SEC = int(os.getenv('DEFAULT_DURATION_SEC', 52))
    MAX_TRANSCRIPT_LENGTH = int(os.getenv('MAX_TRANSCRIPT_LENGTH', 5000))
    
    # Speech rate thresholds (words per minute)
    SPEECH_RATE_THRESHOLDS = {
        'too_fast': (161, float('inf')),
        'fast': (141, 160),
        'ideal': (111, 140),
        'slow': (81, 110),
        'too_slow': (0, 80)
    }
    
    # Filler words list
    FILLER_WORDS = [
        'um', 'uh', 'like', 'you know', 'so', 'actually', 'basically', 
        'right', 'i mean', 'well', 'kinda', 'sort of', 'okay', 'hmm', 'ah'
    ]
    
    # Rubric weights
    RUBRIC_WEIGHTS = {
        'salutation': 5,
        'keyword_presence': 30,
        'flow': 5,
        'speech_rate': 10,
        'grammar': 10,
        'vocabulary': 10,
        'clarity': 15,
        'engagement': 15
    }
    
    # Keyword categories for content analysis
    KEYWORD_CATEGORIES = {
        'must_have': ['name', 'age', 'class', 'school', 'family', 'hobbies'],
        'good_to_have': ['from', 'goal', 'dream', 'fun fact', 'unique', 'strength', 'achievement']
    }
    
    # Salutation levels and keywords
    SALUTATION_LEVELS = {
        'excellent': {
            'keywords': ['excited to introduce', 'feeling great', 'thrilled to share', 'honored to be'],
            'score': 5
        },
        'good': {
            'keywords': ['good morning', 'good afternoon', 'good evening', 'good day', 'hello everyone'],
            'score': 4
        },
        'normal': {
            'keywords': ['hi', 'hello', 'hey'],
            'score': 2
        },
        'none': {
            'score': 0
        }
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
