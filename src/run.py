import os
import tempfile
from app import create_app


def main():
    app = create_app()
    app.secret_key = 'supersecretkey'
    temp_dir = tempfile.gettempdir()
    downloads_folder = os.path.join(temp_dir, 'downloads')
    zips_folder = os.path.join(temp_dir, 'zips')
    app.config['DOWNLOAD_FOLDER'] = downloads_folder
    app.config['ZIP_FOLDER'] = zips_folder

    os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['ZIP_FOLDER'], exist_ok=True)
    app.run('0.0.0.0', debug=True)


if __name__ == '__main__':
    main()