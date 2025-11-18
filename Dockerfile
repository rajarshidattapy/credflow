# 1. Start with a lean Python image
FROM python:3.12-slim

# 2. Set the working directory
WORKDIR /code

# 3. Copy requirements and install (cached)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy ONLY the frontend code
# We rename it to app.py for a standard name
COPY frontend/dashboard.py ./app.py

# 5. Expose the port Cloud Run provides.
# This is just documentation, the CMD is what matters.
EXPOSE 8080

# 6. The command to run Streamlit
#
# --- THIS IS THE FIX ---

CMD streamlit run app.py --server.port=$PORT --server.headless=true --server.enableCORS=false