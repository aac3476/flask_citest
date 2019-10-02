FROM python:3
COPY requirements.txt ./
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]
