# Obraz pro spouštění kódu od agenta: Python a knihovny, nic víc.
# Sestavení:  docker build -t agent-python .
FROM python:3.12-slim
RUN pip install --no-cache-dir requests pandas matplotlib
RUN useradd --create-home agent
USER agent
WORKDIR /prace
