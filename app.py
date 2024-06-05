# an object of WSGI application

from datetime import datetime

import pyodbc
from flask import Flask, Response, jsonify, render_template, request, session, redirect, url_for,flash      
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import requests
#import easyocr

# from flask_session import Session
from fuzzywuzzy import process
import math
import re


app = Flask(__name__, template_folder="templates")  # Flask constructor

app.secret_key = "aurexus@106"
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
# A decorator used to tell the application
# which URL is associated function
conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:aurexdb.database.windows.net;Database=AUREXDB1;Uid=db_su;Pwd={=!Aurexus21!=};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()
api_key = "a77d51086fb7455dbc9b8284573e7feb"
endpoint = "https://aurexusformprocessocr.cognitiveservices.azure.com/"

# Initialize the Form Recognizer client
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(api_key)
)


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/home")
def hello():
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    session.pop('sql_query', None)
    session.pop('sql_query2', None)
    session.pop('sort', None)
    session.pop('sortype', None)
    session.pop('params', None)
    # Count of All Traitement in the project

    cursor.execute(
        "select count(u990_b) as AnoCount,Folder,Proj  from dbo._unimarc  where proj = 'CAEN' and (chkTest<>0) and u990_b<>'' And u990_b<>'_' group by Folder,Proj"
    )
    rows = cursor.fetchall()
    html_ano = ""
    for row in rows:
        row_dicts = dict(zip([column[0] for column in cursor.description], row))
        html_ano += "<tr>"
        for column_name in ["Folder", "AnoCount"]:
            html_ano += "<td>" + str(row_dicts.get(column_name, "")) + "</td>"
        html_ano += "</tr>"

    # Count of All Traitement in the project

    cursor.execute(
        "SELECT traitement,count(traitement) as count_val FROM dbo._unimarc where proj='CAEN' group by traitement"
    )
    rows = cursor.fetchall()
    html_content = ""
    for row in rows:
        row_dict = dict(zip([column[0] for column in cursor.description], row))
        html_content += "<tr>"
        for column_name in ["traitement", "count_val"]:
            html_content += "<td>" + str(row_dict.get(column_name, "")) + "</td>"
        html_content += "</tr>"

    # Total Notice Count of the Project

    cursor.execute("SELECT count(*) as all_count FROM dbo._unimarc where proj='CAEN'")
    rows = cursor.fetchall()
    for row in rows:
        all_count = row[0]

    # Total Notice Count of the Project

    cursor.execute(
        "SELECT Proj,sum(case when ID>30000 and Proj like 'CAEN%' and (chkTest<>0) and u990_b<>'' And u990_b<>'_' then 1 else 0 end) AS Expr1, sum(case when ID>30000 and Proj like 'CAEN%' and (Ano_AnsCode<>'') and u990_b<>'' And u990_b<>'_' then 1 else 0 end) AS Expr2 FROM dbo._unimarc where ID>30000 and Proj like 'CAEN%' GROUP BY Proj"
    )
    rows = cursor.fetchall()
    for row in rows:
        todo = int(row[1])
        done = int(row[2])

    # List of Process with progress bar from client report
    cursor.execute("select * from dbo.[CAEN_Report]")
    html_process = ""
    for row in cursor.fetchall():
        if row.Quantity:
            title = row.EnglishTitle
            percentage = round((row.Done / row.Quantity) * 100)
            html_process += f'<div style="height:45px;"><label class="tx-12 tx-gray-600 mg-b-10">{title} ({percentage}%)</label><div class="progress" style="height: 9px;border-radius:0px;"><div class="progress-bar wd-25p progress-bar-striped active" role="progressbar" style="width:{percentage}%;size:10px;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div></div></div>'
    # Total completed Precentage of the project

    cursor.execute(
        "select FrenchTitle from dbo.[CAEN_Report] where EnglishTitle='Percentage'"
    )
    rows = cursor.fetchall()
    for row in rows:
        percentage = float(row[0])

    return render_template(
        "hometest.html",
        html_content=html_content,
        html_ano=html_ano,
        all_count=all_count,
        html_process=html_process,
        todo=todo,
        done=done,
        percentage=percentage,
    )


