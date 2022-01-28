import os

from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template, session

from protein_spectra_package.startup import DATA_DIR
from protein_spectra_package.reader import *
from protein_spectra_package.peptide_prediction import *
from protein_spectra_package.protein_prediction import *


UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
ALLOWED_EXTENSIONS = {"mzml", "mzxml", "fasta"}

app = Flask(__name__)
app.secret_key = "someSecretKey"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':  # User choosing file type
        file_type = request.form['file_type']
        import_check = toggle_file_type(file_type)
        if session['ms_files']  and session['fasta_file'] is not None:  # Both File(s) imported
            rel_vals = get_values(session['ms_files'])
            hits, peptide_hits = get_peptide_hits(session['fasta_file'], session['ms_files'])
            prtns = get_proteins(hits)
            return render_template('template.html', values=rel_vals, hits=peptide_hits, protein=prtns, import_msg=import_check)

        else:
            return render_template('template.html', import_msg=import_check)

    return render_template('template.html')


@app.route("/upload")
def upload():
    return render_template('upload.html')


@app.route("/home", methods=['GET', 'POST'])
def homepage():
    return render_template('template.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if request.form["button"] == "Upload":
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            files = request.files.getlist('file')
            # if user does not select file, browser also
            # submit an empty part without filename
            for file in files:
                if file.filename == '':
                    flash('No file selected')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if check_uploads():
                return render_template('template.html', success_msg="File(s) uploaded successfully!")
            else:
                return render_template('upload.html', success_msg="Please upload the other file!")
            return redirect(url_for('home'))
        elif request.form['button'] == "Clear Contents":
            files = os.listdir(UPLOAD_FOLDER)
            for file in files:
                os.remove(os.path.join(UPLOAD_FOLDER, file))
            return render_template('upload.html', success_msg="Uploaded files successfully removed!")
        return redirect(url_for('home'))


def toggle_file_type(file_type: str) -> str:
    ext = ".mzML" if file_type == "mzml" else ".mzxml"
    ms_files = [
        os.path.join(app.config['UPLOAD_FOLDER'], f)
        for f in os.listdir(app.config['UPLOAD_FOLDER'])
        if f.endswith(ext)
    ]
    fasta_file = [
        os.path.join(app.config['UPLOAD_FOLDER'], f)
        for f in os.listdir(app.config['UPLOAD_FOLDER'])
        if f.endswith(".fasta")
    ]
    if file_type == "mzml" and len(ms_files) != 1:
        return "Error importing mzml file. Please clear uploaded contents and upload a single mzml file."

    elif file_type == "mzxml" and len(ms_files) != 1:
        return "Error importing mzxml file. Please clear uploaded contents and upload a single mzxml file."

    else:
        session['file_type'] = file_type
        session['ms_files'] = ms_files[0]
        session['fasta_file'] = fasta_file[0]
        return "File(s) imported successfully!"


def check_uploads():
    n_files = len(os.listdir(app.config['UPLOAD_FOLDER']))
    if n_files == 2:
        return True
    else:
        return False


def get_values(file):
    relevant_values = Reader(file)
    values = relevant_values.analyse_spectrum()
    rel_vals = values.to_html(header="true", table_id="table", index=False, justify= "justify-all")
    return rel_vals


def get_peptide_hits(fasta_file, ms_file):
    peptides = PeptideSearch(fasta_file, ms_file)
    hits = peptides.peptide_wrapper()[0]
    peptide_hits = hits.to_html(header="true", table_id="table", index=False)
    return hits, peptide_hits


def get_proteins(hits):
    peptide_list = hits['Peptide hit sequence']
    pro_search = ProteinSearch(peptide_list)
    pro_search.get_proteins()
    ans_with_seq = pro_search.ans_df
    ans_without_seq = ans_with_seq.drop('Sequence', axis=1)
    proteins = ans_without_seq.to_html(header="true", table_id="table", index=False)
    return proteins


if __name__ == '__main__':
    app.run(debug=True)




