FROM python:3.9-slim

WORKDIR /app

COPY ./frontend.py /app/frontend.py
COPY ./background.png /app/background.png
RUN pip install streamlit requests

EXPOSE 8501

CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]

