# Use an official Python runtime 
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8502 available to the world outside this container
EXPOSE 8502

# Run the Streamlit app when the container launches
CMD ["streamlit", "run", "main.py", "--server.port=8502", "--server.address=0.0.0.0"]
