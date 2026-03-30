import os
import schedule
import time
from dotenv import load_dotenv
from graph import app  # Importing the compiled LangGraph app

load_dotenv()

def run_agent_job():
    print("\n--- 🚀 Iniciando flujo del Agente Community Manager ---")
    try:
        # Trigger the graph. The input is just a kick-off signal.
        result = app.invoke({"messages": [], "status": "start"})
        print("--- ✅ Flujo completado ---")
        print(f"Estado final: {result.get('status')}")
    except Exception as e:
        print(f"--- ❌ Error critico en el agente: {e}")

# Scheduler: Run twice a day (e.g., 10:00 AM and 6:00 PM)
# For testing purposes, you can uncomment the direct call below.
schedule.every().day.at("10:00").do(run_agent_job)
schedule.every().day.at("18:00").do(run_agent_job)

if __name__ == "__main__":
    print("🤖 Agent Community Manager (LangGraph) Iniciado.")
    print("📅 Esperando a la hora programada (10:00 y 18:00)...")
    
    # Run immediately for verification (Comment out in production)
    run_agent_job()
    
    while True:
        schedule.run_pending()
        time.sleep(60)
