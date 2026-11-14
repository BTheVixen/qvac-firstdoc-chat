# QVAC Offline Document Chat (`qvac-firstdoc-chat`)

A private, 100% offline **Chat with Your Documents** CLI application built with the Python **QVAC SDK** (`tetherto-qvac-sdk`) and **Llama 3.2 1B Instruct (Q4_0)**.

All document indexing and LLM inference run locally on-device—no cloud APIs or internet connection are required once the model weights are cached.

## Features

* **100% Offline Inference:** Queries local `.txt` and `.md` files inside `docs/` completely offline.
* **Grounded Answers with Citations:** Retrieves the top matching document sections using lightweight keyword overlap and instructs the model to cite source filenames.
* **Zero Extra Embedding Models:** Reuses a single local model (`LLAMA_3_2_1B_INST_Q4_0`) for fast startup and low memory footprint.

## Machine & Software Versions

* **OS:** `Windows-11-10.0.26300-SP0`
* **CPU / GPU:** `Intel64 Family 6 Model 142 Stepping 10, GenuineIntel` / `Intel(R) UHD Graphics 620`
* **Python:** `3.15.2`
* **Python QVAC SDK (`tetherto-qvac-sdk`):** `0.23.0`
* **Bare Worker Runtime (`@qvac/sdk`):** `0.22.0`
* **Local Model:** `LLAMA_3_2_1B_INST_Q4_0`

## Prerequisites

* Python 3.11+
* Node.js & npm (for the `@qvac/sdk@0.22.0` Bare worker runtime)

## Setup & Installation

1 **Clone the repository and create a virtual environment:**
   ```powershell
   git clone https://github.com/BTheVixen/qvac-firstdoc-chat.git
   cd qvac-firstdoc-chat
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2 **Install Python and QVAC worker dependencies:**
   ```powershell
   pip install -r requirements.txt
   npm install -g @qvac/sdk@0.22.0
   ```

3 **Configure environment variables (Windows PowerShell):**
   ```powershell
   $env:QVAC_SDK_DIR = "$(npm root -g)\@qvac\sdk"
   # Optional: Disable Vulkan on Windows systems with Intel integrated graphics to run on CPU
   $env:GGML_VK_DISABLE = "1"
   ```

## Usage

1 Place any `.txt` or `.md` files you want to query inside the `docs/` folder (sample notes are included).
2 Run the application:
   ```powershell
   python chat_app.py
   ```
3 To verify offline functionality, turn off Wi-Fi after the initial model download completes and ask questions about your files. Type `exit` to quit.

## Offline Test Verification (Wi-Fi Off)

Tested with Wi-Fi disconnected (`Airplane Mode` / Wi-Fi off) to verify 100% local QVAC execution:

```text
You (Wi-Fi Off): How does this app fix Vulkan issues on Windows?
Assistant:  [Source: architecture.md]

According to the provided architecture.md file, the app fixes Vulkan issues on Windows by disabling a configuration option called GGML_VK_DISABLE=1. This means that the app does not attempt to use Intel integrated graphics, which can cause Vulkan issues on Windows machines with such hardware.
```

## Hallucination Protection & Grounding

* **Context-Only Prompting:** The system prompt strictly instructs `LLAMA_3_2_1B_INST_Q4_0` to answer *only* using the retrieved text chunks from `docs/` and to refuse to guess when information is missing.
* **Source Filename Citations:** Every retrieved chunk includes its source filename so the model cites where each fact came from.
* **Deterministic Keyword Retrieval:** Relevant document sections are matched locally before generation, preventing the 1B model from fabricating answers outside the provided files.

```text
You (Wi-Fi Off): What is the weather in Johannesburg today?
Assistant: I'm not able to find the answer to the question "What is the weather in Johannesburg today?" in the provided context.
```