@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        name = request.form.get("user")
        password = request.form.get("pass")
        cursor.execute(
            "select * from dbo.User_table where Username=? and Password=?",
            (name, password)
        )

        row = cursor.fetchall()

        if row:
            session["name"] = name
            return hello()
        else:
            return render_template(
                "login.html", message="Please Check the Credential's"
            )

@app.route("/listdata", methods=["GET", "POST"])
def listdata():
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    html_content_fil = ""  # Initialize html_content variable
    process=""
    anotype=""

    # Initialize page_no variable
    #page_no = 1
    cursor.execute(
        "SELECT lot FROM dbo._unimarc where proj='CAEN' group by lot"
    )
    rows = cursor.fetchall()
    for row in rows:
        html_content_fil +=f'<option value="{row[0]}">{row[0]}</option>'
    
    cursor.execute(
        "SELECT traitement FROM dbo._unimarc where proj='CAEN' group by traitement"
    )
    rows = cursor.fetchall()
    for row in rows:
        process +=f'<option value="{row[0]}">{row[0]}</option>'
    
    cursor.execute(
        "SELECT u990_b FROM dbo._unimarc where proj='CAEN' and datalength(u990_b)>0 group by u990_b"
    )
    rows = cursor.fetchall()

    for row in rows:
        anotype +=f'<option value="{row[0]}">{row[0]}</option>'


    html_content = ""
    page_no = int(request.args.get('page_no', 1))  # Get current page number
    session['listpage_no']=page_no

    if request.method == "POST" and "filters" in request.form:
        session.pop('sort',None)
        session.pop('sortype',None)
        session.pop('params',None)
        session.pop('sql_query',None)
        session.pop('sql_query2',None)
        # Retrieve form data
        dossier = request.form["dossier"]
        traitement = request.form["traitement"]
        types = request.form["type"]
        anscode = request.form["anscode"]
        searchword = request.form["searchword"]
        keycol = request.form["keycol"]
        sort = request.form.get("sort", "order by z001_x0")  # Default sort column if not provided
        session['sort']=sort
        sortype = request.form.get("sortype", "ASC")
        session['sortype']=sortype

        # Build SQL query based on form data
        sql_query = "SELECT COUNT(*) FROM dbo._unimarc WHERE Proj = 'CAEN'"
        sql_query2 = """
            SELECT *, 
            Row_Number() Over ({sort} {sortype}) AS Rows 
            FROM dbo._unimarc 
            WHERE Proj = 'CAEN'
        """.format(sort=sort, sortype=sortype)
        params = []

        if dossier != "ALL":
            sql_query += " AND Lot = ?"
            sql_query2 += " AND Lot = ?"
            params.append(dossier)
        if traitement != "ALL":
            sql_query += " AND traitement = ?"
            sql_query2 += " AND traitement = ?"
            params.append(traitement)
        if types != "ALL":
            sql_query += " AND u990_b = ?"
            sql_query2 += " AND u990_b = ?"
            params.append(types)
        if anscode != "ALL":
            sql_query += " AND Ano_AnsCode = ?"
            sql_query2 += " AND Ano_AnsCode = ?"
            params.append(anscode)
        if searchword:
            sql_query += f" AND {keycol} COLLATE Latin1_General_CI_AI LIKE ?"
            sql_query2 += f" AND {keycol} COLLATE Latin1_General_CI_AI LIKE ?"
            params.append(f"%{searchword}%")

        # Save queries and params in session
        session['sql_query'] = sql_query
        session['sql_query2'] = sql_query2
        session['params'] = params

    else:
        # Handle initial page load or no filters submitted
        # sql_query = session.get('sql_query', "SELECT COUNT(*) FROM dbo._unimarc WHERE Proj = 'CAEN'")
        sort=session.get('sort','order by z001_x0')
        sortype=session.get('sortype','ASC')
        print(sort)
        sql_query = session.get('sql_query', "SELECT COUNT(*) FROM dbo._unimarc WHERE Proj = 'CAEN'")
        sql_query2 = session.get('sql_query2', """
            SELECT *, 
            Row_Number() Over ({sort} {sortype}) AS Rows 
            FROM dbo._unimarc 
            WHERE Proj = 'CAEN'
        """.format(sort=sort, sortype=sortype))
        params = session.get('params', [])
        # if not sql_query and not sql_query2
        
    # Execute SQL query for total records
    print(sql_query)
    print(params)
    cursor.execute(sql_query, params)
    total_records = cursor.fetchone()[0]

    # Pagination logic
    total_records_per_page = 20
    offset = (page_no - 1) * total_records_per_page
    total_no_of_pages = math.ceil(total_records / total_records_per_page)
    previous_page = page_no - 1 if page_no > 1 else 1
    next_page = page_no + 1 if page_no < total_no_of_pages else total_no_of_pages
    second_last = total_no_of_pages - 1

    # Modify sql_query2 for pagination
    sql_query2 += " ORDER BY z001_x0 OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    pagination_params = params + [offset, total_records_per_page]
    print(sql_query2)
    # Execute SQL query for records
    cursor.execute(sql_query2, pagination_params)
    recordsPrint = cursor.fetchall()

    # Generate HTML content for records
    if recordsPrint:
        html_content += "<table class='table table-striped table-bordered border-top' style=''>"
        html_content += "<thead><tr>"
        html_content += "<th>Folder</th>"
        html_content += "<th>Image</th>"
        html_content += "<th>Traitement</th>"
        html_content += "<th>QCote</th>"
        html_content += "<th>Type</th>"
        html_content += "<th>Anomalie</th>"
        html_content += "<th>Réponse</th>"
        html_content += "<th>Action</th>"
        html_content += "</tr></thead>"
        html_content += "<tbody>"
        for row in recordsPrint:
            row_dict = dict(zip([column[0] for column in cursor.description], row))
            html_content += "<tr>"
            for column_name in [
                "Folder", "z001_x0", "traitement", "QCote", "u990_b", "u990_c", "Ano_AnsCode"
            ]:
                    html_content += "<td>" + str(row_dict.get(column_name, "")) + "</td>"
            row_id = row_dict.get("Rows", "")
            html_content += f"<td><a href='form-edit?list={row_id}' class='btn-sm btn-primary'><i class='fa-solid fa-edit'></i></a></td>"
            html_content += "</tr>"
        html_content += "</tbody></table>"
    else:
        html_content += "<p>No records found</p>"

    # Close the cursor and connection
    cursor.close()
    cnxn.close()
    return render_template(
        "base2.html",
        page_no=page_no,
        total_no_of_pages=total_no_of_pages,
        total_records=total_records,
        html_content=html_content,
        html_content_fil=html_content_fil,
        process=process,
        anotype=anotype
    )


