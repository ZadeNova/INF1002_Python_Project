## 🚀 Getting Started (For Developers)

Follow these steps to set up the development environment on your local machine.

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    cd your-repo-name
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows (Command Prompt)
    python -m venv venv
    venv\Scripts\activate.bat

    # On Windows (PowerShell)
    python -m venv venv
    venv\Scripts\Activate.ps1
    ```
    *You should see `(venv)` in your terminal prompt.*

3.  **Install Dependencies**
    Install all required libraries from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    Launch the Streamlit app locally.
    ```bash
    streamlit run app.py
    ```
    The app will open in your default web browser at `http://localhost:8501`.

## 📁 Project Structure
