# 🧠 Multi-Agent ETL Copilot (Google ADK)

A fully automated schema mapping, ETL code generation, validation, and documentation system built using **Google’s Agent Development Kit (ADK)**.  

This project transforms ANY tabular dataset into a standardized target schema using a multi-agent workflow.  
It automates schema extraction, mapping, code generation, validation, and documentation.

---

## 🚀 Key Capabilities

✔ Automatic schema extraction  
✔ Source → target mapping (direct, derived, missing)  
✔ ETL code generation (pandas)  
✔ Static validation of transformation logic  
✔ Pipeline documentation generation  
✔ Multi-agent orchestration  
✔ Generic design — works with ANY dataset  

---

## 🏗 Architecture Overview

The system uses five main agents:

```
SchemaAgent
  → MappingAgent
      → TransformAgent
          → ValidationAgent
              → DocumentationAgent
```

The orchestrator ensures clean stateful execution between agents.

---

## 📂 Repository Structure

```
multi-agent-etl-copilot/
│
├── notebooks/
│   └── etl_copilot.ipynb
│
├── src/
│   ├── schema_agent.py
│   ├── mapping_agent.py
│   ├── transform_agent.py
│   ├── validation_agent.py
│   ├── documentation_agent.py
│   └── orchestrator.py
│
├── docs/
│   ├── architecture_diagram.png
│   └── final_documentation.md
│
└── README.md
```

---

## 🧩 Components

### **SchemaAgent**
Extracts column names + inferred datatypes → LLM-friendly schema.

### **MappingAgent**
Maps source → target columns. Flags:
- direct mappings  
- derived mappings  
- missing fields  

### **TransformAgent**
Generates runnable pandas ETL code using mapping output.

### **ValidationAgent**
Static analysis of ETL code to detect:
- missing columns  
- suspicious logic  
- hallucinated field names  

### **DocumentationAgent**
Outputs a complete Markdown-style documentation file:
- Schema summary  
- Mapping table  
- Transformation code  
- Data dictionary  
- Validation summary  

---

## ▶️ Running the Pipeline

```python
from orchestrator import run_pipeline

result = run_pipeline("sample_data/input.csv")
print(result["mapping"])
print(result["transformation_code"])
print(result["validation"])
print(result["documentation"])
```

---

## 🧪 Requirements

```
pip install google-genai
pip install google-adk
pip install pandas
```

---

## 🎯 Capstone Submission
This project was created for the:

**Google × Kaggle Agents Intensive Capstone Project (2025)**  
Submission includes:
- Multi-agent workflow  
- Tools  
- Context engineering  
- Observability  
- A2A communication  
- Documentation  

---

## 📄 License  
MIT License (optional)
