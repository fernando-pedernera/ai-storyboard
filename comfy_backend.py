import modal
import subprocess
import os
import urllib.request

# Define the Modal App
app = modal.App(name="comfyui-backend")

# Define the container image
# We start with a base Python image and install necessary dependencies for ComfyUI
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "curl", "libgl1", "libglib2.0-0")
    .pip_install(
        "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu121"
    )
    .pip_install("xformers")
    .run_commands(
        "git clone https://github.com/comfyanonymous/ComfyUI.git /root/ComfyUI",
        "cd /root/ComfyUI && pip install -r requirements.txt"
    )
)

# Download a base model (SDXL) during the image build step so it's cached
def download_models():
    model_url = "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors"
    dest_path = "/root/ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors"
    
    if not os.path.exists(dest_path):
        print(f"Downloading model to {dest_path}...")
        urllib.request.urlretrieve(model_url, dest_path)
        print("Download complete.")

# Add the model download to the image build process
image = image.run_function(download_models)

@app.function(
    image=image,
    gpu="T4", # Using a T4 GPU which is highly cost-effective ($0.000164/sec)
    timeout=600, # 10 minutes max execution time
)
@modal.web_endpoint(method="POST")
def generate_image(prompt: dict):
    """
    This endpoint will receive a prompt payload, start ComfyUI headlessly, 
    inject the prompt, generate the image, and return it.
    """
    # NOTE: This is a placeholder structure for Phase 1. 
    # In Phase 3, we will add the exact code to interact with the ComfyUI API locally within the container.
    
    return {
        "status": "success",
        "message": "ComfyUI environment is ready. Received prompt.",
        "received_data": prompt
    }

# Para correr este código localmente y desplegarlo en Modal, el usuario ejecutará:
# modal deploy comfy_backend.py
