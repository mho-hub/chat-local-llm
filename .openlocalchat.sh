#!/bin/bash

# Count the number of running "ollama" processes
ollama_process=$(pgrep ollama | wc -l)

# Check if no "ollama" processes are running
if [ "$ollama_process" -eq 0 ]; then
#	echo "Starting Ollama Server..."
	ollama serve
fi

ps -ef | grep streamlit | awk '{print$2}' | xargs kill -9

cd ~/_D_E_V_/Projects/chat-local-llm/

source .venv_a_/bin/activate

streamlit run run_app.py


