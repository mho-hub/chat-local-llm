# TALK TO 2 MODELS with 1 PROMPT
## Gradio application

### Access locally downloaded models using Ollama

#### This app displays:
- A banner at the top
- Two columns, each with 
  - a select box (gr.Dropdown) at the top to choose from a list of local models (`ollama call`). 
  - a panel with a chat area
- An input box (gr.Textbox) to talk to the selected models

- You enter a prompt and it will processed by two different (I you want) LLMs simultaneously.


#### Requirements:
- Python 3.8 or higher
- Ollama installed locally
- Gradio installed (`pip install gradio`)
- Models downloaded and available in Ollama (`ollama list`)
  e. g. You can download two little small LLMs for testing purposes with:
  `ollama run qwen2.5:1.5b`
  `ollama deepseek-r1:1.5b`

#### How to run

1. Clone the repository
2. Create a virtual environment for this application:
	`python -m venv .venv_b_`
	`source .venv2models/bin/activate`  # Linux/Mac
3. Install dependencies: 
    `pip install -r requirements.txt`
    `pip install --upgrade pip`
4. Run the app: `python main.py`

#### Features

- **Model Selection**: Users can select from two separate lists of locally downloaded models.
- **Dual side-to-side-Chat Interface**: A chat interface is provided for interacting with the selected models and comparing the responses

### Notes:
- see screenshot_b.jpg