from flask import Flask, request, render_template,session
from flask_cors import CORS
import json
import glob
import os
import constant

app = Flask(__name__, static_url_path='', static_folder='static',  template_folder='templates')
CORS(app)

@app.route('/')
def index():
    # Load scan result json files list
    result_files = [os.path.basename(x) for x in glob.glob('data/json/*.json')]
    result_files.sort()

    # Json file url argument
    if request.args.get("jsonfile"):
        jsonfile = request.args.get("jsonfile")
        session['jsonfile'] = jsonfile

    # Filters
    feature = request.args.get("feature") if request.args.get("feature") else ""
    severity = request.args.get("severity") if request.args.get("severity") else ""

    # Load Json file
    if not session.get('jsonfile'): session['jsonfile'] = "none"
    json_src = 'data/json/' + session['jsonfile']

    rows_len = 0
    result_list = []
    dockerimage = ""
    if os.path.isfile(json_src):
        with open(json_src) as json_file:
            data = json.load(json_file)
            result_list = []
            dockerimage = data['image']
            for p in data['vulnerabilities']:
                if feature == "" and severity == "" or feature == p['featurename'] or severity == p['severity']:
                    status = "unapproved" if p['vulnerability'] in data['unapproved'] else "approved"
                    result_list.append(dict(
                        severity=p['severity'],
                        vulnerability=p['vulnerability'],
                        link=p['link'],
                        featurename=p['featurename'],
                        featureversion=p['featureversion'],
                        namespace=p['namespace'],
                        description=p['description'],
                        status=status
                    ))
        rows_len = len(result_list)

    # Return rendered HTML template
    return render_template('vulns-list.html',
                           rows=result_list,
                           rows_len=rows_len,
                           result_files=result_files,
                           jsonfile=session['jsonfile'],
                           dockerimage=dockerimage,
                           )

@app.route('/whitelist', methods=['POST'])
def whitelist():
    req_data = request.form
    yml_out = "generalwhitelist:\r\n"
    for p in req_data:
        if "CVE" in p:
            vuln = p.split("@")
            yml_out +=  "  "+vuln[0]+": "+vuln[1]+"\r\n"

    return render_template('whitelist.html', whitelist=yml_out, write_result=0)

@app.route('/whitelist/save', methods=['POST'])
def whitelist_save():
    req_data = request.form
    # Write file
    write_result = "Error!"
    if req_data['yamlfile']:
        yaml_output_file = "/app/data/whitelists/"+req_data['yamlfile']+".yml"
        f = open(yaml_output_file, "w")
        if f.write(req_data['yamloutput']):
            write_result = yaml_output_file
        f.close()

    return render_template('whitelist.html', whitelist=req_data['yamloutput'], write_result=write_result)

def main():
    app.secret_key = constant.SECRET_KEY
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=constant.DEBUG, host='0.0.0.0')

if __name__ == '__main__':
    main()

