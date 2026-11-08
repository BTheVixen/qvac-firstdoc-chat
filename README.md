# QVAC Offline Document Chat (`qvac-firstdoc-chat`)

A private, 100% offline **Chat with Your Documents** CLI application built with the Python **QVAC SDK** (`tetherto-qvac-sdk`) and **Llama 3.2 1B Instruct (Q4_0)**.

All document indexing and LLM inference run locally on-device—no cloud APIs or internet connection are required once the model weights are cached.

## Features
- **100% Offline Inference:** Queries local `.txt` and `.md` files inside `docs/` completely offline.
- **Grounded Answers with Citations:** Retrieves the top matching document sections using lightweight keyword overlap and instructs the model to cite source filenames.
- **Zero Extra Embedding Models:** Reuses a single local model (`LLAMA_3_2_1B_INST_Q4_0`) for fast startup and low memory footprint.

## Prerequisites
- Python 3.11+
- Node.js & npm (for the `@qvac/sdk@0.22.0` Bare worker runtime)

## Setup & Installation

1. **Clone the repository and create a virtual environment:**
   ```powershell
   git clone <your-public-repo-url>
   cd qvac-firstdoc-chat
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install Python and QVAC worker dependencies:**
   ```powershell
   pip install -r requirements.txt
   npm install -g @qvac/sdk@0.22.0
   ```

3. **Configure environment variables (Windows PowerShell):**
   ```powershell
   \(env:QVAC_SDK_DIR = "\)(npm root -g)\@qvac\sdk"
   # Required on Windows systems with Intel integrated graphics to run on CPU:
   \$env:GGML_VK_DISABLE = "1"
   ```

## Usage

1. Place any `.txt` or `.md` files you want to query inside the `docs/` folder (sample notes are included).
2. Run the application:
   ```powershell
   python chat_app.py
   ```
3. To verify offline functionality, disconnect from Wi-Fi after the initial model download completes and ask questions about your files. Type `exit` to quit.