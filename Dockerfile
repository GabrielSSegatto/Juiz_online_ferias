FROM python:3.10-slim

# Instala o cliente do Docker para o Flask conseguir invocar as jaulas de execução
RUN apt-get update && apt-get install -y docker.io && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala o servidor de produção (Gunicorn)
RUN pip install gunicorn

# Copia todo o código fonte
COPY . .

# Expõe a porta padrão
EXPOSE 5000

# Roda o Gunicorn com 4 trabalhadores paralelos (adeus lentidão!)
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "run:app"]
