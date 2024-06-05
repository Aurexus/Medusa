# an object of WSGI application
from flask import Flask,render_template,jsonify
from PyZ3950 import zoom,z3950
import pyodbc
app = Flask(__name__)   # Flask constructor

# A decorator used to tell the application
# which URL is associated function
#cnxn_str = ("Driver={ODBC Driver 17 for SQL Server};Server=,1433;Database=AUREXDB1;Uid=db_su;Pwd='=!Aurexus21!=';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
server = 'tcp:aurexdb.database.windows.net,1433'
database = 'AUREXDB1'
username = 'db_su'
password = '=!Aurexus21!='

@app.route('/')      
def hello():
    return render_template('index.html')

@app.route('/table')
def datas(): 
    # Sudoc Connection Properties Checking
    conn = zoom.Connection("carmin.sudoc.abes.fr", 8859)
    
    # Set connection properties
    conn.databaseName = 'abes-z39-public'
    conn.preferredRecordSyntax='UNIMARC'
    if conn:
        print("Connection Establised!")
        try:
            # Create a CCL query for a specific title and author
            tit = "Recueil articles publiés"
            aut = "Barthes"
            query_string = '@and @attr 1=4 @attr 2=3 @attr 3=3 @attr 4=2 @attr 5=1 @attr 6=1 "+{}+" @attr 1=1003 @attr 2=3 @attr 3=3 @attr 4=2 @attr 5=100 @attr 6=1 "{}"'.format(tit, aut)
            query = zoom.Query('PQF', "@attr 2=4 Esmeralda")
            
            # Perform the search
            res = conn.search(query)            
            # Print the result of the first record
            return str(res[0])
            # print (type(res[0]))

        except Exception as e:
            print('Error: Problem in Fetching!')
            
    else:
        print("Connection Failed!")
        
        
    conn.close ()
    #return render_template('table-basic.html',data=data)
@app.route('/dbconnect')
def dbConnect(): 
    server = "tcp:aurexdb.database.windows.net,1433"
    database = 'AUREXDB1'
    username = 'db_su'
    password = "=!Aurexus21!="
    conn_str = f'Driver={ODBC Driver 17 for SQL Server};Server=,1433;Database=AUREXDB1;Uid=db_su;Pwd="=!Aurexus21!=";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT top(1) * FROM HUB_TEST")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # if cursor:
        # print("Connectin Establised")
    # else:
        # print("Problem Connect")
if __name__=='__main__':
   app.run()
