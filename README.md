
# 🍬 Sugar Commodity AI Chatbot

An intelligent AI-powered chatbot for analysing sugar commodity procurement data using Google Gemini AI.

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/a34e2090-98c2-4c30-9769-e2d3e4d479d0" />

---

## 📋 What You Need

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Google Gemini API Key** (Free) - [Get Key](https://aistudio.google.com/apikey)

---

## 🚀 Quick Start (2 Steps)

### Step 1: Clone the Repository

```
git clone https://github.com/YSULTRA/AI_Chatbot_Kearney_YashSingh.git
cd AI_Chatbot_Kearney_YashSingh
```

### Step 2: Run the Setup Script ( If Script Fails use the manual steps given below )

```
python start.py
```

The script will automatically:
- ✅ Create virtual environment
- ✅ Install all backend dependencies
- ✅ Install all frontend dependencies
- ✅ Ask for your API key (one time)
- ✅ Start both servers

**Get your free API key:** https://aistudio.google.com/apikey

<img width="1136" height="818" alt="image" src="https://github.com/user-attachments/assets/cc2f53a0-188a-42c8-82bf-0dc19a7dc37c" />

<img width="1800" height="1009" alt="image" src="https://github.com/user-attachments/assets/5aeaf368-113e-4704-8cb8-4ccb317a4300" />

<img width="1713" height="771" alt="image" src="https://github.com/user-attachments/assets/4e5e2aac-f53e-47af-a4a9-016521a16ce6" />





## 📝 Manual Setup
```
cd .\AI_Chatbot_Kearney_YashSingh\
```

### Start Backend in Terminal 
```
cd chatbot-backend
python -m venv env
env\Scripts\activate          # Windows
source env/bin/activate       # Mac/Linux
pip install -r .\requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Start Frontend in Other Terminal
```
cd chatbot-frontend
npm install
npm run dev
```

### Access Points
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
---

## 🌐 Access the Application

Once running, open your browser:

- **🎨 Main Interface:** http://localhost:3000
- **📚 API Documentation:** http://localhost:8000/docs
- **🔧 Backend API:** http://localhost:8000


---

## 💬 Try These Questions

Test the chatbot with sample questions:

1. "Which supplier provides the cheapest sugar per kg?"
2. "What's the total spend on all commodities?"
3. "List all sugars starting with 'B'"
4. "Show me the most expensive commodity"
5. "Compare prices between different sugar types"



---

## 📸 Screenshots

### Main Chat Interface
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/3aa832aa-4031-4df4-bfcd-04f5a3d216a6" />

### Interactive API Documentation
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/663cd16b-a04b-42ed-bd9b-9c75b3142357" />

---



## 📁 Project Structure

```
AI_Chatbot_Kearney_YashSingh/
│
├── chatbot-backend/              # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── rag_pipeline.py      # RAG implementation
│   │   ├── data_processor.py    # Data processing
│   │   └── models.py            # Data models
│   ├── data/
│   │   └── Sugar_Spend_Data.csv # Sample data
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # API key (YOU CREATE THIS)
│
├── chatbot-frontend/            # Next.js React Frontend
│   ├── app/
│   │   ├── page.tsx            # Main chat interface
│   │   ├── layout.tsx          # App layout
│   │   └── globals.css         # Styles
│   ├── components/
│   │   ├── ChatMessage.tsx     # Message bubbles
│   │   ├── ChatInput.tsx       # Input box
│   │   └── StatsPanel.tsx      # Statistics cards
│   ├── lib/
│   │   └── api.ts              # API client
│   └── package.json            # Node dependencies
│
├── screenshots/                 # Demo images
├── start.py                    # Universal launcher script
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

---

## ✨ Features

- 🤖 Powered by Google Gemini 2.0 Flash
- 📊 Live commodity statistics
- 🔍 RAG pipeline with ChromaDB
- 💬 Ask questions in plain English
- 🎨 Beautiful, responsive interface
- 📈 Intelligent spend analysis
- 🌐 Access from any device

---

## 🛠️ Tech Stack

### Backend
- **Python 3.9** - Programming language
- **FastAPI** - Modern web framework
- **Google Gemini AI** - LLM for responses
- **ChromaDB** - Vector database
- **Sentence Transformers** - Text embeddings

### Frontend
- **Next.js 15** - React framework
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations

---

## 🎯 Use Cases

1. **Supplier Analysis** - Find the most cost-effective suppliers
2. **Spend Optimization** - Identify areas to reduce costs
3. **Price Comparison** - Compare commodity prices across suppliers
4. **Data Exploration** - Ask natural language questions about your data
5. **Quick Insights** - Get instant answers without Excel analysis

---

## 📧 Support & Contact

**Created by:** Yash Singh  
**Project:** AI Engineering Internship - Kearney  


---



```

