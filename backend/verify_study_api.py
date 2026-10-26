"""
Live verification script for GET /api/health and POST /api/study.
"""

import sys
import time
import json
import urllib.request
import urllib.error
import threading
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

import uvicorn

def run_tests():
    from app.main import app
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="error"
    )
    server = uvicorn.Server(config)
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()
    time.sleep(2.0)

    try:
        # 1. Health endpoint
        print("=== Test 1: GET /api/health ===")
        with urllib.request.urlopen("http://127.0.0.1:8000/api/health") as resp:
            health_json = json.loads(resp.read().decode())
            print(f"Status: {resp.status}")
            print(f"Response: {health_json}")
            assert resp.status == 200
            assert health_json == {"status": "ok", "service": "eduvision-api"}
        print("Test 1 Passed!\n")

        # 2. Real POST /api/study in 'explain' mode
        print("=== Test 2: POST /api/study (mode='explain') ===")
        test_payload = json.dumps({
            "question": "What is Newton's first law of motion?",
            "mode": "explain"
        }).encode("utf-8")

        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/study",
            data=test_payload,
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req) as resp:
            study_json = json.loads(resp.read().decode())
            print(f"Status: {resp.status}")
            print(f"Returned Mode: {study_json.get('mode')}")
            print("\n--- Model Response Preview ---")
            print(study_json.get("answer"))
            print("------------------------------\n")
            assert resp.status == 200
            assert study_json["mode"] == "explain"
            assert len(study_json["answer"]) > 50
        print("Test 2 Passed!\n")

        # 3. Validation test for empty question
        print("=== Test 3: POST /api/study (empty question error handling) ===")
        empty_payload = json.dumps({
            "question": "   ",
            "mode": "explain"
        }).encode("utf-8")

        empty_req = urllib.request.Request(
            "http://127.0.0.1:8000/api/study",
            data=empty_payload,
            headers={"Content-Type": "application/json"}
        )

        try:
            urllib.request.urlopen(empty_req)
            raise AssertionError("Expected 400 or 422 error for empty question, but request succeeded.")
        except urllib.error.HTTPError as err:
            err_body = err.read().decode()
            print(f"Caught expected HTTP {err.code}: {err_body}")
            assert err.code in (400, 422)
        print("Test 3 Passed!\n")

        # 4. Validation test for invalid mode
        print("=== Test 4: POST /api/study (invalid mode error handling) ===")
        invalid_mode_payload = json.dumps({
            "question": "What is gravity?",
            "mode": "invalid_mode"
        }).encode("utf-8")

        invalid_req = urllib.request.Request(
            "http://127.0.0.1:8000/api/study",
            data=invalid_mode_payload,
            headers={"Content-Type": "application/json"}
        )

        try:
            urllib.request.urlopen(invalid_req)
            raise AssertionError("Expected 422 error for invalid mode, but request succeeded.")
        except urllib.error.HTTPError as err:
            err_body = err.read().decode()
            print(f"Caught expected HTTP {err.code}: {err_body}")
            assert err.code == 422
        print("Test 4 Passed!\n")

        print(">>> ALL LIVE HTTP VERIFICATION TESTS PASSED SUCCESSFULLY! <<<")

    finally:
        server.should_exit = True

if __name__ == "__main__":
    run_tests()
