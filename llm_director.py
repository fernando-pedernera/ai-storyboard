import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from openai import AzureOpenAI
import httpx

# Cargar variables de entorno
load_dotenv()

# Deshabilitar verificación SSL si estás en una red corporativa/universitaria
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Configurar cliente Azure OpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    http_client=httpx.Client(verify=False) # Ignorar errores SSL a nivel HTTP
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini")

class Scene(BaseModel):
    scene_number: int
    description: str = Field(description="A brief description of what happens in the scene.")
    camera_angle: str = Field(description="Camera angle or shot type (e.g., Close-up, Wide shot, Low angle).")
    positive_prompt: str = Field(description="Comma-separated keywords for image generation. Must be optimized for Stable Diffusion (e.g., 'astronaut, walking on mars, highly detailed, 8k resolution, cinematic lighting').")
    negative_prompt: str = Field(description="Comma-separated keywords to avoid (e.g., 'blurry, distorted, low quality, text, watermark, bad anatomy').")

class Storyboard(BaseModel):
    title: str
    scenes: list[Scene]

def generate_storyboard(idea: str, num_scenes: int = 4) -> Storyboard:
    """
    Acts as an AI Movie Director, breaking down a simple idea into a structured storyboard
    optimized for Stable Diffusion / ComfyUI image generation.
    """
    system_prompt = f"""You are an expert movie director and AI prompt engineer.
Your job is to take a user's raw idea and turn it into a storyboard with exactly {num_scenes} scenes.
For each scene, provide a description, the camera angle, and highly optimized positive and negative prompts 
for Stable Diffusion (ComfyUI) to generate the frame.
Focus on cinematic quality, lighting, and visual consistency across scenes."""

    try:
        completion = client.beta.chat.completions.parse(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create a storyboard for this idea: {idea}"}
            ],
            response_format=Storyboard,
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        print(f"Error llamando a la API de Azure OpenAI: {e}")
        return None

if __name__ == "__main__":
    idea = "A cybernetic samurai meditating under a neon-lit cherry blossom tree in a futuristic Tokyo."
    print(f"Generando storyboard para: '{idea}' usando Azure OpenAI (Deployment: {deployment_name})...\n")
    
    storyboard = generate_storyboard(idea)
    
    if storyboard:
        print(f"Título: {storyboard.title}\n")
        for scene in storyboard.scenes:
            print(f"Escena {scene.scene_number}: {scene.camera_angle}")
            print(f"Descripción: {scene.description}")
            print(f"Prompt Positivo: {scene.positive_prompt}")
            print(f"Prompt Negativo: {scene.negative_prompt}")
            print("-" * 50)
