import re
import language_tool_python
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer
import numpy as np

class CommunicationAnalyzer:
    def __init__(self, config):
        self.config = config
        self.tool = language_tool_python.LanguageTool(config.LANGUAGE_TOOL_LANG)
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.sentence_model = SentenceTransformer(config.SENTENCE_MODEL)
        
        # Download required NLTK data
        self._download_nltk_data()

    def _download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')

    def analyze(self, transcript):
        """Main analysis function"""
        words = word_tokenize(transcript.lower())
        sentences = sent_tokenize(transcript)
        total_words = len(words)
        
        # Calculate all metrics
        content_scores = self._analyze_content_structure(transcript, words, sentences)
        speech_rate_score = self._analyze_speech_rate(total_words)
        language_scores = self._analyze_language_grammar(transcript, words)
        clarity_score = self._analyze_clarity(transcript, words)
        engagement_score = self._analyze_engagement(transcript)
        
        # Combine scores
        criterion_scores = {
            **content_scores,
            'speech_rate': speech_rate_score,
            **language_scores,
            'clarity': clarity_score,
            'engagement': engagement_score
        }
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(criterion_scores)
        
        return {
            'overall_score': overall_score,
            'criterion_scores': criterion_scores,
            'detailed_feedback': self._generate_detailed_feedback(transcript, criterion_scores),
            'word_count': total_words,
            'sentence_count': len(sentences)
        }

    def _analyze_content_structure(self, transcript, words, sentences):
        """Analyze content and structure metrics"""
        return {
            'salutation': self._analyze_salutation(transcript),
            'keyword_presence': self._analyze_keyword_presence(transcript),
            'flow': self._analyze_flow(sentences)
        }

    def _analyze_salutation(self, transcript):
        """Analyze salutation level"""
        transcript_lower = transcript.lower()
        
        for level, data in self.config.SALUTATION_LEVELS.items():
            if level == 'none':
                continue
                
            for keyword in data['keywords']:
                if keyword in transcript_lower:
                    return data['score']
        
        return self.config.SALUTATION_LEVELS['none']['score']

    def _analyze_keyword_presence(self, transcript):
        """Analyze keyword presence"""
        transcript_lower = transcript.lower()
        must_have_score = 0
        good_to_have_score = 0
        
        # Check must-have keywords
        for keyword in self.config.KEYWORD_CATEGORIES['must_have']:
            if self._fuzzy_match(keyword, transcript_lower):
                must_have_score += 4  # 4 points per must-have keyword
        
        # Check good-to-have keywords (max 10 points)
        for keyword in self.config.KEYWORD_CATEGORIES['good_to_have']:
            if self._fuzzy_match(keyword, transcript_lower):
                good_to_have_score += 2  # 2 points per good-to-have keyword
        
        return must_have_score + min(good_to_have_score, 10)

    def _analyze_flow(self, sentences):
        """Analyze introduction flow"""
        if len(sentences) < 2:
            return 0
            
        first_sentence = sentences[0].lower()
        last_sentence = sentences[-1].lower()
        
        has_salutation = any(word in first_sentence for word in 
                           ['hello', 'hi', 'good morning', 'good afternoon', 'good evening'])
        has_closing = any(word in last_sentence for word in ['thank', 'thanks', 'appreciate'])
        
        return 5 if (has_salutation and has_closing) else 0

    def _analyze_speech_rate(self, total_words):
        """Analyze speech rate"""
        words_per_minute = (total_words / self.config.DEFAULT_DURATION_SEC) * 60
        
        for category, (min_wpm, max_wpm) in self.config.SPEECH_RATE_THRESHOLDS.items():
            if min_wpm <= words_per_minute <= max_wpm:
                return self._get_speech_rate_score(category)
        
        return 2  # Default to lowest score

    def _get_speech_rate_score(self, category):
        """Get score for speech rate category"""
        scores = {
            'too_fast': 2,
            'fast': 6,
            'ideal': 10,
            'slow': 6,
            'too_slow': 2
        }
        return scores.get(category, 2)

    def _analyze_language_grammar(self, transcript, words):
        """Analyze language and grammar metrics"""
        return {
            'grammar': self._analyze_grammar(transcript, len(words)),
            'vocabulary': self._analyze_vocabulary(words)
        }

    def _analyze_grammar(self, transcript, total_words):
        """Analyze grammar errors"""
        matches = self.tool.check(transcript)
        errors_per_100_words = (len(matches) / total_words) * 100 if total_words > 0 else 0
        grammar_score = 1 - min(errors_per_100_words / 10, 1)
        
        if grammar_score >= 0.9:
            return 10
        elif grammar_score >= 0.7:
            return 8
        elif grammar_score >= 0.5:
            return 6
        elif grammar_score >= 0.3:
            return 4
        else:
            return 2

    def _analyze_vocabulary(self, words):
        """Analyze vocabulary richness using TTR"""
        if not words:
            return 2
            
        distinct_words = len(set(words))
        total_words = len(words)
        ttr = distinct_words / total_words
        
        if ttr >= 0.9:
            return 10
        elif ttr >= 0.7:
            return 8
        elif ttr >= 0.5:
            return 6
        elif ttr >= 0.3:
            return 4
        else:
            return 2

    def _analyze_clarity(self, transcript, words):
        """Analyze clarity through filler words"""
        if not words:
            return 3
            
        filler_count = 0
        transcript_lower = transcript.lower()
        
        for filler in self.config.FILLER_WORDS:
            # Count occurrences of filler words
            filler_count += len(re.findall(r'\b' + re.escape(filler) + r'\b', transcript_lower))
        
        filler_rate = (filler_count / len(words)) * 100
        
        if filler_rate <= 3:
            return 15
        elif filler_rate <= 6:
            return 12
        elif filler_rate <= 9:
            return 9
        elif filler_rate <= 12:
            return 6
        else:
            return 3

    def _analyze_engagement(self, transcript):
        """Analyze engagement through sentiment"""
        sentiment_scores = self.sentiment_analyzer.polarity_scores(transcript)
        positive_score = sentiment_scores['pos']
        
        if positive_score >= 0.9:
            return 15
        elif positive_score >= 0.7:
            return 12
        elif positive_score >= 0.5:
            return 9
        elif positive_score >= 0.3:
            return 6
        else:
            return 3

    def _calculate_overall_score(self, criterion_scores):
        """Calculate overall score from criterion scores"""
        total_score = 0
        
        for criterion, weight in self.config.RUBRIC_WEIGHTS.items():
            score = criterion_scores.get(criterion, 0)
            total_score += score
        
        return min(100, total_score)

    def _fuzzy_match(self, keyword, text):
        """Fuzzy matching for keywords"""
        return keyword in text

    def _generate_detailed_feedback(self, transcript, criterion_scores):
        """Generate detailed feedback for each criterion"""
        return {
            'salutation': f"Score: {criterion_scores['salutation']}/5 - {self._get_salutation_feedback(transcript)}",
            'keyword_presence': f"Score: {criterion_scores['keyword_presence']}/30 - Includes essential personal details",
            'flow': f"Score: {criterion_scores['flow']}/5 - Proper introduction structure",
            'speech_rate': f"Score: {criterion_scores['speech_rate']}/10 - Appropriate pacing",
            'grammar': f"Score: {criterion_scores['grammar']}/10 - Language accuracy",
            'vocabulary': f"Score: {criterion_scores['vocabulary']}/10 - Word variety",
            'clarity': f"Score: {criterion_scores['clarity']}/15 - Clear expression",
            'engagement': f"Score: {criterion_scores['engagement']}/15 - Positive tone"
        }

    def _get_salutation_feedback(self, transcript):
        """Get specific feedback for salutation"""
        transcript_lower = transcript.lower()
        
        for level, data in self.config.SALUTATION_LEVELS.items():
            if level == 'none':
                continue
                
            for keyword in data['keywords']:
                if keyword in transcript_lower:
                    return f"Used {level} level salutation"
        
        return "No appropriate salutation found"
