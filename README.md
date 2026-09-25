# 🎬 AI Storyboard & Animatic Pipeline

*[🇪🇸 Leer esta documentación en Español](README.es.md)*

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![Generative AI](https://img.shields.io/badge/AI-Azure%20OpenAI%20%7C%20ComfyUI-purple)

## 📌 Overview
This repository contains an **Automated Storyboard & Animatic Pipeline**, designed to demonstrate advanced integration of Large Language Models (LLMs) with generative image and video workflows. 

The pipeline acts as an autonomous AI Movie Director. It takes a raw text idea, uses a structured LLM agent to break it down into cinematic scenes, and programmatically orchestrates a headless **ComfyUI** instance (deployed on a serverless GPU cloud via Modal) to render the storyboard frames. 

Finally, it exposes a Webhook (Flask API) that can be triggered by automation tools like **n8n** or Make, creating a fully autonomous Generative AI workflow suitable for creative studios and audiovisual production teams.

---

## 🏗️ System Architecture

Below is the architecture diagram. The flow illustrates how information travels from the moment the user sends an idea until the final video is rendered in the cloud.

```mermaid
graph TD
    %% Node Definitions
    Start([🚀 Start: n8n Webhook])
    API[💻 api.py / main_pipeline.py<br/>Local Orchestrator]
    LLM{🧠 Azure OpenAI API<br/>gpt-5-mini Model}
    Modal[☁️ Modal Serverless GPU<br/>comfy_backend.py]
    ComfyUI[[🎨 ComfyUI Headless<br/>Image Generation]]
    SDXL[(📦 SDXL & LoRAs<br/>AI Models)]
    Video[🎞️ video_generator.py<br/>Post-Production]
    End([✅ Final Animatic Video])

    %% Data Flow
    Start -->|1. Sends Text Idea| API
    
    %% Lengthen connection and simplify text to prevent overlapping 2 and 3
    API --->|2. Injects System Prompt| LLM
    LLM --->|3. Returns Structured JSON| API
    
    API -->|4. Injects JSON into workflow_api.json| Modal
    Modal -->|5. Spins up GPU & Container| ComfyUI
    ComfyUI <-->|6. Loads Models| SDXL
    ComfyUI -->|7. Returns Generated Images| API
    API -->|8. Executes OpenCV script| Video
    Video -->|9. Stitches images into MP4| End

    %% Node Styles for high contrast on GitHub
    style Start fill:#238636,stroke:#2ea043,stroke-width:2px,color:#ffffff
    style API fill:#1f6feb,stroke:#388bfd,stroke-width:2px,color:#ffffff
    style LLM fill:#8957e5,stroke:#d2a8ff,stroke-width:2px,color:#ffffff
    style Modal fill:#db61a2,stroke:#ff7b72,stroke-width:2px,color:#ffffff
    style ComfyUI fill:#d29922,stroke:#e3b341,stroke-width:2px,color:#ffffff
    style SDXL fill:#21262d,stroke:#8b949e,stroke-width:2px,color:#c9d1d9
    style Video fill:#1f6feb,stroke:#388bfd,stroke-width:2px,color:#ffffff
    style End fill:#238636,stroke:#2ea043,stroke-width:2px,color:#ffffff
```

### Detailed Component Description:

1. **LLM Director (`llm_director.py`)**: 
   - Uses **Azure OpenAI** alongside Pydantic to guarantee *Structured Outputs*.
   - Transforms a simple user prompt into a strict JSON payload containing specific camera angles, scene descriptions, and highly optimized positive/negative prompts for Stable Diffusion.

2. **ComfyUI Headless Orchestrator (`main_pipeline.py`)**:
   - Reads the standard `workflow_api.json` from ComfyUI.
   - Dynamically modifies the node graph, injecting the LLM-generated prompts into the precise CLIPTextEncode nodes.
   - Simulates dispatching the compute job to a cloud GPU cluster.

3. **Cloud Backend (`comfy_backend.py`)**:
   - Infrastructure as Code (IaC) using **Modal**.
   - Spins up Linux containers with T4 GPUs on demand, installs PyTorch dependencies, and boots ComfyUI headlessly, ensuring massive scalability and per-second billing.

4. **Automation Endpoint (`api.py` & `n8n_workflow.json`)**:
   - Exposes the entire pipeline via a Flask REST API.
   - Includes an `n8n` workflow template to connect the pipeline to Slack, Email, or internal CRM systems.

5. **Post-Production (`video_generator.py`)**:
   - An OpenCV-backed script that automatically grabs the generated images frame by frame and stitches them into a sequential `.mp4` presentation (Animatic).

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Azure OpenAI API Key (or standard OpenAI/Gemini Key)
- Modal CLI authenticated (`modal token new`)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/fernando-pedernera/ai-storyboard.git
cd ai-storyboard
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install openai pydantic flask requests python-dotenv opencv-python numpy
```

3. Configure environment variables:
Create a `.env` file in the root directory:
```env
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.services.ai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5-mini
API_VERSION=2024-02-15-preview
```

### Usage

**1. Run the CLI Pipeline:**
```bash
python main_pipeline.py
```
*This will execute the agent, generate the JSON payloads, simulate the GPU cloud dispatch, and process the storyboard logic.*

**2. Run the Webhook Server (For n8n):**
```bash
python api.py
```
*This starts a local server on port 5000, ready to receive POST requests from n8n, Make, or Postman.*

**3. Generate the Animatic (Video):**
```bash
python video_generator.py
```
*This script will grab the images generated by ComfyUI and stitch them into a `storyboard_pitch.mp4` file.*

---

## 🎬 Real-World Application
In a real production environment, this pipeline saves hundreds of hours for conceptual artists and directors. By automating the prompt-engineering phase and the ComfyUI rendering phase, a creative studio can generate 10 different visual storyboards for a client pitch in a matter of minutes, simply by sending a Slack message.

## License
MIT License
