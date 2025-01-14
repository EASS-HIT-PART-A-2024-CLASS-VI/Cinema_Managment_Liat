FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Upgrade pip and install dependencies with increased timeout
RUN pip install --upgrade pip
RUN pip install --timeout=1000 streamlit requests

# Copy application files
COPY ./frontend.py /app/frontend.py
COPY ./background.png /app/background.png
COPY ./moviesback.png /app/moviesback.png

# Expose the port Streamlit will use
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
