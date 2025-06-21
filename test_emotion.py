from utils.emotion import detect_emotion

# Replace this with the path to your test image
image_path = "happy_face_1.jpg"

# Paste your Hugging Face API token here (or load from env)
hf_token = "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"

# Load image bytes
with open(image_path, "rb") as f:
    image_bytes = f.read()

# Call the function
label, score = detect_emotion(image_bytes, hf_token)

# Print result
print(f"Detected emotion: {label}, Confidence: {score:.2f}")
