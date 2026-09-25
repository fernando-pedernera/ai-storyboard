# Plan de Proyecto: Generador Automatizado de Storyboards y Animáticas (AI Storyboard & Animatic Pipeline)

## 1. Resumen del Proyecto
Para destacar en la entrevista para el puesto de **AI Developer & Generative Technologist**, este proyecto consistirá en construir un *pipeline* automatizado que convierta una idea de texto simple en un storyboard visual completo, y opcionalmente en una animática (video corto). 

El proyecto demostrará tu capacidad para integrar LLMs con herramientas de generación de imágenes y video (ComfyUI), orquestándolo todo con Python y demostrando un enfoque hacia la producción audiovisual, tal como lo requiere el puesto.

## 2. Alineación con los Requisitos del Puesto
Este proyecto toca directamente los puntos clave de la oferta de trabajo:
*   **ComfyUI (Imprescindible) & Stable Diffusion/Flux:** Se usará ComfyUI en modo *headless* (mediante su API) para generar las imágenes usando flujos de trabajo avanzados.
*   **LLMs (Claude / OpenAI):** Se usará un LLM para expandir una idea corta en un guion estructurado escena por escena, generando los *prompts* (positivos y negativos) específicos para ComfyUI.
*   **LoRA & ControlNet:** Se integrarán en el flujo de ComfyUI para mantener la consistencia del estilo (LoRA) y la composición de las escenas (ControlNet - ej. poses o profundidad).
*   **Python & Git:** Python será el "pegamento" que orquestará las llamadas a la API del LLM y a la API de ComfyUI. Todo estará versionado en Git.
*   **Automatización de Workflows / n8n (Deseable):** El script de Python puede ser expuesto como un webhook que n8n consuma, demostrando conocimientos en automatización.
*   **Background Audiovisual:** El resultado es un producto directamente aplicable a estudios creativos y de video (un storyboard/animática).

## 3. Arquitectura del Sistema
El flujo será el siguiente:
1.  **Input:** El usuario envía una frase (ej. "Un astronauta descubriendo un templo antiguo en Marte").
2.  **Agente LLM (Python + Claude/OpenAI API):** El script en Python envía la frase al LLM con un *system prompt* que le indica actuar como un Director de Cine. El LLM devuelve un JSON con 4-5 escenas, detallando: descripción de la escena, ángulo de cámara, y el *prompt* exacto para Stable Diffusion.
3.  **Generación Visual (Python + ComfyUI API):** El script lee el JSON y, por cada escena, envía el *prompt* al servidor local de ComfyUI.
4.  **Flujo en ComfyUI:** ComfyUI ejecuta un workflow predefinido que incluye:
    *   Modelo base (SDXL o Flux).
    *   Un LoRA específico para darle un estilo "Cinemático" o "Ilustración de Storyboard".
    *   (Opcional) ControlNet para mantener consistencia.
5.  **Output:** Las imágenes se guardan en una carpeta. Opcionalmente, se usa FFmpeg o OpenCV en Python para unirlas en un video corto (animática).

## 4. Fases de Desarrollo

### Fase 1: Configuración del Entorno (Día 1)
*   Instalar ComfyUI localmente.
*   Descargar modelos necesarios (SDXL/Flux, un par de LoRAs estilísticos).
*   Crear un entorno virtual de Python (`venv`) e instalar dependencias (`requests`, `openai` o `anthropic`, `python-dotenv`).
*   Inicializar repositorio Git.

### Fase 2: Creación del Workflow en ComfyUI (Día 1-2)
*   Crear un workflow visual en la interfaz de ComfyUI que genere imágenes de alta calidad con un estilo consistente usando LoRAs.
*   Asegurarse de que el workflow funcione bien.
*   Exportar el workflow en formato JSON (formato API de ComfyUI).

### Fase 3: Integración del LLM (Día 2)
*   Escribir el script de Python `llm_director.py`.
*   Diseñar el *prompt* para que el LLM genere un guion estructurado en JSON.
*   Probar la generación de los prompts.

### Fase 4: Orquestación y API de ComfyUI (Día 3)
*   Escribir `comfy_client.py` en Python para conectarse a la API local de ComfyUI (`http://127.0.0.1:8188/prompt`).
*   Modificar dinámicamente el JSON del workflow de ComfyUI desde Python para inyectar los *prompts* generados por el LLM.
*   Descargar las imágenes generadas automáticamente a una carpeta `/output`.

### Fase 5: Extras y Refinamiento (Día 4)
*   **Creación de Video:** Añadir una función en Python que tome las imágenes generadas y cree un `.mp4` tipo presentación con transiciones simples.
*   **Automatización:** Crear un flujo simple en Make o n8n que escuche un correo o formulario y dispare el script de Python.
*   **Documentación:** Escribir un `README.md` excelente **en inglés**, explicando la arquitectura, cómo correrlo y cómo resuelve un problema real en producción audiovisual.

## 5. Estrategia para la Entrevista
*   **Portafolio:** Sube este proyecto a tu GitHub personal con un buen README que incluya GIFs o imágenes de los resultados.
*   **Demostración:** Si te piden mostrar código, puedes explicar cómo usaste Python para automatizar un workflow complejo de ComfyUI que de otro modo sería manual.
*   **Discusión:** Estarás preparado para hablar sobre los retos técnicos de usar ComfyUI *headless*, cómo manejar las alucinaciones del LLM para que los prompts de imagen sean consistentes, y cómo este *pipeline* ahorra horas de trabajo a un equipo de arte conceptual.

## Siguientes Pasos
Si estás de acuerdo con este plan, puedo ayudarte a:
1. Crear la estructura inicial del proyecto y los scripts de Python.
2. Escribir el código para interactuar con la API de Claude o OpenAI.
3. Explicarte cómo exportar y usar el JSON de la API de ComfyUI en Python.
