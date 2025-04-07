import gradio as gr
import ollama
import os

# Define avatars for user and assistant
USER_AVATAR = "😎"
BOT_AVATAR = "🤖"

# Get available models
list_of_llms = [model.model for model in ollama.list().models]
list_of_llms.insert(0, "ollama models")

def update_model_display(model_name):
    """Returns text to display selected model or None if no selection"""
    return f"You selected: {model_name}" if model_name else None

with gr.Blocks(title="Dual Model Chat") as demo:
    banner_path = "./static/banner.png"
    if os.path.exists(banner_path):
        gr.Image(value=banner_path, scale=1, show_label=False, container=False, height=50)
    else:
        gr.HTML("<div style='width: 100%; background-color: #f0f0f0; padding: 20px; text-align: center; border-radius: 5px;'>Placeholder for Banner (static/banner.jpg not found)</div>")

    with gr.Row():
        # Column A
        with gr.Column(scale=1):
            with gr.Row():
                # Icon and dropdown in same row
                if os.path.exists("./static/logo_A.jpg"):
                    gr.Image(value="./static/logo_A.jpg", width=100, height=150, show_label=False)
                else:
                    gr.HTML("""<div style="width:100px;height:100px;background:#f5f5f5;
                                        display:flex;justify-content:center;align-items:center;
                                        border-radius:8px;border:1px solid #ddd;">Icon A</div>""")

                with gr.Column():  # New column to keep dropdown and text together
                    dropdown_a = gr.Dropdown(
                        list_of_llms,
                        label="Select your 1st Model",
                        interactive=True
                    )
                    # Model selection display text
                    model_display_a = gr.Textbox(
                        value=None,
                        label=None,
                        interactive=False,
                        show_label=False,
                        visible=False
                    )

            # Update display when dropdown changes
            dropdown_a.change(
                fn=update_model_display,
                inputs=dropdown_a,
                outputs=model_display_a
            ).then(
                lambda x: gr.update(visible=x is not None),
                inputs=model_display_a,
                outputs=model_display_a
            )

            chatbot_a = gr.Chatbot(height=400)

        # Column B
        with gr.Column(scale=1):
            with gr.Row():
                with gr.Column():  # New column to keep dropdown and text together
                    dropdown_b = gr.Dropdown(
                        list_of_llms,
                        label="Select your 2nd Model",
                        interactive=True
                    )
                    # Model selection display text
                    model_display_b = gr.Textbox(
                        value=None,
                        label=None,
                        interactive=False,
                        show_label=False,
                        visible=False
                    )

                if os.path.exists("./static/logo_B.jpg"):
                    gr.Image(value="./static/logo_B.jpg", width=100, height=150, show_label=False)
                else:
                    gr.HTML("""<div style="width:100px;height:100px;background:#f5f5f5;
                                        display:flex;justify-content:center;align-items:center;
                                        border-radius:8px;border:1px solid #ddd;">Icon B</div>""")

            # Update display when dropdown changes
            dropdown_b.change(
                fn=update_model_display,
                inputs=dropdown_b,
                outputs=model_display_b
            ).then(
                lambda x: gr.update(visible=x is not None),
                inputs=model_display_b,
                outputs=model_display_b
            )

            chatbot_b = gr.Chatbot(height=400)

    with gr.Row():
        msg = gr.Textbox(
            label="Type your message",
            placeholder="Enter message here...",
            container=False,
            elem_classes=["blue-input"]
        )

    # Chat functions
    def respond_a(message, history, model):
        if not model or model == "ollama models":
            return "", history + [(f"{USER_AVATAR} {message}", f"{BOT_AVATAR} Please select a model first")]

        try:
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": message}],
                stream=False
            )
            bot_response = response['message']['content']
            # Add avatars to messages
            return "", history + [(f"{USER_AVATAR} {message}", f"{BOT_AVATAR} {bot_response}")]
        except Exception as e:
            return "", history + [(f"{USER_AVATAR} {message}", f"{BOT_AVATAR} Error: {str(e)}")]

    def respond_b(message, history, model):
        if not model or model == "ollama models":
            return "", history + [(f"{USER_AVATAR} {message}", f"{BOT_AVATAR} Please select a model first")]

        try:
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": message}],
                stream=False
            )
            bot_response = response['message']['content']
            # Add avatars to messages
            return "", history + [(f"{USER_AVATAR} {message}", f"{BOT_AVATAR} {bot_response}")]
        except Exception as e:
            return "", history + [(f"{USER_AVATAR} {message}", f"{BOT_AVATAR} Error: {str(e)}")]

    msg.submit(respond_a, [msg, chatbot_a, dropdown_a], [msg, chatbot_a])
    msg.submit(respond_b, [msg, chatbot_b, dropdown_b], [msg, chatbot_b])

    # Custom CSS
    demo.css = """
    body {
        display: flex;
        flex-direction: column;
        min-height: 100vh; /* Ensure the body takes at least the full viewport height */
    }
    #component-1 { /* Target the Row containing the banner */
        margin-bottom: 0 !important; /* Remove default bottom margin */
    }
    #component-2 { /* Target the Row containing the columns */
        flex-grow: 1; /* Make the row of columns take up remaining vertical space */
        display: flex; /* Enable flexbox for the columns within the row */
    }
    #component-2 > div { /* Target the individual columns */
        display: flex;
        flex-direction: column;
    }
    #component-3 { /* Target the Row containing the textbox */
        margin-top: 0 !important; /* Remove top margin */
        margin-bottom: 0 !important; /* Remove bottom margin */
    }
    .blue-input input {
        background-color: #e0f2f7 !important;
        border: 2px solid #1e88e5 !important;
    }
    .textbox {
        padding: 0 !important;
        margin-top: -15px !important;
        border: none !important;
        box-shadow: none !important;
    }
    .textbox textarea {
        font-size: 0.9em !important;
        color: #666 !important;
        background: transparent !important;
    }
    """

demo.launch()