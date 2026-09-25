import json
import random
from llm_director import generate_storyboard

def load_comfyui_workflow(filepath: str = "workflow_api.json") -> dict:
    """Carga el workflow base de ComfyUI en formato API."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def inject_prompts_into_workflow(workflow: dict, positive_prompt: str, negative_prompt: str, seed: int = None) -> dict:
    """
    Busca los nodos de texto en el workflow JSON y reemplaza su contenido
    con los prompts generados por el LLM.
    """
    # En nuestro workflow_api.json, el Nodo "6" es el Positive Prompt, "7" es Negative, y "3" es el KSampler (semilla).
    # En un entorno de producción, esto buscaría dinámicamente el `class_type` == "CLIPTextEncode".
    
    for node_id, node_data in workflow.items():
        if node_data.get("class_type") == "CLIPTextEncode":
            # Usualmente el nodo con mayor ID o conectado de cierta forma es el negativo. 
            # Aquí lo hacemos directo por ID para la PoC.
            if node_id == "6":
                node_data["inputs"]["text"] = positive_prompt
            elif node_id == "7":
                node_data["inputs"]["text"] = negative_prompt
        
        elif node_data.get("class_type") == "KSampler":
            # Asignar una semilla aleatoria para cada imagen si no se provee
            node_data["inputs"]["seed"] = seed if seed else random.randint(1000000, 9999999)

    return workflow

def send_to_modal_backend(workflow_json: dict, scene_number: int):
    """
    Función simulada que enviaría el JSON estructurado al servidor de Modal 
    (comfy_backend.py) para su renderizado en la nube.
    """
    print(f"[{scene_number}] Enviando workflow de ComfyUI a la GPU en Modal (Nube)...")
    
    # En la vida real haríamos algo como:
    # response = requests.post("https://fernando--comfyui-backend-generate.modal.run", json=workflow_json)
    # with open(f"scene_{scene_number}.png", "wb") as f:
    #     f.write(response.content)
    
    print(f"[{scene_number}] Imagen generada y guardada como 'scene_{scene_number}.png' (Simulado)\n")

if __name__ == "__main__":
    idea_usuario = "A futuristic sci-fi city where nature has completely taken over the skyscrapers, cinematic lighting, dramatic angle."
    
    print("=" * 60)
    print(" AI STORYBOARD PIPELINE - INICIANDO ")
    print("=" * 60)
    
    # Paso 1: El LLM actúa como Director y divide la idea en escenas
    print(f"1. Generando guion y prompts para: '{idea_usuario}'")
    storyboard = generate_storyboard(idea_usuario, num_scenes=3)
    
    if not storyboard:
        print("Error: No se pudo generar el storyboard.")
        exit()
        
    print(f"¡Guion generado exitosamente! Título: {storyboard.title}\n")
    
    # Cargar el workflow base
    base_workflow = load_comfyui_workflow("workflow_api.json")
    
    # Paso 2 y 3: Iterar por cada escena, inyectar el JSON y enviar a la GPU
    for scene in storyboard.scenes:
        print(f"--- Procesando Escena {scene.scene_number}: {scene.camera_angle} ---")
        
        # Inyectar los prompts exactos en la estructura de nodos de ComfyUI
        custom_workflow = inject_prompts_into_workflow(
            workflow=base_workflow.copy(),
            positive_prompt=scene.positive_prompt,
            negative_prompt=scene.negative_prompt
        )
        
        # Guardar el JSON específico de la escena para propósitos de depuración/entrevista
        debug_filename = f"scene_{scene.scene_number}_workflow.json"
        with open(debug_filename, "w", encoding="utf-8") as f:
            json.dump(custom_workflow, f, indent=2)
        print(f"[*] JSON del Workflow de ComfyUI inyectado y guardado en {debug_filename}")
        
        # Enviar el JSON al servidor remoto en Modal
        send_to_modal_backend(custom_workflow, scene.scene_number)
    
    print("=" * 60)
    print(" Pipeline completado. Storyboard listo para producción.")
    print("=" * 60)
