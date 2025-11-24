class CommunicationAnalyzerApp {
    constructor() {
        this.apiUrl = 'http://localhost:5000/analyze';
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.getElementById('analyzeBtn').addEventListener('click', () => {
            this.analyzeTranscript();
        });
    }

    async analyzeTranscript() {
        const transcript = document.getElementById('transcriptInput').value.trim();
        
        if (!transcript) {
            alert('Please enter a transcript to analyze.');
            return;
        }

        this.showLoading(true);
        
        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ transcript })
            });

            if (!response.ok) {
                throw new Error('Analysis failed');
            }

            const result = await response.json();
            this.displayResults(result);
            
        } catch (error) {
            console.error('Error:', error);
            alert('Error analyzing transcript. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    displayResults(result) {
        // Update overall score
        document.getElementById('overallScore').textContent = result.overall_score;
        
        // Update criterion scores
        this.updateCriterionScores(result.criterion_scores);
        
        // Update detailed feedback
        this.updateDetailedFeedback(result.detailed_feedback);
        
        // Show results section
        document.getElementById('resultsSection').style.display = 'block';
    }

    updateCriterionScores(scores) {
        const container = document.getElementById('criterionScores');
        container.innerHTML = '';
        
        const criteria = [
            { key: 'salutation', label: 'Salutation', max: 5 },
            { key: 'keyword_presence', label: 'Keyword Presence', max: 30 },
            { key: 'flow', label: 'Flow', max: 5 },
            { key: 'speech_rate', label: 'Speech Rate', max: 10 },
            { key: 'grammar', label: 'Grammar', max: 10 },
            { key: 'vocabulary', label: 'Vocabulary', max: 10 },
            { key: 'clarity', label: 'Clarity', max: 15 },
            { key: 'engagement', label: 'Engagement', max: 15 }
        ];
        
        criteria.forEach(criterion => {
            const score = scores[criterion.key] || 0;
            const scoreItem = document.createElement('div');
            scoreItem.className = 'score-item';
            scoreItem.innerHTML = `
                <h4>${criterion.label}</h4>
                <div class="score-value">${score}/${criterion.max}</div>
            `;
            container.appendChild(scoreItem);
        });
    }

    updateDetailedFeedback(feedback) {
        const container = document.getElementById('detailedFeedback');
        container.innerHTML = '';
        
        Object.entries(feedback).forEach(([key, value]) => {
            const feedbackItem = document.createElement('div');
            feedbackItem.className = 'feedback-item';
            
            const label = key.split('_').map(word => 
                word.charAt(0).toUpperCase() + word.slice(1)
            ).join(' ');
            
            feedbackItem.innerHTML = `
                <h4>${label}</h4>
                <p>${value}</p>
            `;
            container.appendChild(feedbackItem);
        });
    }

    showLoading(show) {
        document.getElementById('loading').style.display = show ? 'block' : 'none';
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new CommunicationAnalyzerApp();
});
