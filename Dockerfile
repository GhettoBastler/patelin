# build stage
FROM --platform=linux/arm64 python:latest AS builder

COPY requirements.txt .

# instal python dependencies to the user directory
RUN pip install --user -r requirements.txt

# second stage
FROM --platform=linux/arm64 python:slim

# copy dependencies from build stage
COPY --from=builder /root/.local /root/.local

# copy source directory 
COPY src/ .

# update the PATH environment variable
ENV PATH=/root/.local:$PATH

# run
CMD [ "python", "./main.py" ]
