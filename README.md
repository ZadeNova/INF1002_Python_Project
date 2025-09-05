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
    ```
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    Launch the Streamlit app locally.
    ```
    streamlit run app.py
    ```
    The app will open in your default web browser at `http://localhost:8501`.

## 📁 Project Structure













## 🪵 GitHub Branch Workflow Guide: Avoiding Collisions

To work together without overwriting each other's code, we **must** use a branching workflow. This guide explains how to do it.

### **The Golden Rule: Never Push Directly to `main`**
The `main` branch is our stable, working version. To keep it safe, we will all do our work in separate **feature branches** and then merge them via **Pull Requests (PRs)**.

### **Standard Workflow For Adding a Feature**

#### 1. Get the Latest Code
*Always* start from the latest `main` branch.
```
git checkout main
git pull origin main
```

### 2. Create your Feature Branch
```
# Create and switch to a new branch
git checkout -b feature/your-feature-name
```

### 3. Do your Work
Code your feature, write tests, and make sure it works. Commit your changes to your branch.
```bash
# Stage your changes
git add .

# Commit with a clear message
git commit -m "feat: add calculate_sma function with tests"
```
### 4. Push your feature to Github

Upload your branch to the shared repository.
```
git push -u origin feature/your-feature-name
```



