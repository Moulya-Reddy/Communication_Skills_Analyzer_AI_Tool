from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import CommunicationAnalyzer
from config import get_config
import os

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    config = get_config()
    app.config.from_object(config)
    
    # Initialize CORS
    CORS(app, origins=config.CORS_ORIGINS)
    
    # Initialize analyzer
    analyzer = CommunicationAnalyzer(config)
    
    @app.route('/analyze', methods=['POST'])
    def analyze_transcript():
        try:
            data = request.get_json()
            transcript = data.get('transcript', '')
            
            if not transcript:
                return jsonify({'error': 'No transcript provided'}), 400
            
            if len(transcript) > config.MAX_TRANSCRIPT_LENGTH:
                return jsonify({
                    'error': f'Transcript too long. Maximum {config.MAX_TRANSCRIPT_LENGTH} characters allowed.'
                }), 400
            
            result = analyzer.analyze(transcript)
            return jsonify(result)
        
        except Exception as e:
            app.logger.error(f"Analysis error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'environment': os.getenv('FLASK_ENV', 'development'),
            'debug': app.config['DEBUG']
        })

    @app.route('/config', methods=['GET'])
    def get_config_info():
        """Endpoint to get current configuration (for debugging)"""
        return jsonify({
            'max_transcript_length': config.MAX_TRANSCRIPT_LENGTH,
            'default_duration_sec': config.DEFAULT_DURATION_SEC,
            'cors_origins': config.CORS_ORIGINS
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['API_HOST'],
        port=app.config['API_PORT'],
        debug=app.config['DEBUG']
    )
