from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Path to the CSV file
csv_file_path = 'votes.csv'
csv_file_mgpt = 'mGPT.csv'
csv_file_llama = 'Llama.csv'
csv_file_quest = 'questions.csv'

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


def my_load_data(input_string):
    data = []
    with open(input_string+".csv", 'r') as csvfile:
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

@app.route('/vote', methods=['POST'])
def vote():
    option = request.form.get('option')

    # Load existing data
    data = load_data()
    # Find the option and update the votes
    for row in data:
        if row['option'] == option:
            row['votes'] = str(int(row['votes']) + 1)
            break

    # Save the updated data
    save_data(data)
    return redirect(url_for('index'))


@app.route('/modelcomp', methods=['POST'])
def modelcomp():

    option1 = request.form.get('option1')
    option2 = request.form.get('option2')
    my_num = request.form.get('num')

    my_data = my_load_data(option2)
    #model1 = my_data['']

    for row in my_data:
        if row['nums'] == str(my_num):
            cvp = row['cvp']
            return render_template('modelcomp.html', my_num=my_num, cvp=cvp, option1=option1, option2=option2 )

    return "Row not found"




if __name__ == '__main__':
    app.run(debug=True)
