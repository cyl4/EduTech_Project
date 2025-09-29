#!/usr/bin/env python3
"""
Simple test script for the AI Presentation Coach backend
"""

import requests
import json
import time
import websocket
import threading
from io import BytesIO

# Configuration
BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"

def test_basic_endpoints():
    """Test basic HTTP endpoints"""
    print("🧪 Testing basic endpoints...")
    
    # Test homepage
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Homepage: {response.status_code}")
    except Exception as e:
        print(f"❌ Homepage failed: {e}")
    
    # Test API docs
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"✅ API docs: {response.status_code}")
    except Exception as e:
        print(f"❌ API docs failed: {e}")

def test_session_creation():
    """Test session creation and management"""
    print("\n🧪 Testing session management...")
    
    # Create session
    try:
        response = requests.post(f"{BASE_URL}/api/sessions", data={
            "mode": "professional",
            "topic": "AI in Healthcare",
            "custom_context": "Medical professionals audience"
        })
        
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data["session_id"]
            print(f"✅ Session created: {session_id}")
            return session_id
        else:
            print(f"❌ Session creation failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Session creation failed: {e}")
        return None

def test_session_summary(session_id):
    """Test getting session summary"""
    if not session_id:
        return
    
    print(f"\n🧪 Testing session summary for {session_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/sessions/{session_id}/summary")
        if response.status_code == 200:
            summary = response.json()
            print(f"✅ Session summary retrieved")
            print(f"   Topic: {summary.get('topic', 'N/A')}")
            print(f"   Mode: {summary.get('mode', 'N/A')}")
            print(f"   Total chunks: {summary.get('total_chunks', 0)}")
        else:
            print(f"❌ Session summary failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Session summary failed: {e}")

def test_websocket_connection(session_id):
    """Test WebSocket connection"""
    if not session_id:
        return
    
    print(f"\n🧪 Testing WebSocket connection for {session_id}...")
    
    def on_message(ws, message):
        print(f"📨 Received message: {len(message)} characters")
        try:
            data = json.loads(message)
            if "transcript" in data:
                print(f"   Transcript: {data['transcript'][:50]}...")
            if "score" in data:
                print(f"   Score: {data['score'].get('overall_score', 'N/A')}")
        except:
            pass
    
    def on_error(ws, error):
        print(f"❌ WebSocket error: {error}")
    
    def on_close(ws, close_status_code, close_msg):
        print("🔌 WebSocket connection closed")
    
    def on_open(ws):
        print("✅ WebSocket connection opened")
        # Send some dummy audio data
        dummy_audio = b"dummy_audio_data" * 100
        ws.send(dummy_audio, opcode=websocket.ABNF.OPCODE_BINARY)
        time.sleep(2)
        ws.close()
    
    try:
        ws = websocket.WebSocketApp(
            f"{WS_URL}/ws/{session_id}",
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        
        # Run WebSocket in a separate thread
        ws_thread = threading.Thread(target=ws.run_forever)
        ws_thread.start()
        ws_thread.join(timeout=5)
        
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")

def test_session_deletion(session_id):
    """Test session deletion"""
    if not session_id:
        return
    
    print(f"\n🧪 Testing session deletion for {session_id}...")
    
    try:
        response = requests.delete(f"{BASE_URL}/api/sessions/{session_id}")
        if response.status_code == 200:
            print("✅ Session deleted successfully")
        else:
            print(f"❌ Session deletion failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Session deletion failed: {e}")

def test_error_handling():
    """Test error handling"""
    print("\n🧪 Testing error handling...")
    
    # Test invalid session ID
    try:
        response = requests.get(f"{BASE_URL}/api/sessions/invalid-id/summary")
        if response.status_code == 404:
            print("✅ Invalid session ID handled correctly")
        else:
            print(f"❌ Invalid session ID not handled: {response.status_code}")
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting AI Presentation Coach Backend Tests")
    print("=" * 50)
    
    # Test basic endpoints
    test_basic_endpoints()
    
    # Test session management
    session_id = test_session_creation()
    
    # Test session summary
    test_session_summary(session_id)
    
    # Test WebSocket
    test_websocket_connection(session_id)
    
    # Test error handling
    test_error_handling()
    
    # Test session deletion
    test_session_deletion(session_id)
    
    print("\n" + "=" * 50)
    print("🏁 Tests completed!")
    print("\nTo run the backend:")
    print("1. Create .env file with OPENAI_API_KEY")
    print("2. Run: python main.py")
    print("3. Visit: http://localhost:8000")

if __name__ == "__main__":
    main()
