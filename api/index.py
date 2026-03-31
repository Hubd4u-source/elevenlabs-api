"""Main Flask API entry point for Vercel."""

import os
import sys

# Add parent directory to path for local development
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
from io import BytesIO

from api.token_manager import token_manager
from api.elevenlabs_client import ElevenLabsClient

app = Flask(__name__)
CORS(app)

# Admin authentication
ADMIN_KEY = os.getenv("ADMIN_KEY", "your-secret-admin-key-change-this")


def require_admin():
    """Check admin authentication."""
    auth_key = request.headers.get("X-Admin-Key") or request.args.get("admin_key")
    if auth_key != ADMIN_KEY:
        return jsonify({"error": "Unauthorized. Provide X-Admin-Key header or admin_key param"}), 401
    return None


@app.route("/")
def home():
    """API documentation."""
    return jsonify({
        "name": "ElevenLabs Multi-Token API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/tts": "Text-to-speech generation",
            "GET /api/voices": "List available voices",
            "GET /api/user": "Get user info",
            "GET /api/subscription": "Get subscription info",
            "GET /admin": "Admin panel (requires admin_key)",
            "GET /admin/tokens": "List all tokens (requires X-Admin-Key)",
            "POST /admin/tokens": "Add new token (requires X-Admin-Key)",
            "DELETE /admin/tokens/<index>": "Remove token (requires X-Admin-Key)",
            "PUT /admin/tokens/<index>/toggle": "Enable/disable token (requires X-Admin-Key)",
            "POST /admin/tokens/<index>/reset": "Reset failure count (requires X-Admin-Key)"
        }
    })


@app.route("/api/tts", methods=["POST"])
def text_to_speech():
    """Generate speech from text with automatic token rotation."""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body required"}), 400
    
    text = data.get("text")
    voice_id = data.get("voice_id", "cgSgspJ2msm6clMCkdW9")
    model_id = data.get("model_id", "eleven_turbo_v2_5")
    output_format = data.get("output_format", "mp3_44100_128")
    
    if not text:
        return jsonify({"error": "text field is required"}), 400
    
    # Try with token rotation
    max_attempts = len(token_manager.tokens) if token_manager.tokens else 1
    
    for attempt in range(max_attempts):
        token = token_manager.get_active_token()
        
        if not token:
            return jsonify({"error": "No active tokens available"}), 503
        
        client = ElevenLabsClient(token)
        audio, status, error = client.text_to_speech(voice_id, text, model_id, output_format)
        
        # Success
        if status == 200:
            return send_file(
                BytesIO(audio),
                mimetype="audio/mpeg",
                as_attachment=True,
                download_name=f"speech_{voice_id}.mp3"
            )
        
        # Token exhausted or failed - rotate
        if status in [402, 401, 429]:
            token_manager.mark_token_failed()
            continue
        
        # Other errors - don't rotate
        return jsonify({"error": error, "status": status}), status
    
    return jsonify({"error": "All tokens exhausted or failed"}), 503


@app.route("/api/voices", methods=["GET"])
def list_voices():
    """List available voices."""
    token = token_manager.get_active_token()
    
    if not token:
        return jsonify({"error": "No active tokens available"}), 503
    
    client = ElevenLabsClient(token)
    data, status = client.list_voices()
    
    return jsonify(data), status


@app.route("/api/user", methods=["GET"])
def get_user():
    """Get user information."""
    token = token_manager.get_active_token()
    
    if not token:
        return jsonify({"error": "No active tokens available"}), 503
    
    client = ElevenLabsClient(token)
    data, status = client.get_user()
    
    return jsonify(data), status


@app.route("/api/subscription", methods=["GET"])
def get_subscription():
    """Get subscription information."""
    token = token_manager.get_active_token()
    
    if not token:
        return jsonify({"error": "No active tokens available"}), 503
    
    client = ElevenLabsClient(token)
    data, status = client.get_subscription()
    
    return jsonify(data), status


