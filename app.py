import random 
from datetime import datetime
import pytz
from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Path to the CSV file
csv_file_path = 'main.csv'
csv_file_mgpt = 'mGPT.csv'
csv_file_llama = 'Llama.csv'
csv_file_quest = 'questions.csv'
csv_file_rslts = 'rslts.csv'
csv_file_tmp = 'tmp.csv'


# Load initial data from the CSV file
def load_data():
  data = []
  with open(csv_file_path, 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
      data.append(row)
  return data

def read_csv_to_dict_list(csv_file_path):
    dict_list = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dict_list.append(dict(row))
    return dict_list


def write_to_csv_tmp(data):
  with open(csv_file_tmp, 'w', newline='') as csvfile:
    fieldnames = ['name', 'time', 'questionNo', 'models', 'winner']
    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csv_writer.writerow(data)

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




# Save data to the CSV file
def save_data(data):
  with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['option', 'votes']
    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(data)


@app.route('/')
def index():
  options = my_load_data("main")
  questions = my_load_data("questions")

  x = random.randint(1,4)
  y = random.randint(1,4)
  z = random.randint(1,4)

  while( x == y ):
    x = random.randint(1,4)

  randModel1_name = (options[x])['MODEL']
  randModel1_ID = (options[x])['ID']
  randModel2_name = (options[y])['MODEL']
  randModel2_ID = (options[y])['ID']
  randQ_text = (questions[z])['cvp']
  randQ_ID = (questions[z])['nums']
 
  model1_answr = ((my_load_data(randModel1_name))[int(randQ_ID)-1])['cvp']
  model2_answr = ((my_load_data(randModel2_name))[int(randQ_ID)-1])['cvp']

  print("model1_name:", randModel1_name)
  print("model1_ID:", randModel1_ID)
  print("model2_name:", randModel2_name)
  print("model2_ID:", randModel2_ID)
  print("The Question:", randQ_text)
  print("Questio ID:", randQ_ID)
  print("Model1 Answer:", model1_answr)

  data_to_write = {
        'time' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'questionNo' : randQ_ID,
        'models': (randModel1_name+' VS '+randModel2_name),
    }
  write_to_csv_tmp(data_to_write)

  return render_template('index.html', options = options,
                         randQ_text = randQ_text,
                         model1_answr = model1_answr,
                         model2_answr = model2_answr,
                         randModel1_name = randModel1_name,
                         randModel2_name = randModel2_name)

@app.route("/button", methods=["POST", "GET"])
def button_function():
    rslt = request.form.get("results")
    model2 = request.form.get("model2")
    tmp[] = read_csv_to_dict_list("tmp.csv")
    print("tmp stuff: ",tmp)
    data_to_append = {
        'name': request.form.get('user'),
        'winner': request.form.get('results')
    }
    print(data_to_append)
    return "SUCCESS"


if __name__ == '__main__':
    app.run(debug=True)
