FROM python:3.10

# Set up user permissions for Hugging Face
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Go inside backend folder and install requirements
COPY --chown=user backend/requirements.txt $HOME/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the python files from backend folder
COPY --chown=user backend/ $HOME/app/

# Start the FastAPI Server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]