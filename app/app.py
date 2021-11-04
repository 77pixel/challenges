from flask import Flask, render_template, request, send_file
import os
import math
from collections import defaultdict
import uuid



app = Flask(__name__)
uuid.uuid4().hex


# Benford's law percentages for leading digits 1-9
BENFORD = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
#db folder
DB_DIR = './db/'


def benford_first_digits(column_data):
    #empty dict
    first_digits = defaultdict(int) 
    
    for val in column_data:
        if val == '': continue
        str_val = str(val)
        #checking first digit in string number
        first_digits[str_val[0]] += 1

    #sorting output
    data_count = [v for (k,v) in sorted(first_digits.items())]
    
    #count total
    total_count = sum(data_count)
    
    #count percentage
    data_pct = [(i/total_count) * 100 for i in data_count]
    
    return data_count, data_pct, total_count


def parse_file(file, col_number, col_benford):
    
    #open and read file
    f = open(file,"r")
    lines = f.readlines()
    f.close()

    ret = []
    ret_err =[]
    benford_list = []

    for line in lines:
        
        #simple remove white characters
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        
        #split the line
        l = line.split('\t')
        
        #check column number as expected
        if len(l) == col_number:

            #check if value is integer and append to list and table if its correct
            try:
                benford_list.append(int(l[col_benford-1]))
                ret.append(l)
            except ValueError:
                ret_err.append(l)
        else:
            ret_err.append(l)

    #find and count digits
    ret_benford = benford_first_digits(benford_list)

    # chi-square test statistic based on Benford norm 
    expected_counts =  [round(p * float(ret_benford[2])/ 100) for p in BENFORD]
    chi_square_stat = 0; 
    
    for data, expected in zip(ret_benford[0], expected_counts):
        chi_square = math.pow(data - expected, 2)
        chi_square_stat += chi_square / expected

    return (ret, ret_err, ret_benford, "{:.3f}".format(chi_square_stat), chi_square_stat < 15.51)


@app.route('/benford/<uid>', methods = ['GET', 'POST'])
def upload_file(uid):
    if request.method == 'POST':
        
        #get file and config values
        file = request.files['file']
        col_number = int(request.form['col_number'])
        col_benford = int(request.form['col_benford'])
        
        if 'show_raw_table' in request.form: 
            show_raw_table = True
        else:
            show_raw_table = False

        if file:
            #generate unige name
            new_uid = str(uuid.uuid4().hex)
            
            #save data and config
            file_path = os.path.join(DB_DIR, new_uid + '.raw')
            file.save(file_path)
            conf = open(os.path.join(DB_DIR, new_uid + '.txt'),"w")
            conf.write("{};{};{}".format(col_number,col_benford, show_raw_table))
            conf.close()
            
            #do calclulation
            benford_data = parse_file(file_path, col_number, col_benford)
            
            #send data
            return render_template('benford.html', 
                                    table = benford_data[0], 
                                    errtable = benford_data[1],
                                    benford = BENFORD, 
                                    file = benford_data[2][1],
                                    chi_square_stat = benford_data[3],
                                    result = benford_data[4],
                                    show_raw_table = show_raw_table,
                                    fileid = new_uid)
        
    if request.method == 'GET':
        
        #open config and data
        conf = open(os.path.join(DB_DIR, uid + '.txt'), "r")
        c = conf.read()
        config_list = c.split(';')
        conf.close()
        col_number = int(config_list[0])
        col_benford = int(config_list[1])
        if str(config_list[2]) == 'True': 
            show_raw_table = True
        else:
            show_raw_table = False
        
        benford_data = parse_file(os.path.join(DB_DIR, uid + '.raw'), col_number, col_benford)
        return render_template('benford.html', 
                                table = benford_data[0], 
                                errtable = benford_data[1],
                                benford = BENFORD, 
                                file = benford_data[2][1],
                                chi_square_stat = benford_data[3],
                                result = benford_data[4],
                                show_raw_table = show_raw_table,
                                fileid = uid)
        
@app.route('/')
def index_html():
    return render_template('index.html')

@app.route('/challenge/<id>')
def show_user_profile(id):    
    return render_template('challenge{}.html'.format(id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

