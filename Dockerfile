# build stage
FROM python:latest AS builder

COPY requirements.txt .

# instal python dependencies to the user directory
RUN pip install --user -r requirements.txt

# second stage
FROM python:slim

# copy dependencies from build stage
COPY --from=builder /root/.local /root/.local

# copy source directory 
COPY src/ .

# update the PATH environment variable
ENV PATH=/root/.local:$PATH

# run
CMD [ "python", "-m", "gunicorn", "-w", "3", "-b", "0.0.0.0:8000", "main:server" ]
