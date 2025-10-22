@echo off
title Backend - Sugar Commodity AI Chatbot
cd /d "C:\Users\YASH SINGH\AI_Chatbot_Kearney\chatbot-backend"
"C:\Users\YASH SINGH\AI_Chatbot_Kearney\chatbot-backend\env\Scripts\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause