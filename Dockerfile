FROM python:3.7-buster
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD resulting.py /
ADD latimes-state-totals.csv /
ADD cdph-race-ethnicity.csv /
CMD ["bokeh","serve","--show","resulting.py"]
