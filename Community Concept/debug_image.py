import requests
from PIL import Image
import io

# PROMPT ORIGINAL decoded: Cyberpunk style promotional poster for Sabrina Carpenter song Because I Liked a Boy, neon lights, futuristic city background, masterpiece, 8k, high resolution
# Usando endpoint directo de imagen
url = "https://image.pollinations.ai/prompt/Cyberpunk%20style%20promotional%20poster%20for%20Sabrina%20Carpenter%20song%20Because%20I%20Liked%20a%20Boy%2C%20neon%20lights%2C%20futuristic%20city%20background%2C%20masterpiece%2C%208k%2C%20high%20resolution?width=1080&height=1080&seed=42&model=flux"

print(f"⬇️ Downloading: {url}")

try:
    # Add headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"Content-Length: {len(response.content)} bytes")
    
    if response.status_code == 200:
        # Check if it's text (HTML error) or binary
        if "text" in response.headers.get('Content-Type', ''):
            print("⚠️ WARNING: Content-Type indicates text. Response excerpt:")
            print(response.text[:200])
        else:
            # Try parsing locally
            try:
                img = Image.open(io.BytesIO(response.content))
                print(f"✅ PIL can open image. Format: {img.format}, Size: {img.size}")
                
                # Save just to be sure
                with open("test_debug_image.jpg", "wb") as f:
                    f.write(response.content)
                print("Saved to test_debug_image.jpg")
                
            except Exception as e:
                print(f"❌ PIL Verification Failed: {e}")
                print("First 100 bytes of content:")
                print(response.content[:100])
    
except Exception as e:
    print(f"❌ Download failed: {e}")
