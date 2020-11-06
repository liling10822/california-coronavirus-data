FROM python:3.7-buster
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD visualization_corona_data.py /
ADD latimes-state-totals.csv /
ADD cdph-race-ethnicity.csv /
CMD ["bokeh","serve","-show", "visualization_corona_data.py"]
