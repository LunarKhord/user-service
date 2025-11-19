# User-Service






## 🧱 Architecture System Design Diagram
[Placeholder]

## ⚙️ **Installation & Setup**

### **1. Clone the Repository**

```bash
git clone https://github.com/LunarKhord/user-service.git
cd user-service
```

### **2. Create and Activate a Virtual Environment**

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\Activate.ps1 # Windows (PowerShell)
```


### **3. Install uv**

```bash
pip install uv
```

### **3. Install Dependencies**

```bash
uv sync
```


### **5. Run the Development Server**

```bash
uvicorn main:app --reload
```

Visit API Docs:

```
http://127.0.0.1:8000/docs
```

### **6. Run Tests**

```bash
pytest
```
