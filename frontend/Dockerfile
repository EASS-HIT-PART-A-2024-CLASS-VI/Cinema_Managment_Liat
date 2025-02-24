FROM python:3.9-slim

# הגדרת סביבת העבודה בתוך הקונטיינר
WORKDIR /app

RUN pip install --upgrade pip

# העתקת קובץ requirements.txt לפרונטאנד
COPY ./requirements.txt /app/requirements.txt

# התקנת כל התלויות, כולל streamlit-sortables
RUN pip install --no-cache-dir -r /app/requirements.txt

# העתקת כל הקבצים הרלוונטיים
COPY ./app.py /app/app.py
COPY ./components /app/components
COPY ./pages /app/pages
COPY ./assets /app/assets
COPY ./tests /app/tests
COPY ./setup.py /app/setup.py
COPY ./conftest.py /app/conftest.py

# Install the package in development mode
RUN pip install -e .

# Ensure all necessary directories are Python packages
RUN touch /app/components/__init__.py
RUN touch /app/pages/__init__.py
RUN touch /app/tests/__init__.py

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]