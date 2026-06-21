#!/usr/bin/env python3
"""send_report.py — envia por email el ultimo resumen generado por monitor.py.

Usa SMTP con variables de entorno: SMTP_USER, SMTP_PASS, REPORT_TO
(opcionales: SMTP_HOST, SMTP_PORT). Si NO estan configuradas, escribe el
reporte en consola y termina sin error (no falla el workflow).
"""
import os
import sys
import ssl
import smtplib
import datetime
from email.mime.text import MIMEText

HERE = os.path.dirname(os.path.abspath(__file__))
RESUMEN = os.path.join(HERE, "data", "ultimo-resumen.txt")


def load_body():
    if os.path.exists(RESUMEN):
        with open(RESUMEN, encoding="utf-8") as f:
            return f.read()
    return "No se encontro data/ultimo-resumen.txt. ¿Corriste monitor.py primero?"


def main():
    body = load_body()
    user = os.environ.get("SMTP_USER")
    pw = os.environ.get("SMTP_PASS")
    to = os.environ.get("REPORT_TO")
    # OJO GitHub Actions: un secret no definido llega como "" (string vacío), NO ausente.
    # Por eso el chequeo va ANTES de parsear el puerto (int("") reventaría).
    if not (user and pw and to):
        print("[send_report] SMTP no configurado "
              "(faltan SMTP_USER / SMTP_PASS / REPORT_TO).")
        print("[send_report] Reporte por consola:\n")
        print(body)
        return 0

    host = os.environ.get("SMTP_HOST") or "smtp.gmail.com"
    try:
        port = int(os.environ.get("SMTP_PORT") or "465")
    except ValueError:
        port = 465

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "Meniw Reputation Autopilot — %s" % datetime.date.today().isoformat()
    msg["From"] = user
    msg["To"] = to

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=ctx) as s:
            s.login(user, pw)
            s.sendmail(user, [x.strip() for x in to.split(",")], msg.as_string())
        print("[send_report] Email enviado a:", to)
        return 0
    except Exception as e:  # noqa: BLE001
        print("[send_report] No se pudo enviar el email:", str(e)[:200])
        print("[send_report] Reporte por consola:\n")
        print(body)
        return 0  # no falla el workflow por un problema de email


if __name__ == "__main__":
    sys.exit(main())
