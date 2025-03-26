# chat-local-llm
## STREAMLIT application

### Access locally downloaded models using Ollama

#### This app displays:
- a side panel with 
  - a select box to choose from a list of local models (`ollama call`). 
  - a clear button for the chat history (`shelve`) of the selected model.
- a central panel with a chat input field
  - the panel opens after the selected model is selected and displayed
  - chat history is displayed

#### Requirements:
- Python 3.8 or higher
- Ollama installed locally
- Streamlit installed (`pip install streamlit`)
- Models downloaded and available in Ollama (`ollama list`)

#### How to run

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run main.py`

#### Features

- **Model Selection**: Users can select from a list of locally downloaded models.
- **Chat Interface**: A chat interface is provided for interacting with the selected model.
- **Clear Chat History**: Users can clear the chat history for the selected model.

### Notes:
- see screenshot