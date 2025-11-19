# User-Service






## 🧱 Architecture

user-service/
│
├── main.py                 # FastAPI entrypoint
├── pyproject.toml        # Project dependencies
│
├── app/
│   ├── config/              # Database setup and configuration
│   ├── models/              # Database models including Pydantic v2 schemas 
│   ├── controllers/         # Business logic
│   └── utils/               # Helpers
│
└── tests/
    └── test_health.py       # Pytest suite for basic endpoint checks



## ⚙️ **Installation & Setup**

### **1. Clone the Repository**

```bash
git clone https://github.com/[]
cd []
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