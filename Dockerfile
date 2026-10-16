FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd --uid 10001 --create-home student
COPY --chown=student:student app.py ./
COPY --chown=student:student templates ./templates
COPY --chown=student:student data ./data
USER student
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "app:app"]
