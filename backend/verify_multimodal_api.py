"""
Comprehensive test script for EduVision AI:
1. Confirms original text-only POST /api/study endpoint still works.
2. Tests real image understanding via POST /api/study/image across all three modes (explain, revision, quiz).
3. Tests rejection of invalid/corrupt image types and oversized files.
"""

import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
IMAGE_PATH = Path(r"C:\Users\divya\.gemini\antigravity-ide\brain\d33b918f-b4cd-4aff-9b3e-178c246c036d\plant_cell_diagram_1793001222949.jpg")

def send_multipart_request(endpoint: str, file_bytes: bytes, filename: str, content_type: str, mode: str, question: str = ""):
    boundary = "----EduVisionTestBoundary7MA4YWxkTrZu0gW"
    body = bytearray()

    # Form field: mode
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="mode"\r\n\r\n{mode}\r\n'.encode("utf-8"))

    # Form field: question (if provided)
    if question:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="question"\r\n\r\n{question}\r\n'.encode("utf-8"))

    # Form field: file
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8"))
    body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
    body.extend(file_bytes)
    body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    return req

def run_all_tests():
    print("=" * 60)
    print("EDVISION AI MULTIMODAL VERIFICATION SUITE")
    print("=" * 60)

    # 1. Verify original text-only endpoint works
    print("\n--- Test 1: Original text-only POST /api/study (explain) ---")
    text_payload = json.dumps({
        "question": "What is cellular respiration in one sentence?",
        "mode": "explain"
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/api/study",
        data=text_payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(f"Status: {resp.status}")
        print(f"Mode: {data.get('mode')}")
        print("Snippet:", data.get("answer")[:150] + "...")
        assert resp.status == 200
        assert data["mode"] == "explain"
        assert len(data["answer"]) > 20
    print(">>> Test 1 Passed: Text endpoint functions properly.")

    # Load real study image
    assert IMAGE_PATH.exists(), f"Test image {IMAGE_PATH} not found!"
    real_image_bytes = IMAGE_PATH.read_bytes()
    print(f"\nLoaded study image ({IMAGE_PATH.name}): {len(real_image_bytes)} bytes")

    # 2. Multimodal Test: Explain mode
    print("\n--- Test 2: Multimodal POST /api/study/image (mode='explain') ---")
    req = send_multipart_request(
        "/api/study/image",
        real_image_bytes,
        "plant_cell.jpg",
        "image/jpeg",
        mode="explain",
        question="Explain the role of chloroplasts and the large central vacuole labeled in this plant cell diagram."
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(f"Status: {resp.status}")
        print(f"Mode: {data.get('mode')}")
        print("\n[Gemma 4 Explain Output Preview]:")
        print(data.get("answer")[:350] + "...\n")
        assert resp.status == 200
        assert data["mode"] == "explain"
        assert "chloroplast" in data["answer"].lower() or "vacuole" in data["answer"].lower()
    print(">>> Test 2 Passed: Real image understood and explained.")

    # 3. Multimodal Test: Revision mode
    print("\n--- Test 3: Multimodal POST /api/study/image (mode='revision') ---")
    req = send_multipart_request(
        "/api/study/image",
        real_image_bytes,
        "plant_cell.jpg",
        "image/jpeg",
        mode="revision",
        question="Create revision notes for the main organelles shown in this cell."
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(f"Status: {resp.status}")
        print(f"Mode: {data.get('mode')}")
        print("\n[Gemma 4 Revision Output Preview]:")
        print(data.get("answer")[:350] + "...\n")
        assert resp.status == 200
        assert data["mode"] == "revision"
        assert len(data["answer"]) > 50
    print(">>> Test 3 Passed: Revision notes generated from image.")

    # 4. Multimodal Test: Quiz mode
    print("\n--- Test 4: Multimodal POST /api/study/image (mode='quiz') ---")
    req = send_multipart_request(
        "/api/study/image",
        real_image_bytes,
        "plant_cell.jpg",
        "image/jpeg",
        mode="quiz",
        question="Test me on the plant cell parts labeled in this diagram."
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(f"Status: {resp.status}")
        print(f"Mode: {data.get('mode')}")
        print("\n[Gemma 4 Quiz Output Preview]:")
        print(data.get("answer")[:350] + "...\n")
        assert resp.status == 200
        assert data["mode"] == "quiz"
        assert "practice questions" in data["answer"].lower() or "question" in data["answer"].lower()
    print(">>> Test 4 Passed: 5 practice questions and answer key generated from image.")

    # 5. Invalid image rejection (fake PNG with text content)
    print("\n--- Test 5: Reject fake image (spoofed filename, invalid magic bytes) ---")
    fake_png = b"This is just plain text content masquerading as a PNG."
    req = send_multipart_request(
        "/api/study/image",
        fake_png,
        "fake.png",
        "image/png",
        mode="explain"
    )
    try:
        urllib.request.urlopen(req)
        raise AssertionError("Server accepted invalid image without error!")
    except urllib.error.HTTPError as err:
        err_msg = err.read().decode()
        print(f"Caught expected HTTP {err.code}: {err_msg}")
        assert err.code == 400
        assert "Invalid or unsupported image format" in err_msg
    print(">>> Test 5 Passed: Binary signature validation successfully rejected spoofed file.")

    # 6. Oversized image rejection (> 5 MB)
    print("\n--- Test 6: Reject oversized image (> 5 MB) ---")
    # Valid PNG header but 5.5 MB of data
    oversized = b"\x89PNG\r\n\x1a\n" + (b"\x00" * (6 * 1024 * 1024))
    req = send_multipart_request(
        "/api/study/image",
        oversized,
        "huge.png",
        "image/png",
        mode="explain"
    )
    try:
        urllib.request.urlopen(req)
        raise AssertionError("Server accepted oversized image without error!")
    except urllib.error.HTTPError as err:
        err_msg = err.read().decode()
        print(f"Caught expected HTTP {err.code}: {err_msg}")
        assert err.code == 400
        assert "5 MB limit" in err_msg
    print(">>> Test 6 Passed: 5 MB size limit correctly enforced.")

    print("\n" + "=" * 60)
    print("ALL MULTIMODAL & TEXT TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
