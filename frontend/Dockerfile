FROM python:3.9-slim

# הגדרת סביבת העבודה בתוך הקונטיינר
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --timeout=1000 streamlit requests

# העתקת כל הקבצים הרלוונטיים
COPY ./app.py /app/app.py
COPY ./components /app/components
COPY ./pages /app/pages
COPY ./assets /app/assets

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