@app.route("/base")
def renderBase():
    return render_template("base.html")


@app.route("/render")
def renderTemplate():
    return render_template("table-export.html", now=datetime.utcnow())


@app.route("/dashboard")
def renderDashboard():
    return render_template("hometest.html", now=datetime.utcnow())


@app.route("/roi")
def renderROI():
    return render_template("roi.html")


# @app.route("/base")
# def renderBase():
#    return render_template("base.html")


@app.route("/get_suggestions", methods=["POST"])
def get_suggestions():
    try:
        data = request.get_json()

        user_input = data.get("user_input", "")

        library = [
            "Abel",
            "Abraham",
            "Achille",
            "Adel",
            "Ademar",
            "Adhemar",
            "Adolf",
            "Adrien",
            "Agénor",
            "Aimé",
            "Alain",
            "Albert",
            "Albertet",
            "Alexandre",
            "Alexis",
            "Alfred",
            "Allain",
            "Alphonse",
            "Alphonse Joseph",
            "Alvin",
            "Amable",
            "Amédée",
            "Anatole",
            "André",
            "André-Marie",
            "Ange",
            "Anicet",
            "Antoine",
            "Anton",
            "Antonin",
            "Armand",
            "Arnaud",
            "Arnaut",
            "Arsène",
            "Arthur",
            "Aubin",
            "Auguste",
            "Augustin",
            "Aurèle",
            "Aurélien",
            "Aymard",
            "Aymeric",
            "Balthazar",
            "Baptiste",
            "Barthélemy",
            "Bastien",
            "Baudouin",
            "Benjamin",
            "Benoît",
            "Bernard",
            "Bertrand",
            "Blanchard",
            "Bruno",
            "Calixte",
            "Calvin",
            "Camille",
            "Camille Alphonse",
            "Candide",
            "Carolus",
            "Cédric",
            "Celestin",
            "Cesar",
            "Charle",
            "Charles",
            "Charles-Édouard",
            "Charlot",
            "Christian",
            "Christophe",
            "Claude",
            "Claude-Henri",
            "Clement",
            "Clovis",
            "Constant",
            "Cyrille",
            "Damien",
            "Daniel",
            "Danton",
            "David",
            "Delbert",
            "Denis",
            "Désiré",
            "Didier",
            "Dieudonné",
            "Dominique",
            "Donatien",
            "Edgar",
            "Edgard",
            "Edmé",
            "Edmond",
            "Édouard",
            "Élie",
            "Élisée",
            "Émile",
            "Émilien",
            "Emmanuel",
            "Éric",
            "Ernest",
            "Erwan",
            "Étienne",
            "Fabien",
            "Fabrice",
            "Félicien",
            "Felix",
            "Ferdinand",
            "Fernand",
            "Flavien",
            "Fleury",
            "Florent",
            "Florian",
            "Florimond",
            "Francis",
            "Franck",
            "François",
            "François-Marie",
            "François-Xavier",
            "Frank",
            "Frédéric",
            "Fulbert",
            "Fulgence",
            "Gabriel",
            "Gaël",
            "Gaillard",
            "Gaspard",
            "Gaston",
            "Gédéon",
            "Geoffrey",
            "Georges",
            "Gérald",
            "Gérard",
            "Gerbaud",
            "Germain",
            "Ghislain",
            "Gilbert",
            "Gilles",
            "Godfrey",
            "Grégoire",
            "Guillaume",
            "Guy",
            "Hadrien",
            "Harold",
            "Hector",
            "Henri",
            "Herbert",
            "Hervé",
            "Hilaire",
            "Hippolyte",
            "Honoré",
            "Horace",
            "Hubert",
            "Hugo",
            "Hugues",
            "Hyacinthe",
            "Ignace",
            "Isidore",
            "Ivo",
            "Jacquelin",
            "Jacques",
            "Jacques-Désiré",
            "Jacques-Marie",
            "Jacquet",
            "James",
            "Jean",
            "Jean-André",
            "Jean-Antoine",
            "Jean-Baptiste",
            "Jean-Baptiste-Alphonse",
            "Jean-Bernard",
            "Jean-Charles",
            "Jean-Christophe",
            "Jean-Claude",
            "Jean-Denis",
            "Jean-Emmanuel",
            "Jean-Étienne",
            "Jean-François",
            "Jean-Guy",
            "Jean-Henri",
            "Jean-Jacques",
            "Jean-Joseph",
            "Jean-Julien",
            "Jean-Louis",
            "Jean-Luc",
            "Jean-Marc",
            "Jean-Marie",
            "Jean-Martin",
            "Jean-Michel",
            "Jean-Nicolas",
            "Jean-Noël",
            "Jean-Pascal",
            "Jean-Paul",
            "Jean-Philippe",
            "Jean-Pierre",
            "Jean-René",
            "Jean-Robert",
            "Jean-Sébastien",
            "Jean-Yves",
            "Jérémie",
            "Jérémy",
            "Jerome",
            "Joël",
            "Jonathan",
            "Jules",
            "Julien",
            "Julien-Joseph",
            "Just",
            "Justin",
            "Lauren",
            "Laurence",
            "Laurent",
            "Lazare",
            "Léandre",
            "Léo",
            "Leon",
            "Léon",
            "Loïc",
            "Lothaire",
            "Louis",
            "Louis-Alphonse",
            "Louis-Étienne",
            "Loup",
            "Luc",
            "Lucas",
            "Lucien",
            "Ludo",
            "Ludovic",
            "Mainard",
            "Manuel",
            "Marc",
            "Marc-André",
            "Marcel",
            "Marcellin",
            "Marco",
            "Mario",
            "Martin",
            "Mathieu",
            "Matthias",
            "Matthieu",
            "Maurice",
            "Maurille",
            "Maxence",
            "Maxime",
            "Maximilien",
            "Maynard",
            "Medard",
            "Melvin",
            "Michel",
            "Michel-Ange",
            "Mikaël",
            "Moise",
            "Napoleon",
            "Nicodème",
            "Nicolas",
            "Noe",
            "Noel",
            "Norbert",
            "Odilon",
            "Olivier",
            "Pacôme",
            "Pascal",
            "Patrice",
            "Patrick",
            "Paul",
            "Paul-Antoine",
            "Paul-Louis",
            "Paul-Marie",
            "Philibert",
            "Philippe",
            "Phillippe",
            "Pierre",
            "Pierre-Édouard",
            "Pierre-Julien",
            "Pierre-Marie",
            "Pierre-Paul",
            "Pierre-Simon",
            "Pierre-Yves",
            "Pierrick",
            "Profiat",
            "Prosper",
            "Quentin",
            "Raimond",
            "Rainier",
            "Raoul",
            "Raphael",
            "Raymond",
            "Réal",
            "Réjean",
            "Rémy",
            "René",
            "Reynald",
            "Robert",
            "Roger",
            "Roland",
            "Romain",
            "Roman",
            "Roméo",
            "Romuald",
            "Salome",
            "Samuel",
            "Sébastien",
            "Ségolène",
            "Seraphin",
            "Servais",
            "Severin",
            "Simon",
            "Stéphane",
            "Stéphen",
            "Sylvain",
            "Sylvestre",
            "Tancrède",
            "Théodore",
            "Théodule",
            "Thibaut",
            "Thierry",
            "Thomas",
            "Timothée",
            "Titouan",
            "Toussaint",
            "Ulysse",
            "Valentin",
            "Vianney",
            "Victor",
            "Vincent",
            "Virgile",
            "Xavier",
            "Yacine",
            "Yann",
            "Yannick",
            "Yvan",
            "Yves",
            "Yvon",
            "Zacharie",
        ]

        # Get a list of suggestions with their scores
        suggestions_with_scores = process.extract(user_input, library, limit=5)

        # Filter out suggestions with a score below a certain threshold (e.g., 70)
        filtered_suggestions = [
            suggestion for suggestion, score in suggestions_with_scores if score >= 70
        ]

        return jsonify({"suggestions": filtered_suggestions})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/form-edit", methods=["GET", "POST"])
