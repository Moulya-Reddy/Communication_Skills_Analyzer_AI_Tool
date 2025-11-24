import re
import language_tool_python
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class CommunicationAnalyzer:
    def __init__(self, config):
        self.config = config
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Use public LanguageTool server to avoid download issues
        try:
            self.tool = language_tool_python.LanguageToolPublic('en-US')
        except:
            # Fallback: try local server, but don't fail if it doesn't work
            self.tool = None
        
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
        
        # Excellent salutations
        excellent_keywords = ['excited to introduce', 'feeling great', 'thrilled to share', 'honored to be']
        for keyword in excellent_keywords:
            if keyword in transcript_lower:
                return 5
        
        # Good salutations
        good_keywords = ['good morning', 'good afternoon', 'good evening', 'good day', 'hello everyone']
        for keyword in good_keywords:
            if keyword in transcript_lower:
                return 4
        
        # Normal salutations
        normal_keywords = ['hi', 'hello', 'hey']
        for keyword in normal_keywords:
            if keyword in transcript_lower:
                return 2
        
        return 0

    def _analyze_keyword_presence(self, transcript):
        """Analyze keyword presence"""
        transcript_lower = transcript.lower()
        must_have_score = 0
        good_to_have_score = 0
        
        # Must-have keywords (4 points each)
        must_have_keywords = ['name', 'age', 'class', 'school', 'family', 'hobbies']
        for keyword in must_have_keywords:
            if self._fuzzy_match(keyword, transcript_lower):
                must_have_score += 4
        
        # Good-to-have keywords (2 points each, max 10 points)
        good_to_have_keywords = ['from', 'goal', 'dream', 'fun fact', 'unique', 'strength', 'achievement']
        for keyword in good_to_have_keywords:
            if self._fuzzy_match(keyword, transcript_lower):
                good_to_have_score += 2
        
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
        
        # Speech rate thresholds
        if words_per_minute > 160:
            return 2  # Too fast
        elif 141 <= words_per_minute <= 160:
            return 6  # Fast
        elif 111 <= words_per_minute <= 140:
            return 10  # Ideal
        elif 81 <= words_per_minute <= 110:
            return 6  # Slow
        else:
            return 2  # Too slow

    def _analyze_language_grammar(self, transcript, words):
        """Analyze language and grammar metrics"""
        return {
            'grammar': self._analyze_grammar(transcript, len(words)),
            'vocabulary': self._analyze_vocabulary(words)
        }

    def _analyze_grammar(self, transcript, total_words):
        """Analyze grammar errors"""
        try:
            if self.tool is None:
                # If LanguageTool is not available, use a basic grammar check
                return self._basic_grammar_check(transcript, total_words)
            
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
        except:
            # Fallback to basic grammar check
            return self._basic_grammar_check(transcript, total_words)

    def _basic_grammar_check(self, transcript, total_words):
        """Basic grammar check as fallback"""
        # Simple checks for common errors
        common_errors = 0
        
        # Check for basic punctuation
        sentences = sent_tokenize(transcript)
        for sentence in sentences:
            if len(sentence.strip()) > 0 and not sentence.strip()[-1] in ['.', '!', '?']:
                common_errors += 1
        
        # Check for capitalization in sentences
        for sentence in sentences:
            if len(sentence.strip()) > 0 and not sentence.strip()[0].isupper():
                common_errors += 1
        
        errors_per_100_words = (common_errors / total_words) * 100 if total_words > 0 else 0
        grammar_score = 1 - min(errors_per_100_words / 10, 1)
        
        if grammar_score >= 0.9:
            return 10
        elif grammar_score >= 0.7:
            return 8
        elif grammar_score >= 0.5:
            return 6
        else:
            return 4

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
        
        filler_words = [
            'um', 'uh', 'like', 'you know', 'so', 'actually', 'basically', 
            'right', 'i mean', 'well', 'kinda', 'sort of', 'okay', 'hmm', 'ah'
        ]
        
        for filler in filler_words:
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
        try:
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
        except:
            # If sentiment analysis fails, return a default score
            return 9

    def _calculate_overall_score(self, criterion_scores):
        """Calculate overall score from criterion scores"""
        total_score = (
            criterion_scores['salutation'] +
            criterion_scores['keyword_presence'] +
            criterion_scores['flow'] +
            criterion_scores['speech_rate'] +
            criterion_scores['grammar'] +
            criterion_scores['vocabulary'] +
            criterion_scores['clarity'] +
            criterion_scores['engagement']
        )
        
        return min(100, total_score)

    def _fuzzy_match(self, keyword, text):
        """Fuzzy matching for keywords"""
        return keyword in text

    def _generate_detailed_feedback(self, transcript, criterion_scores):
        """Generate detailed feedback for each criterion"""
        grammar_method = "Public Server" if self.tool else "Basic Check"
        
        return {
            'salutation': f"Score: {criterion_scores['salutation']}/5 - {self._get_salutation_feedback(transcript)}",
            'keyword_presence': f"Score: {criterion_scores['keyword_presence']}/30 - Includes essential personal details",
            'flow': f"Score: {criterion_scores['flow']}/5 - Proper introduction structure",
            'speech_rate': f"Score: {criterion_scores['speech_rate']}/10 - Appropriate pacing",
            'grammar': f"Score: {criterion_scores['grammar']}/10 - Language accuracy ({grammar_method})",
            'vocabulary': f"Score: {criterion_scores['vocabulary']}/10 - Word variety",
            'clarity': f"Score: {criterion_scores['clarity']}/15 - Clear expression",
            'engagement': f"Score: {criterion_scores['engagement']}/15 - Positive tone"
        }

    def _get_salutation_feedback(self, transcript):
        """Get specific feedback for salutation"""
        transcript_lower = transcript.lower()
        
        if any(phrase in transcript_lower for phrase in ['excited to introduce', 'feeling great', 'thrilled to share']):
            return "Used excellent level salutation"
        elif any(phrase in transcript_lower for phrase in ['good morning', 'good afternoon', 'good evening', 'hello everyone']):
            return "Used good level salutation"
        elif any(phrase in transcript_lower for phrase in ['hi', 'hello', 'hey']):
            return "Used normal level salutation"
        else:
            return "No appropriate salutation found"
