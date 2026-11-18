# Receta para construir la app en la nube (Render). No necesita Docker en su computador.
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# El servicio de hosting indica el puerto en la variable PORT; en local se usa 8765.
ENV PORT=8765
EXPOSE 8765
CMD solara run app.py --host 0.0.0.0 --port ${PORT} --production --no-open
