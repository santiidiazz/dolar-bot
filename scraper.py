"""
Bot de monitoreo de precios del dólar
Scrapea dolarito.ar y manda un reporte por email con Excel adjunto.
"""

import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
from email_sender import enviar_reporte
from excel_report import generar_excel


API_URL = "https://dolarito.ar/api/v1/todas"

HISTORICO_CSV = Path("historico_dolar.csv")


def obtener_precios() -> dict:
    """Llama a la API pública de dolarito.ar y devuelve los precios."""
    headers = {"User-Agent": "Mozilla/5.0 (DolarBot/1.0)"}
    response = requests.get(API_URL, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()


def parsear_datos(raw: dict) -> list[dict]:
    """Convierte la respuesta de la API a una lista de dicts limpia."""
    tipos_interes = ["blue", "oficial", "bolsa", "contadoconliqui", "mayorista", "cripto"]
    resultado = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")

    for tipo in tipos_interes:
        if tipo in raw:
            info = raw[tipo]
            resultado.append({
                "fecha": fecha_hoy,
                "tipo": tipo.capitalize(),
                "compra": float(info.get("compra", 0)),
                "venta": float(info.get("venta", 0)),
                "variacion": info.get("variacion", "—"),
            })

    return resultado


def guardar_historico(df_nuevo: pd.DataFrame):
    """Acumula registros en el CSV histórico."""
    if HISTORICO_CSV.exists():
        df_hist = pd.read_csv(HISTORICO_CSV)
        df_total = pd.concat([df_hist, df_nuevo], ignore_index=True)
    else:
        df_total = df_nuevo

    df_total.to_csv(HISTORICO_CSV, index=False)
    print(f"  Histórico actualizado: {len(df_total)} registros en {HISTORICO_CSV}")


def detectar_alertas(df: pd.DataFrame) -> list[str]:
    """Genera mensajes de alerta si el blue supera ciertos umbrales."""
    alertas = []
    blue = df[df["tipo"] == "Blue"]
    if not blue.empty:
        venta = blue.iloc[0]["venta"]
        if venta > 1500:
            alertas.append(f"⚠️  Dólar blue superó $1.500 — venta: ${venta:.0f}")
        if venta > 2000:
            alertas.append(f"🚨 Dólar blue superó $2.000 — venta: ${venta:.0f}")
    return alertas


def main():
    print("=" * 50)
    print(f"  DolarBot arrancando — {datetime.now():%d/%m/%Y %H:%M}")
    print("=" * 50)

    # 1. Obtener datos
    print("\n[1/4] Scrapeando dolarito.ar...")
    raw = obtener_precios()
    datos = parsear_datos(raw)
    df = pd.DataFrame(datos)
    print(f"  OK — {len(df)} tipos de cambio obtenidos")

    # 2. Mostrar en consola
    print("\n[2/4] Precios actuales:")
    print(df.to_string(index=False))

    # 3. Guardar histórico
    print("\n[3/4] Guardando histórico...")
    guardar_historico(df)

    # 4. Generar Excel y enviar email
    print("\n[4/4] Generando reporte y enviando email...")
    alertas = detectar_alertas(df)
    excel_path = generar_excel(df, alertas)
    enviar_reporte(df, alertas, excel_path)

    print("\n Listo!")


if __name__ == "__main__":
    main()