#FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime
FROM python:3.11.9-slim

WORKDIR /root
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN apt update && apt install -y tesseract-ocr
RUN chmod +x entrypoint.sh
EXPOSE 5000

ENV PROJECT=tesseract

ENTRYPOINT ["./entrypoint.sh"]
CMD ["flask"]

