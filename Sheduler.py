import schedule
import time
from scraper import main
 
 
def job():
    try:
        main()
    except Exception as e:
        print(f"Error en el bot: {e}")
 
 
schedule.every().day.at("09:00").do(job)
 
print("Scheduler corriendo. Bot programado para las 9:00 AM todos los días.")
print("Presioná Ctrl+C para detenerlo.\n")
 
while True:
    schedule.run_pending()
    time.sleep(60)