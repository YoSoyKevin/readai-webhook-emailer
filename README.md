# 🤖 ReadAI Webhook Emailer – AWS Lambda Serverless

¿Quieres que tus reuniones hablen por sí solas? Este servicio convierte los webhooks de [Read.ai](https://read.ai) en correos electrónicos amigables, claros y personalizados. Todo eso sin mover un dedo. Tú haces la reunión, nosotros el resto.

---

## 🚀 ¿Qué hace esta Lambda?

- 📩 Recibe payloads vía webhook de Read.ai.
- 🔍 Filtra participantes por dominio (ej. `@tudominio.com`, `@midominio.com`).
- 📆 Convierte fechas y horas a formato legible y local (UTC-5).
- 🛠️ Genera correos HTML con:
  - Lista de asistentes y ausentes
  - Temas tratados
  - Acciones pendientes
  - Preguntas clave
  - Link personalizado para solicitar el video
- ✉️ Envío de correos por Gmail (SMTP).
- 💥 Manejo básico de errores con logs detallados.

---

## 🧪 Variables de entorno

Asegúrate de configurar lo siguiente en tu entorno Lambda:

| Variable     | Descripción                         |
|--------------|-------------------------------------|
| `gmail_user` | Correo Gmail remitente              |
| `gmail_pass` | Contraseña o App Password de Gmail  |
| `API_URL`    | URL base para generar el link del video |

---

## 🛠️ Deploy en AWS Lambda

1. Crea una función Lambda con **Python 3.8+**.
2. Establece las variables de entorno mencionadas.
3. Sube el archivo `.py` como `lambda_function.py`.
4. Agrega un trigger API Gateway para recibir los webhooks de Read.ai.
5. Prueba y monitoriza los logs (CloudWatch).

---

## 🧾 Estructura

```
📦 readai-webhook-emailer/
 ┣ 📄 lambda_function.py   # Código principal
 ┣ 📄 requirements.txt     # (Vacío por ahora)
 ┗ 📄 README.md             # Este archivo con toda la magia
```

---

## 🧱 Posibles mejoras

- 🕒 Manejo de zonas horarias con `pytz` o `pendulum`.
- 📬 Migrar a AWS SES para mejor control de envío.
- 🎨 Plantillas de correo con `Jinja2`.
- ✅ Validación de seguridad para webhooks entrantes.

---

## 📦 Requisitos

```bash
Python >= 3.8
```

**requirements.txt**
```txt
# No hay dependencias externas... aún
```

---


## 📄 Licencia

MIT License – úsalo, modifícalo y hazlo aún mejor.

---

> _“Las reuniones sin resumen son como promesas sin acción. Este bot se encarga de eso.”_  

