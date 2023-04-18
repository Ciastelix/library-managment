FROM python:3.11.3-alpine3.16
COPY . .
RUN pip install -r requirements.txt

ENV DATABASE_URL="sqlite:///db.db"
ENV SECRET_KEY="MY_OWN_SECRET_KEY"
ENV ALGORITM="HS26"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]