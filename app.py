from datetime import datetime
import pytz
from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Path to the CSV file
csv_file_path = 'votes.csv'
csv_file_mgpt = 'mGPT.csv'
csv_file_llama = 'Llama.csv'
csv_file_quest = 'questions.csv'
csv_file_rslts = 'rslts.csv'

# Check if the CSV file exists, if not create it with headers
if not os.path.exists(csv_file_path):
  with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['option', 'votes']
    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csv_writer.writeheader()


# Load initial data from the CSV file
def load_data():
  data = []
  with open(csv_file_path, 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
      data.append(row)
  return data


def append_to_csv(data):
  with open(csv_file_rslts, 'a', newline='') as csvfile:
    fieldnames = ['name', 'time', 'questionNo', 'Models', 'Winner']
    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csv_writer.writerow(data)


def my_load_data(input_string):
  data = []
  with open(input_string + ".csv", 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
      data.append(row)
  return data


def my_load_num(num):
  num = int(num)
  return num


#
# Save data to the CSV file
def save_data(data):
  with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['option', 'votes']
    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(data)


@app.route('/')
def index():
  options = load_data()
  return render_template('index.html', options=options)

  # Save the updated data
  save_data(data)
  return redirect(url_for('index'))


@app.route('/modelcomp', methods=['POST'])
def modelcomp():
  option1 = request.form.get('option1')
  option2 = request.form.get('option2')
  my_num = request.form.get('num')
  user = request.form.get('User')
  ques = my_load_data('questions')
  my_data = my_load_data(option1)
  my_data2 = my_load_data(option2)
  data_to_append = {
      'name': user,
      'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
      'questionNo': my_num,
      'Models': option1 + " VS " + option2
  }

  #append_to_csv(data_to_append)

  tst_data = my_data

  for row in ques:
    if row['nums'] == str(my_num):
      ques1 = row['cvp']
      break

  for row in my_data:
    if row['nums'] == str(my_num):
      cvp1 = row['cvp']
      break

  for row in my_data2:
    if row['nums'] == str(my_num):
      cvp2 = row['cvp']
      break

  return render_template('modelcomp.html',
                         my_num=my_num,
                         cvp1=cvp1,
                         cvp2=cvp2,
                         option1=option1,
                         option2=option2,
                         tst_data=tst_data,
                         ques1=ques1,
                         user=user)


@app.route('/modelcomp/button_function', methods=['POST'])
def button_function():
  option1 = request.form.get("option1")
  option2 = request.form.get("option2")

  gmt_plus_3 = pytz.timezone('Etc/GMT-3')
  current_time_gmt_plus_3 = datetime.now(gmt_plus_3)
  
  data_to_append = {
      'name': request.form.get('user'),
      'time': current_time_gmt_plus_3,
      'questionNo': request.form.get('my_num'),
      'Models': f"{option1} vs {option2}",
      'Winner': request.form.get('results')
  }
  append_to_csv(data_to_append)
  return request.form.get('results')


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080)
