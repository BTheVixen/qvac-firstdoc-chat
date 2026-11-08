# Project Architecture & Troubleshooting
- This app uses Llama 3.2 1B Instruct (Q4_0) via the tetherto-qvac-sdk Python client.
- Documents inside the docs/ folder are split into paragraphs and ranked by keyword overlap before being passed to the local LLM.
- On Windows machines with Intel integrated graphics, set GGML_VK_DISABLE=1 to run smoothly on CPU.