@app.route("/admin")
def admin_panel():
    """Admin panel UI."""
    admin_key = request.args.get("admin_key", "")
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ElevenLabs Token Manager</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; margin-bottom: 30px; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; }
            .stat-card h3 { font-size: 14px; opacity: 0.9; margin-bottom: 10px; }
            .stat-card .value { font-size: 32px; font-weight: bold; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #f8f9fa; font-weight: 600; }
            .enabled { color: #28a745; font-weight: bold; }
            .disabled { color: #dc3545; font-weight: bold; }
            .current { background: #fff3cd; }
            button { padding: 6px 12px; margin: 2px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; }
            .btn-toggle { background: #007bff; color: white; }
            .btn-delete { background: #dc3545; color: white; }
            .btn-reset { background: #28a745; color: white; }
            .add-token { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; }
            input[type="text"] { padding: 10px; width: 100%; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
            .btn-add { background: #28a745; color: white; padding: 12px 24px; font-size: 16px; }
            .error { color: #dc3545; margin-top: 10px; }
            .success { color: #28a745; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 ElevenLabs Token Manager</h1>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>Total Tokens</h3>
                    <div class="value" id="total-tokens">-</div>
                </div>
                <div class="stat-card">
                    <h3>Active Tokens</h3>
                    <div class="value" id="active-tokens">-</div>
                </div>
                <div class="stat-card">
                    <h3>Total Usage</h3>
                    <div class="value" id="total-usage">-</div>
                </div>
            </div>
            
            <h2>Token Pool</h2>
            <table id="tokens-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Token Preview</th>
                        <th>Status</th>
                        <th>Usage</th>
                        <th>Failures</th>
                        <th>Last Used</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="tokens-body">
                    <tr><td colspan="7">Loading...</td></tr>
                </tbody>
            </table>
            
            <div class="add-token">
                <h3>Add New Token</h3>
                <input type="text" id="token-name" placeholder="Token Name (e.g., Account 1)">
                <input type="text" id="token-value" placeholder="Bearer Token (eyJhbGci...)">
                <button class="btn-add" onclick="addToken()">Add Token</button>
                <div id="message"></div>
            </div>
        </div>
        
        <script>
            const ADMIN_KEY = '""" + admin_key + """';
            
            async function loadTokens() {
                try {
                    const res = await fetch('/admin/tokens', {
                        headers: { 'X-Admin-Key': ADMIN_KEY }
                    });
                    const data = await res.json();
                    
                    if (data.error) {
                        document.getElementById('tokens-body').innerHTML = 
                            '<tr><td colspan="7" class="error">' + data.error + '</td></tr>';
                        return;
                    }
                    
                    const tokens = data.tokens;
                    document.getElementById('total-tokens').textContent = tokens.length;
                    document.getElementById('active-tokens').textContent = 
                        tokens.filter(t => t.enabled).length;
                    document.getElementById('total-usage').textContent = 
                        tokens.reduce((sum, t) => sum + t.usage_count, 0);
                    
                    const tbody = document.getElementById('tokens-body');
                    tbody.innerHTML = tokens.map(t => `
                        <tr class="${t.is_current ? 'current' : ''}">
                            <td>${t.name}${t.is_current ? ' 👈' : ''}</td>
                            <td><code>${t.token_preview}</code></td>
                            <td class="${t.enabled ? 'enabled' : 'disabled'}">
                                ${t.enabled ? '✓ Enabled' : '✗ Disabled'}
                            </td>
                            <td>${t.usage_count}</td>
                            <td>${t.failed_count}</td>
                            <td>${t.last_used ? new Date(t.last_used).toLocaleString() : 'Never'}</td>
                            <td>
                                <button class="btn-toggle" onclick="toggleToken(${t.index})">
                                    ${t.enabled ? 'Disable' : 'Enable'}
                                </button>
                                <button class="btn-reset" onclick="resetToken(${t.index})">Reset</button>
                                <button class="btn-delete" onclick="deleteToken(${t.index})">Delete</button>
                            </td>
                        </tr>
                    `).join('');
                } catch (err) {
                    document.getElementById('tokens-body').innerHTML = 
                        '<tr><td colspan="7" class="error">Error loading tokens: ' + err.message + '</td></tr>';
                }
            }
            
            async function addToken() {
                const name = document.getElementById('token-name').value;
                const token = document.getElementById('token-value').value;
                const msg = document.getElementById('message');
                
                if (!name || !token) {
                    msg.innerHTML = '<p class="error">Please fill in both fields</p>';
                    return;
                }
                
                try {
                    const res = await fetch('/admin/tokens', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-Admin-Key': ADMIN_KEY
                        },
                        body: JSON.stringify({ name, token })
                    });
                    const data = await res.json();
                    
                    if (data.error) {
                        msg.innerHTML = '<p class="error">' + data.error + '</p>';
                    } else {
                        msg.innerHTML = '<p class="success">Token added successfully!</p>';
                        document.getElementById('token-name').value = '';
                        document.getElementById('token-value').value = '';
                        loadTokens();
                    }
                } catch (err) {
                    msg.innerHTML = '<p class="error">Error: ' + err.message + '</p>';
                }
            }
            
            async function toggleToken(index) {
                try {
                    await fetch(`/admin/tokens/${index}/toggle`, {
                        method: 'PUT',
                        headers: { 'X-Admin-Key': ADMIN_KEY }
                    });
                    loadTokens();
                } catch (err) {
                    alert('Error: ' + err.message);
                }
            }
            
            async function resetToken(index) {
                try {
                    await fetch(`/admin/tokens/${index}/reset`, {
                        method: 'POST',
                        headers: { 'X-Admin-Key': ADMIN_KEY }
                    });
                    loadTokens();
                } catch (err) {
                    alert('Error: ' + err.message);
                }
            }
            
            async function deleteToken(index) {
                if (!confirm('Are you sure you want to delete this token?')) return;
                
                try {
                    await fetch(`/admin/tokens/${index}`, {
                        method: 'DELETE',
                        headers: { 'X-Admin-Key': ADMIN_KEY }
                    });
                    loadTokens();
                } catch (err) {
                    alert('Error: ' + err.message);
                }
            }
            
            loadTokens();
            setInterval(loadTokens, 5000);
        </script>
    </body>
    </html>
    """
    
    return render_template_string(html)


@app.route("/admin/tokens", methods=["GET"])
def admin_list_tokens():
    """List all tokens (admin only)."""
    auth_error = require_admin()
    if auth_error:
        return auth_error
    
    return jsonify({
        "tokens": token_manager.get_all_tokens(),
        "current_index": token_manager.current_index
    })


@app.route("/admin/tokens", methods=["POST"])
def admin_add_token():
    """Add a new token (admin only)."""
    auth_error = require_admin()
    if auth_error:
        return auth_error
    
    data = request.get_json()
    token = data.get("token")
    name = data.get("name", "New Token")
    
    if not token:
        return jsonify({"error": "token field is required"}), 400
    
    token_data = token_manager.add_token(token, name)
    return jsonify({"success": True, "token": token_data}), 201


@app.route("/admin/tokens/<int:index>", methods=["DELETE"])
def admin_delete_token(index):
    """Delete a token (admin only)."""
    auth_error = require_admin()
    if auth_error:
        return auth_error
    
    if token_manager.remove_token(index):
        return jsonify({"success": True})
    return jsonify({"error": "Token not found"}), 404


@app.route("/admin/tokens/<int:index>/toggle", methods=["PUT"])
def admin_toggle_token(index):
    """Enable/disable a token (admin only)."""
    auth_error = require_admin()
    if auth_error:
        return auth_error
    
    if token_manager.toggle_token(index):
        return jsonify({"success": True})
    return jsonify({"error": "Token not found"}), 404


@app.route("/admin/tokens/<int:index>/reset", methods=["POST"])
def admin_reset_token(index):
    """Reset failure count (admin only)."""
    auth_error = require_admin()
    if auth_error:
        return auth_error
    
    if token_manager.reset_failures(index):
        return jsonify({"success": True})
    return jsonify({"error": "Token not found"}), 404


# For local development
if __name__ == "__main__":
    app.run(debug=True, port=5000)
