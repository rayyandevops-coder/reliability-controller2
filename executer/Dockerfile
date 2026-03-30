FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl gcc && rm -rf /var/lib/apt/lists/*

# install kubectl
RUN curl -LO "https://dl.k8s.io/release/v1.29.0/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

COPY . .

RUN pip install flask requests

CMD ["python", "app.py"]