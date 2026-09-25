from flask import Flask, request, jsonify
import json
from llm_director import generate_storyboard
from main_pipeline import load_comfyui_workflow, inject_prompts_into_workflow, send_to_modal_backend

app = Flask(__name__)

@app.route('/api/storyboard', methods=['POST'])
def handle_storyboard_request():
    """
    Webhook endpoint para n8n. Recibe una idea, genera el storyboard, 
    crea los JSONs para ComfyUI y simula el envío a Modal.
    """
    data = request.json
    if not data or 'idea' not in data:
        return jsonify({"error": "No 'idea' provided in the request body"}), 400
        
    idea = data['idea']
    print(f"\n[API] Recibida nueva idea desde n8n: '{idea}'")
    
    # 1. Generar storyboard con LLM
    storyboard = generate_storyboard(idea, num_scenes=3)
    if not storyboard:
        return jsonify({"error": "Fallo al generar el storyboard"}), 500
        
    # 2. Cargar Workflow Base
    base_workflow = load_comfyui_workflow("workflow_api.json")
    
    # 3. Procesar escenas
    processed_scenes = []
    for scene in storyboard.scenes:
        custom_workflow = inject_prompts_into_workflow(
            workflow=base_workflow.copy(),
            positive_prompt=scene.positive_prompt,
            negative_prompt=scene.negative_prompt
        )
        
        # Enviar a Modal
        send_to_modal_backend(custom_workflow, scene.scene_number)
        processed_scenes.append({
            "scene_number": scene.scene_number,
            "description": scene.description
        })
        
    # Respuesta para que n8n pueda parsearla y enviarla por Slack
    return jsonify({
        "status": "success",
        "title": storyboard.title,
        "total_scenes": len(storyboard.scenes),
        "scenes_processed": processed_scenes,
        "message": "Los workflows de ComfyUI han sido enviados a la GPU."
    })

if __name__ == '__main__':
    print("Iniciando Servidor API para integración con n8n en puerto 5000...")
    app.run(host='0.0.0.1', port=5000, debug=True)
