"""
Envía el reporte por email con cuerpo HTML y Excel adjunto.
Configurá tus credenciales en el archivo .env
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

EMAIL_ORIGEN  = os.getenv("EMAIL_ORIGEN")   # tu Gmail
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")  # destinatario
EMAIL_PASS    = os.getenv("EMAIL_PASS")     # contraseña de aplicación de Google


def _construir_tabla_html(df: pd.DataFrame) -> str:
    """Convierte el DataFrame en una tabla HTML con estilo inline."""
    filas = ""
    for _, row in df.iterrows():
        spread = row["venta"] - row["compra"]
        color  = "#fff0f0" if row["tipo"] == "Blue" else "#ffffff"
        filas += f"""
        <tr style="background:{color}">
          <td style="{TD}">{row['tipo']}</td>
          <td style="{TD}">${row['compra']:,.2f}</td>
          <td style="{TD}">${row['venta']:,.2f}</td>
          <td style="{TD}">${spread:,.2f}</td>
          <td style="{TD}">{row['variacion']}</td>
        </tr>"""
    return filas

TH = "padding:8px 12px;background:#1F4E79;color:#fff;font-family:Arial,sans-serif;font-size:13px;"
TD = "padding:7px 12px;font-family:Arial,sans-serif;font-size:13px;border-bottom:1px solid #eee;"


def _html_body(df: pd.DataFrame, alertas: list[str]) -> str:
    filas  = _construir_tabla_html(df)
    alerta_html = ""
    if alertas:
        items = "".join(f"<li>{a}</li>" for a in alertas)
        alerta_html = f"""
        <div style="background:#FFE0E0;border-left:4px solid #C00;padding:10px 16px;margin-bottom:16px;border-radius:4px">
          <strong style="font-family:Arial;color:#900">⚠️ Alertas:</strong>
          <ul style="font-family:Arial;font-size:13px;margin:4px 0 0 16px">{items}</ul>
        </div>"""

    return f"""
    <html><body style="font-family:Arial,sans-serif;padding:24px;color:#333">
      <h2 style="color:#1F4E79">Reporte Dólar — {datetime.now():%d/%m/%Y %H:%M}</h2>
      {alerta_html}
      <table cellspacing="0" cellpadding="0" style="border-collapse:collapse;width:100%;max-width:520px">
        <tr>
          <th style="{TH}">Tipo</th>
          <th style="{TH}">Compra</th>
          <th style="{TH}">Venta</th>
          <th style="{TH}">Spread</th>
          <th style="{TH}">Variación</th>
        </tr>
        {filas}
      </table>
      <p style="font-size:12px;color:#888;margin-top:20px">
        Generado automáticamente por DolarBot · Fuente: dolarito.ar
      </p>
    </body></html>"""


def enviar_reporte(df: pd.DataFrame, alertas: list[str], excel_path: Path):
    """Arma el email y lo envía via Gmail SMTP."""
    if not all([EMAIL_ORIGEN, EMAIL_DESTINO, EMAIL_PASS]):
        print("  ⚠️  EMAIL_ORIGEN / EMAIL_DESTINO / EMAIL_PASS no están en .env — email omitido")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f" Dólar hoy {datetime.now():%d/%m/%Y} — reporte automático"
    msg["From"]    = EMAIL_ORIGEN
    msg["To"]      = EMAIL_DESTINO

    msg.attach(MIMEText(_html_body(df, alertas), "html"))

    # Adjuntar Excel
    with open(excel_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{excel_path.name}"')
    msg.attach(part)

    # Enviar
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ORIGEN, EMAIL_PASS)
        server.sendmail(EMAIL_ORIGEN, EMAIL_DESTINO, msg.as_string())
    print(f"  Email enviado a {EMAIL_DESTINO}")