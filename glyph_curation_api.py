#!/usr/bin/env python3
"""
Flask API for Glyph Curation with Custom Feedback
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from pathlib import Path
from datetime import datetime

# Import our backend
from glyph_curation_backend import GlyphCurationBackend

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the backend
backend = GlyphCurationBackend()

@app.route('/api/regenerate', methods=['POST'])
def regenerate_glyph():
    """Regenerate glyph variants with custom feedback."""
    try:
        data = request.get_json()
        
        glyph_info = data.get('glyph_info')
        custom_feedback = data.get('custom_feedback', '')
        
        if not glyph_info:
            return jsonify({'error': 'Missing glyph_info'}), 400
        
        print(f"🔄 Regenerating {glyph_info['name']} with feedback: {custom_feedback}")
        
        # Generate new variants using the backend
        result = backend.generate_glyph_variants(glyph_info)
        
        if result['success']:
            # Record the regeneration with feedback
            backend.record_selection(
                glyph_info=glyph_info,
                selected_variant=0,  # Not selected yet
                feedback=None,
                regeneration_count=1,
                custom_feedback=custom_feedback
            )
            
            return jsonify({
                'success': True,
                'message': f'Successfully regenerated {glyph_info["name"]} variants',
                'variants': [variant['path'] for variant in result['variants']],
                'feedback_recorded': bool(custom_feedback)
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Failed to generate variants')
            }), 500
            
    except Exception as e:
        print(f"❌ Error in regenerate_glyph: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/select', methods=['POST'])
def select_variant():
    """Record user selection of a variant."""
    try:
        data = request.get_json()
        
        glyph_info = data.get('glyph_info')
        selected_variant = data.get('selected_variant')
        feedback = data.get('feedback')
        regeneration_count = data.get('regeneration_count', 0)
        
        if not glyph_info or selected_variant is None:
            return jsonify({'error': 'Missing required data'}), 400
        
        # Record the selection
        backend.record_selection(
            glyph_info=glyph_info,
            selected_variant=selected_variant,
            feedback=feedback,
            regeneration_count=regeneration_count
        )
        
        return jsonify({
            'success': True,
            'message': f'Selection recorded for {glyph_info["name"]} - Variant {selected_variant}'
        })
        
    except Exception as e:
        print(f"❌ Error in select_variant: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/insights', methods=['GET'])
def get_insights():
    """Get reinforcement learning insights."""
    try:
        insights = backend.get_reinforcement_insights()
        custom_insights = backend.get_custom_feedback_insights()
        
        return jsonify({
            'success': True,
            'reinforcement_insights': insights,
            'custom_feedback_insights': custom_insights
        })
        
    except Exception as e:
        print(f"❌ Error in get_insights: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get curation progress."""
    try:
        progress = backend.get_curation_progress()
        
        return jsonify({
            'success': True,
            'progress': progress
        })
        
    except Exception as e:
        print(f"❌ Error in get_progress: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export', methods=['GET'])
def export_data():
    """Export complete curation data."""
    try:
        data = backend.export_curation_data()
        
        return jsonify({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        print(f"❌ Error in export_data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'backend_initialized': backend is not None
    })

if __name__ == '__main__':
    print("🚀 Starting Glyph Curation API Server...")
    print("=" * 50)
    print("📡 API Endpoints:")
    print("  POST /api/regenerate - Regenerate glyph variants with feedback")
    print("  POST /api/select - Record variant selection")
    print("  GET  /api/insights - Get reinforcement learning insights")
    print("  GET  /api/progress - Get curation progress")
    print("  GET  /api/export - Export curation data")
    print("  GET  /api/health - Health check")
    print("=" * 50)
    print("🌐 Server will run on: http://localhost:5002")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5002, debug=True) 