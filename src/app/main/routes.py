from flask import Blueprint, current_app, render_template, request, send_file, after_this_request, flash, redirect, url_for, session
import subprocess
import os
import shutil
import zipfile
import requests


main_bp = Blueprint(
    'main_bo', __name__,
    template_folder='templates',
    static_folder='static'
    )

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    package_details = None
    package_name = None
    package_version = None
    requires_dist = None
    markdown_content = None
    if request.method == 'POST':
        package_name = request.form['package_name']
        if not package_name:
            flash('Package name is required!', 'error')
            return redirect('/')
        
        if "==" in package_name:
            package_version = package_name.split("==")[1]
            package_name = package_name.split("==")[0]            

        if 'get-details' in request.form:
            try:
                if not package_version:
                    response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
                else:
                    response = requests.get(f'https://pypi.org/pypi/{package_name}/{package_version}/json')
                response.raise_for_status()
                package_info = response.json()                
                package_details = package_info.get('info')                
                session['package_version'] = package_details['version']
                session['requires_dist'] = package_details['requires_dist']
                requires_dist = session.get('requires_dist')
                markdown_content = str(package_details['description'].replace('`', r'\`'))                
                #print(markdown_content)
            except requests.RequestException as e:
                flash(f"Error occurred or package does not exist.", 'error')
                return redirect('/')

        elif 'download' in request.form:
            try:
                package_version = session.get('package_version')
                
                command = ["pip", "download", f"{package_name}=={package_version}", "-d", current_app.config['DOWNLOAD_FOLDER']]
                subprocess.run(command, check=True)
                
                zip_filename = f"{package_name}_{package_version}.zip"
                zip_filepath = os.path.join(current_app.config['ZIP_FOLDER'], zip_filename)
                with zipfile.ZipFile(zip_filepath, 'w') as zipf:
                    for root, _, files in os.walk(current_app.config['DOWNLOAD_FOLDER']):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.basename(file_path))

                shutil.rmtree(current_app.config['DOWNLOAD_FOLDER'])
                os.makedirs(current_app.config['DOWNLOAD_FOLDER'])

                #log_download(package_name)

                @after_this_request
                def remove_file(response):
                    try:
                        os.remove(zip_filepath)
                    except Exception as e:
                        current_app.logger.error(f"Error removing file: {e}")
                    return response

                return send_file(zip_filepath, as_attachment=True)
            except subprocess.CalledProcessError as e:
                flash(f"Error downloading package.", 'error')
                return redirect('/')

    return render_template('index.html', package_details=package_details, package_name=package_name)

#def log_download(package_name):
#    with open("download_log.txt", "a") as log_file:
#        log_file.write(f"{datetime.now()}: {package_name} downloaded\n")


