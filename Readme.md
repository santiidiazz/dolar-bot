 DolarBot — Monitor automático de precios del dólar
Bot en Python que consulta los precios del dólar (blue, oficial, bolsa, etc.)
y envía un reporte diario por email con tabla HTML y archivo Excel adjunto.
¿Qué hace?

Obtiene precios actualizados desde la API pública de dolarito.ar
Genera un Excel con formato prolijo y colores según tipo de cambio
Envía email HTML con tabla de precios y alertas si el blue sube mucho
Guarda un historial en CSV para análisis posterior
Se puede programar para correr solo todos los días a las 9 AM

Casos de Uso
* **Ahorro de tiempo:** Elimina la necesidad de revisar portales financieros manualmente cada mañana.
* **Toma de decisiones:** Alertas inmediatas al celular/correo cuando el mercado presenta variaciones bruscas.
* **Registro contable:** El archivo Excel adjunto sirve como registro histórico para equipos de administración.


Estructura del proyecto
dolar_bot/
├── scraper.py        ← punto de entrada principal
├── excel_report.py   ← genera el archivo .xlsx
├── email_sender.py   ← arma y envía el email
├── scheduler.py      ← corre el bot diariamente
├── requirements.txt
└── .env              ← tus credenciales (no subir a GitHub)
Instalación
bashgit clone https://github.com/santiidiazz/dolar-bot
cd dolar-bot
pip install -r requirements.txt
Configuración
Creá un archivo .env con tus datos:
EMAIL_ORIGEN=tu_email@gmail.com
EMAIL_DESTINO=destinatario@gmail.com
EMAIL_PASS=xxxx xxxx xxxx xxxx

La contraseña es una contraseña de aplicación de Google, no tu password normal.
Creala en: myaccount.google.com → Seguridad → Contraseñas de aplicación

Uso
Correr una vez manualmente:
bashpython scraper.py
Programar para correr todos los días a las 9 AM:
bashpython scheduler.py
Tecnologías usadas

requests — llamadas HTTP a la API
pandas — procesamiento de datos
openpyxl — generación del Excel con formato
smtplib — envío de email via Gmail
schedule — automatización de la tarea diaria
python-dotenv — manejo seguro de credenciales