def edit_form():
    # Establish database connection
    listpage_no = session.get('listpage_no', 1)
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    if not session['name']:
        return index()
    try:
        # Fetching page number from query params with a default value of 1
        list_no = request.args.get('list', 1)
        list_prev = int(request.args.get('list', 1))-1
        list_next = int(request.args.get('list', 1))+1
        sort = session.get('sort', 'order by z001_x0')
        sortype = session.get('sortype', 'ASC')
        params = session.get('params', [])
        # params = params.append(list_no)
        # Prepare SQL query using session values with safe parameter insertion
        # Ensure params is a list
        if not isinstance(params, list):
            params = []
        params.append(list_no)
        sql_query2 = session.get('sql_query2', """
            SELECT *, 
            Row_Number() Over ({sort} {sortype}) AS Rows 
            FROM dbo._unimarc 
            WHERE Proj = 'CAEN'
        """.format(sort=sort, sortype=sortype))

        query = f"""
            WITH object_rows AS ({sql_query2})
            SELECT * FROM object_rows WHERE Rows = ?
        """

        print(query)
        print(params)
        
        cursor.execute(query,params)        

        row = cursor.fetchone()

        if row:
            # Map row values to variables
            recid = int(row[1]) if row[1] is not None else ""
            proj = str(row[4]) if row[4] is not None else ""
            dossier = row[5] if row[5] is not None else ""
            image = row[2] if row[2] is not None else ""
            traitement = row[3] if row[3] is not None else ""
            qcote = row[13] if row[13] is not None else ""
            txtBrut = row[11] if row[11] is not None else ""
            ano = row[109] if row[109] is not None else ""
            anscode = row[110] if row[110] is not None else ""
            anocode = row[125] if row[125] is not None else ""
            anoanswer = row[126] if row[126] is not None else ""
            readable = row[119] if row[119] is not None else ""
            # Use regex to find all URLs
            site_url=''

            if readable:
                urls = re.findall(r'(https?://\S+)', readable)
            
            if urls:
                for url in urls:
                    site_url = url
                    # If you want to process only the first URL, you can break the loop
                    break

            # api_key = "a77d51086fb7455dbc9b8284573e7feb"
            # endpoint = "https://aurexusformprocessocr.cognitiveservices.azure.com/"

            # Initialize the Form Recognizer client
            # document_analysis_client = DocumentAnalysisClient(
            #     endpoint=endpoint, credential=AzureKeyCredential(api_key)
            # )

            # response = requests.get(f"https://aurexus.net/auximages/CAEN/{dossier}/{image}")
            # image_data = response.content

            # Analyze the image
            # poller = document_analysis_client.begin_analyze_document(
            #     "prebuilt-document", document=image_data
            # )
            # result = poller.result()

            # Print the extracted content
            # for page in result.pages:
            #     for line in page.lines:
            #         print(line.content)

            # Render the template with the fetched data
            return render_template(
                "form-edit.html",
                proj = proj,
                recid = recid,
                dossier = dossier,
                image = image,
                traitement = traitement,
                qcote = qcote,
                txtBrut = txtBrut,
                ano = ano,
                anoanswer = anoanswer,
                anscode = anscode,
                anocode = anocode,
                readable = readable,
                image_link = f"https://aurexus.net/auximages/CAEN/{dossier}/{image}",
                listpage_no = listpage_no,
                list_prev = list_prev,
                list_next = list_next,
                site_url=site_url
                
            )
        else:
            # Handle case where no row is found
            return "No data found for the specified page number.", 404

    except Exception as e:
        # Handle any other exceptions
        return str(e), 500

    finally:
        # Ensure the connection is closed
        cursor.close()
        cnxn.close()     

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    data = request.json    
    image = data.get('image')

    if  not image:
        return jsonify({"error": "dossier and image are required"}), 400

    try:
        response = requests.get(image)
        image_data = response.content

        # Analyze the image
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-document", document=image_data
        )
        result = poller.result()

        # Extract and return the content
        extracted_content = []
        for page in result.pages:
            for line in page.lines:
                extracted_content.append(line.content)

        return jsonify({"content": extracted_content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logout')
def logout():
    # session.pop('name', None)    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
