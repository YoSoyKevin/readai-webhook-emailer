# -*- coding:utf-8 -*-
import json
import os
import base64
from email.message import EmailMessage
import smtplib
from datetime import datetime, timedelta

def lambda_handler(event, context):

    request_body = base64.b64decode(event['body']).decode('utf-8')
    request_body = json.loads(request_body)

    title = request_body.get('title', '')
    start_time = request_body.get('start_time', '')
    end_time = request_body.get('end_time', '')
    start_time_date, start_time_hour = tzone_convert(start_time)
    end_time_date, end_time_hour = tzone_convert(end_time)
    participants = request_body.get('participants', [])

    participants = [
        {'name': p.get('name', ''), 'email': p.get('email', '')}
        for p in participants
    ]

    # Filtrar destinatarios válidos por dominio permitido
    allowed_domains = os.getenv('ALLOWED_DOMAINS', '').split(',')
    destinatarios = [
        p['email'] for p in participants
        if p.get('email') and any(domain in p['email'] for domain in allowed_domains)
    ]

    participants_absent = [
        {'name': p['name'], 'email': p['email']}
        for p in participants
        if p['email'] is not None and p['name'] == p['email']
    ]

    participants_absent_HTML = ''
    if participants_absent:
        participants_absent_HTML += '<p><strong>No asistieron:</strong></p><ul>'
        for p in participants_absent:
            participants_absent_HTML += f'<li>{p["email"]}</li>'
        participants_absent_HTML += '</ul>'

    participants_HTML = '<ul>'
    for p in participants:
        if p['email'] is not None:
            participants_HTML += f'<li>{p["name"]} - {p["email"]}</li>'
        else:
            participants_HTML += f'<li>{p["name"]}</li>'
    participants_HTML += '</ul>'

    summary = request_body.get('summary', '')
    action_items_HTML = _list_to_html(request_body.get('action_items', []))
    key_questions_HTML = _list_to_html(request_body.get('key_questions', []))
    topics_HTML = _list_to_html(request_body.get('topics', []))

    session_id = request_body.get('session_id', '')
    report_url = request_body.get('report_url', '')

    remitente = os.environ.get('EMAIL_USER')
    api_url = os.environ.get('API_URL')

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com") as smtp:
            smtp.login(remitente, os.environ.get('EMAIL_PASS'))

            for destinatario in destinatarios:
                try:
                    unique_api_url = f"{api_url}id={session_id}&email={destinatario}"

                    mensaje_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <body>
                    <p style="font-size: small; color: gray;">Session ID: {session_id}</p>
                    <p>Hi 👋,</p> 
                    <p>Here is the meeting summary for <strong>{start_time_date} at {start_time_hour}</strong>.</p> 
                    <p><strong>Participants:</strong></p>
                    {participants_HTML}
                    {participants_absent_HTML}
                    <p>{summary}</p>
                    <p><strong>Topics Discussed:</strong></p>
                    {topics_HTML}
                    <p><strong>Action Items:</strong></p>
                    {action_items_HTML}
                    <p><strong>Key Questions:</strong></p>
                    {key_questions_HTML}
                    <p>🎥 To access the meeting video click 👉 <a href="{unique_api_url}">here</a>.</p>
                    <p>Regards,</p>
                    <p>Your Digital Assistant 🤖</p>
                    </body>
                    </html>"""

                    email = EmailMessage()
                    email["From"] = remitente
                    email["To"] = destinatario
                    email["Subject"] = f"Meeting Summary: {title}"
                    email.set_content("This is an HTML email. Please enable HTML view.")
                    email.add_alternative(mensaje_html, subtype='html')

                    smtp.sendmail(remitente, destinatario, email.as_string())
                    print(f"Email sent to: {destinatario}")

                except Exception as e:
                    print(f"Error sending email to {destinatario}: {e}")

    except Exception as e:
        print(f"SMTP connection error: {e}")

    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "body": json.dumps(event),
        "headers": {
            "Content-Type": "application/json"
        }
    }

def tzone_convert(time):
    if time.endswith('Z'):
        time = time.replace('Z', '+00:00')
    time_datetime = datetime.fromisoformat(time)
    if time_datetime.utcoffset() != timedelta(hours=-5):
        utc_offset = timedelta(hours=-5)
        time_datetime = time_datetime.astimezone(tz=None) + (utc_offset - time_datetime.utcoffset())

    time_date = time_datetime.strftime('%d/%m/%Y')
    time_hour = time_datetime.strftime('%I:%M %p')
    return time_date, time_hour

def _list_to_html(items):
    html = '<ul>'
    for item in items:
        html += f'<li>{item.get("text", "")}</li>'
    html += '</ul>'
    return html
