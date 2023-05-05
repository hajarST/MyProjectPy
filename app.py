from flask import Flask, render_template, flash, redirect, url_for, session, request, logging , jsonify , Response
from flaskext.mysql import MySQL
import pymysql
import io
import csv
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from fpdf import FPDF
 
app = Flask(__name__)
app.secret_key = "Cairocoders-Ednalan"  # clés secrete de session
  
mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'stock'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
  
# Register Form Class
'''class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
 '''
# Article Form Class
class ArticleForm(Form):
    nom_Produit = StringField('Nom_Produit', [validators.Length(min=1, max=200)]) #kant title  ('Title)
    #body = TextAreaField('Body', [validators.Length(min=30)])
    prix = StringField('Prix', [validators.Length(min=1, max=200)])
  
# Index
@app.route('/')
def index():
    return render_template('home.html')
  
# About
@app.route('/about')
def about():
    return render_template('about.html')
""" 
# Articles ca marche 
@app.route('/articles')
def produits():
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    # Get articles
    result = cur.execute("SELECT * FROM produit")
    produits = cur.fetchall()
    if result > 0:
        return render_template('articles.html', produits=produits)
    else:
        msg = 'Aucun article trouvé'
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()
 
#Single Article
@app.route('/article/<string:Id_Produit>/')
def article(id):
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    # Get article
    result = cur.execute("SELECT * FROM produit WHERE Id_Produit = %s", [id])
    article = cur.fetchone()
    return render_template('article.html', article=article)
    """
'''
# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
          
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        # Execute query
        cur.execute("INSERT INTO user_flask(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
        # Commit to DB
        conn.commit()
        # Close connection
        cur.close()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
 ''' 
# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        #Nom_Utilisateur = request.form['Nom_Utilisateur'] # ou bien request.form.get('Nom_Utilisateur')
        #password_candidate = request.form['Mot_De_Passe']
        Nom_Utilisateur = request.form.get('Nom_Utilisateur')
        password_candidate = request.form.get('Mot_De_Passe')


        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
  
        # Get user by username
        result = cur.execute("SELECT * FROM utilisateur WHERE Nom_Utilisateur = %s", [Nom_Utilisateur])
  
        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            #password = data['password']
            password = sha256_crypt.encrypt(str(data['Mot_De_Passe']))
            #LIGNE 118 erreur   password = sha256_crypt.encrypt(str(form.password.data))
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['Nom_Utilisateur'] = Nom_Utilisateur
  
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
  
    return render_template('login.html')
 
# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
    #def wrap(*args, wrap_argument=False, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
            #return f(*args,wrap_argument=False, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
 
# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))
  
# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur1 = conn.cursor(pymysql.cursors.DictCursor)
    cur2 = conn.cursor(pymysql.cursors.DictCursor)
    # Get articles
    #result = cur.execute("SELECT * FROM articles")
    # Show articles only from the user logged in 
    #result = cur.execute("SELECT * FROM produit WHERE author = %s", [session['Nom_Utilisateur']])
    #result = 
    cur.execute("SELECT COUNT(*) as nbr FROM client")
    cur1.execute("SELECT COUNT(*) as nbr FROM fournisseur")
    cur2.execute("SELECT COUNT(*) as nbr FROM produit")
    clients = cur.fetchone()
    fournisseurs = cur1.fetchone() 
    produits = cur2.fetchone()
    #if result > 0:
    return render_template('dashboard.html', clients=clients,fournisseurs=fournisseurs,produits=produits)
   # else:
       # msg = 'No Client Found'
        #return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()
#**********************************************************************************************************************************************
#categorie hajar hajar
@app.route('/categories')
def categories():
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    # Get articles
    result = cur.execute("SELECT * FROM categorie")
    categories = cur.fetchall()

        
    if result > 0:
        return render_template('categories.html',  categories=categories)
    else:
        msg = 'Aucun categorie trouvé'
        return render_template('categories.html', msg=msg)
    # Close connection
    cur.close()


@app.route('/add_categorie', methods=['POST'])
def add_categorie():
    conn = mysql.connect()
    cur0 = conn.cursor(pymysql.cursors.DictCursor)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        Id_Categorie = request.form['Id_Categorie']
        Nom_Categorie = request.form['Nom_Categorie']
    var = cur0.execute("SELECT Id_Categorie from categorie where Id_Categorie = %s",Id_Categorie)
    if var==0:
        cur.execute("INSERT INTO categorie ( Id_Categorie , Nom_Categorie ) VALUES (%s,%s)", (Id_Categorie,Nom_Categorie))
        conn.commit()
        flash('Categorie ajouté avec succés')
    else:
        flash('Categorie existe déjà')
    return redirect(url_for('categories'))
 
@app.route('/edit_categorie/<id>', methods = ['POST', 'GET'])
def get_categorie(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM categorie WHERE Id_Categorie = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_categorie.html', categorie = data[0])
 
@app.route('/update_categorie/<id>', methods=['GET', 'POST'])
def update_categorie(id):
    if request.method == 'POST':
        #Id_Client = request.form['Id_Client']
        Nom_Categorie = request.form['Nom_Categorie']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("UPDATE categorie SET Nom_Categorie = %s  where Id_Categorie = %s", (Nom_Categorie, id))
        flash('Categorie modifiée avec succés')
        conn.commit()
        return redirect(url_for('categories'))
 
@app.route('/delete_categorie/<string:id>', methods = ['POST','GET'])
def delete_categorie(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute("DELETE FROM categorie WHERE Id_Categorie = %s",(id))
    conn.commit()
    flash('Categorie supprimée avec succés')
    return redirect(url_for('produits'))




#**********************************************************************************************************************************************
#produit hajar hajar
@app.route('/produits')
def produits():
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    # Get articles
    result = cur.execute("SELECT * FROM produit")
    produits = cur.fetchall()

    
    cur2 = conn.cursor(pymysql.cursors.DictCursor)
  
    # Get articles
    cur2.execute("SELECT Id_Categorie,Nom_Categorie FROM categorie")
    categories = cur2.fetchall()
        
    if result > 0:
        return render_template('produits.html', produits=produits, categories=categories)
    else:
        msg = 'Aucun produit trouvé'
        return render_template('produits.html', msg=msg)
    # Close connection
    cur.close()


#repport produits
def downloadPdt():
  #return render_template('download_csv_client.html')
    return render_template('produits.html')
@app.route('/download/report/csvPdt')
def download_report_Pdt():
 conn = None
 cursor = None
 try:
  conn = mysql.connect()
  cursor = conn.cursor(pymysql.cursors.DictCursor)
   
  cursor.execute("SELECT Id_Produit,Nom_Produit,Quantite,Prix,Id_Categorie  FROM produit")
  result = cursor.fetchall()
 
  output = io.StringIO()
  writer = csv.writer(output)
   
  line = ['Id, Nom, Quantite, Prix, Categorie ']
  writer.writerow(line)
 
  for row in result:
   line = [str(row['Id_Produit']) + ',' + row['Nom_Produit'] + ',' + str(row['Quantite']) + ',' + str(row['Prix']) + ',' + str(row['Id_Categorie'])]
   writer.writerow(line)
 
  output.seek(0)
   
  return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=Produits_report.csv"})
 except Exception as e:
  print(e)
 finally:
  cursor.close() 
  conn.close()

@app.route('/add_produit', methods=['POST'])
def add_produit():
    conn = mysql.connect()
    cur0 = conn.cursor(pymysql.cursors.DictCursor)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        Id_Produit = request.form['Id_Produit']
        Nom_Produit = request.form['Nom_Produit']
        Quantite = request.form['Quantite']
        Prix = request.form['Prix']
        Id_Categorie = request.form['Id_Categorie']
    var = cur0.execute("SELECT Id_Produit from produit where Id_Produit = %s",Id_Produit)
    if var==0:
        cur.execute("INSERT INTO produit (Id_Produit,Nom_Produit, Quantite , Prix , Id_Categorie ) VALUES (%s,%s,%s,%s,%s)", (Id_Produit, Nom_Produit, Quantite,Prix,Id_Categorie))
        conn.commit()
        flash('Produit ajouté avec succés')
    else:
        flash('Produit existe déjà')
    return redirect(url_for('produits'))
 
@app.route('/edit_produit/<id>', methods = ['POST', 'GET'])
def get_produit(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM produit WHERE Id_Produit = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_produit.html', produit = data[0])
 
@app.route('/update_produit/<id>', methods=['GET', 'POST'])
def update_produit(id):
    if request.method == 'POST':
        #Id_Client = request.form['Id_Client']
        Nom_Produit = request.form['Nom_Produit']
        Quantite = request.form['Quantite']
        Prix = request.form['Prix']
        Id_Categorie = request.form['Id_Categorie']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("UPDATE produit SET Nom_Produit = %s , Quantite = %s , Prix = %s , Id_Categorie = %s  WHERE Id_Produit = %s", (Nom_Produit, Quantite, Prix,Id_Categorie, id))
        flash('Produit modifié avec succés')
        conn.commit()
        return redirect(url_for('produits'))
 
@app.route('/delete_produit/<string:id>', methods = ['POST','GET'])
def delete_produit(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
   #cur.execute("DELETE FROM client WHERE Id_Client = {0}".format(id))
    cur.execute("DELETE FROM produit WHERE Id_Produit = %s",(id))
    conn.commit()
    flash('Produit supprimé avec succés')
    return redirect(url_for('produits'))



    
 #******************************************************************************************************************************************
  
#client hajar hajar
@app.route('/clients')
def clients():
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    # Get articles
    result = cur.execute("SELECT * FROM client")
    clients = cur.fetchall()
    if result > 0:
        return render_template('clients.html', clients=clients)
    else:
        msg = 'Aucun client trouvé'
        return render_template('clients.html', msg=msg)
    # Close connection
    cur.close()

#repport clients
def download():
  #return render_template('download_csv_client.html')
    return render_template('clients.html')
@app.route('/download/report/csvClt')
def download_report():
 conn = None
 cursor = None
 try:
  conn = mysql.connect()
  cursor = conn.cursor(pymysql.cursors.DictCursor)
   
  cursor.execute("SELECT Id_Client, Nom_Client, Prenom_Client, Adresse_Client , Telephone_Client , Email_Client FROM client")
  result = cursor.fetchall()
 
  output = io.StringIO()
  writer = csv.writer(output)
   
  line = ['Id, Nom, Prenom, Adresse, Telephone , Email']
  writer.writerow(line)
 
  for row in result:
   line = [str(row['Id_Client']) + ',' + row['Nom_Client'] + ',' + row['Prenom_Client'] + ',' + row['Adresse_Client'] + ',' + row['Telephone_Client']+ ',' + row['Email_Client']]
   writer.writerow(line)
 
  output.seek(0)
   
  return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=Clients_report.csv"})
 except Exception as e:
  print(e)
 finally:
  cursor.close() 
  conn.close()
#

@app.route('/add_client', methods=['POST'])
def add_client():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur0 = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        Id_Client = request.form['Id_Client']
        Nom_Client = request.form['Nom_Client']
        Prenom_Client = request.form['Prenom_Client']
        Adresse_Client = request.form['Adresse_Client']
        Telephone_Client = request.form['Telephone_Client']
        Email_Client = request.form['Email_Client']
    var =cur0.execute("Select Id_Client from client where Id_Client = %s ",Id_Client)

    if var==0:
        cur.execute("INSERT INTO client (Id_Client,Nom_Client, Prenom_Client , Adresse_Client , Telephone_Client , Email_Client) VALUES (%s,%s,%s,%s,%s,%s)", (Id_Client, Nom_Client, Prenom_Client,Adresse_Client,Telephone_Client,Email_Client))
        conn.commit()
        flash('Client Added successfully')
    else:
        flash('Client existe déjà')
    return redirect(url_for('clients'))

#
@app.route('/edit_client/<id>', methods = ['POST', 'GET'])
def get_client(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM client WHERE Id_Client = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_client.html', client = data[0])
 
@app.route('/update_client/<id>', methods=['GET', 'POST'])
def update_client(id):
    if request.method == 'POST':
        #Id_Client = request.form['Id_Client']
        Nom_Client = request.form['Nom_Client']
        Prenom_Client = request.form['Prenom_Client']
        Adresse_Client = request.form['Adresse_Client']
        Telephone_Client = request.form['Telephone_Client']
        Email_Client = request.form['Email_Client']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("UPDATE client SET Nom_Client = %s , Prenom_Client = %s , Adresse_Client = %s , Telephone_Client = %s , Email_Client = %s WHERE Id_Client = %s", (Nom_Client, Prenom_Client, Adresse_Client,Telephone_Client,Email_Client , id))
        flash('Client Updated Successfully')
        conn.commit()
        return redirect(url_for('clients'))
 
@app.route('/delete_client/<string:id>', methods = ['POST','GET'])
def delete_client(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
   #cur.execute("DELETE FROM client WHERE Id_Client = {0}".format(id))
    cur.execute("DELETE FROM client WHERE Id_Client = %s",(id))
    conn.commit()
    flash('Client Removed Successfully')
    return redirect(url_for('clients'))
 #******************************************************************************************************************************************

 #fournisseur hajar hajar
@app.route('/fournisseurs')
def fournisseurs():
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    # Get articles
    result = cur.execute("SELECT * FROM fournisseur")
    fournisseurs = cur.fetchall()
    if result > 0:
        return render_template('fournisseurs.html', fournisseurs=fournisseurs)
    else:
        msg = 'Aucun fournisseur trouvé'
        return render_template('fournisseurs.html', msg=msg)
    # Close connection
    cur.close()

#repport fournisseurs
def downloadFrns():
  #return render_template('download_csv_client.html')
    return render_template('fournisseurs.html')
@app.route('/download/report/csvFrns')
def download_report_Frns():
 conn = None
 cursor = None
 try:
  conn = mysql.connect()
  cursor = conn.cursor(pymysql.cursors.DictCursor)
   
  cursor.execute("SELECT Id_Fournisseur,Nom_Fournisseur,Prenom_Fournisseur,Adresse_Fournisseur,Telephone_Fournisseur,Email_Fournisseur  FROM fournisseur")
  result = cursor.fetchall()
 
  output = io.StringIO()
  writer = csv.writer(output)
   
  line = ['Id, Nom, Prenom, Adresse, Telephone , Email ']
  writer.writerow(line)
 
  for row in result:
   line = [str(row['Id_Fournisseur']) + ',' + row['Nom_Fournisseur'] + ',' + row['Prenom_Fournisseur'] + ',' + row['Adresse_Fournisseur'] + ',' + row['Telephone_Fournisseur']+ ',' + row['Email_Fournisseur']]
   writer.writerow(line)
 
  output.seek(0)
   
  return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=Fournisseurs_report.csv"})
 except Exception as e:
  print(e)
 finally:
  cursor.close() 
  conn.close()


@app.route('/add_fournisseur', methods=['POST'])
def add_fournisseur():
    conn = mysql.connect()
    cur0 = conn.cursor(pymysql.cursors.DictCursor)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        Id_Fournisseur = request.form['Id_Fournisseur']
        Nom_Fournisseur = request.form['Nom_Fournisseur']
        Prenom_Fournisseur = request.form['Prenom_Fournisseur']
        Adresse_Fournisseur = request.form['Adresse_Fournisseur']
        Telephone_Fournisseur = request.form['Telephone_Fournisseur']
        Email_Fournisseur = request.form['Email_Fournisseur']
    var = cur0.execute("SELECT Id_Fournisseur from fournisseur where Id_Fournisseur = %s",Id_Fournisseur)
    if var == 0:
        cur.execute("INSERT INTO fournisseur (Id_Fournisseur,Nom_Fournisseur, Prenom_Fournisseur , Adresse_Fournisseur , Telephone_Fournisseur , Email_Fournisseur) VALUES (%s,%s,%s,%s,%s,%s)", (Id_Fournisseur, Nom_Fournisseur, Prenom_Fournisseur,Adresse_Fournisseur,Telephone_Fournisseur,Email_Fournisseur))
        conn.commit()
        flash('Fournisseur bien ajouté')
    else:
        flash('Fournisseur existe déjà')
    return redirect(url_for('fournisseurs'))
 
@app.route('/edit_fournisseur/<id>', methods = ['POST', 'GET'])
def get_fournisseur(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM fournisseur WHERE Id_Fournisseur = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_fournisseur.html', fournisseur = data[0])
 
@app.route('/update_fournisseur/<id>', methods=['GET', 'POST'])
def update_fournisseur(id):
    if request.method == 'POST':
        #Id_Client = request.form['Id_Client']
        Nom_Fournisseur = request.form['Nom_Fournisseur']
        Prenom_Fournisseur = request.form['Prenom_Fournisseur']
        Adresse_Fournisseur = request.form['Adresse_Fournisseur']
        Telephone_Fournisseur = request.form['Telephone_Fournisseur']
        Email_Fournisseur = request.form['Email_Fournisseur']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("UPDATE fournisseur SET Nom_Fournisseur = %s , Prenom_Fournisseur = %s , Adresse_Fournisseur = %s , Telephone_Fournisseur = %s , Email_Fournisseur = %s WHERE Id_Fournisseur = %s", (Nom_Fournisseur, Prenom_Fournisseur, Adresse_Fournisseur,Telephone_Fournisseur,Email_Fournisseur , id))
        flash('Fournisseur modifié avec succés')
        conn.commit()
        return redirect(url_for('fournisseurs'))
 
@app.route('/delete_fournisseur/<string:id>', methods = ['POST','GET'])
def delete_fournisseur(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
   #cur.execute("DELETE FROM client WHERE Id_Client = {0}".format(id))
    cur.execute("DELETE FROM fournisseur WHERE Id_Fournisseur = %s",(id))
    conn.commit()
    flash('Fournisseur supprimé avec succés')
    return redirect(url_for('fournisseurs'))

#search fournisseur
@app.route("/searchdatafrns",methods=["POST","GET"])
def searchdatafrns():
    if request.method == 'POST':
        search_word = request.form['search_word']
        print(search_word)
        cur = mysql.connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * from fournisseur WHERE Nom_Fournisseur LIKE '%{}%' ORDER BY Id_Fournisseur DESC LIMIT 20".format(search_word)
        cur.execute(query)
        fournisseur = cur.fetchall()
    return jsonify({'data': render_template('responsefrns.html', fournisseur=fournisseur)})
#********************************************************************************************************************************************
#**********************************************************************************************************************************************
#commande achat hajar hajar
@app.route('/commandeAchat')
def commandeAchat():
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur1 = conn.cursor(pymysql.cursors.DictCursor)
    cur2 = conn.cursor(pymysql.cursors.DictCursor)
    # Get articles
    result = cur.execute("SELECT * FROM commande_achat")
    commandeAchat = cur.fetchall()
    cur1.execute("SELECT Id_Produit,Nom_Produit  FROM produit")
    cur2.execute("SELECT Id_Fournisseur,Nom_Fournisseur ,Prenom_Fournisseur FROM fournisseur")
    produits =cur1.fetchall()
    fournisseurs = cur2.fetchall()   
    if result > 0:
        return render_template('commandeAchat.html', commandeAchat=commandeAchat,produits=produits,fournisseurs=fournisseurs)
    else:
        msg = 'Aucune commande achat trouvée'
        return render_template('commandeAchat.html', msg=msg)
    # Close connection
    cur.close()


#PDF REPORT achat

@app.route('/download/report/pdf')
def download_report_Cmd_Achat():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
         
        cursor.execute("SELECT * FROM commande_achat")
        result = cursor.fetchall()
 
        pdf = FPDF()
        pdf.add_page()
         
        page_width = pdf.w - 2 * pdf.l_margin
         
        pdf.set_font('Times','B',14.0) 
        pdf.cell(page_width, 0.0, 'commande_achat Data', align='C')
        pdf.ln(7)
 
        pdf.set_font('Courier', '', 12)
         
        col_width = page_width/6
         
        pdf.ln(1)
         
        th = pdf.font_size
         
        for row in result:
            pdf.cell(col_width, th, str(row['Id_Commande_Achat']), border=1)
            
            pdf.cell(col_width, th, str(row['Id_Produit']), border=1)
            pdf.cell(col_width, th, str(row['Date_Commande_Achat']), border=1)
            pdf.cell(col_width, th, row['Id_Fournisseur'], border=1)
            pdf.cell(col_width, th, str(row['Quantite_A_Acheter']), border=1)
            pdf.cell(col_width, th, str(row['TOTAL_HT']), border=1)
            pdf.cell(col_width, th, str(row['TVA']), border=1)
            pdf.ln(th)
         
        pdf.ln(10)
         
        pdf.set_font('Times','',10.0) 
        pdf.cell(page_width, 0.0, '- end of report -', align='C')
         
        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=Commande_Achat_report.pdf'})
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


@app.route('/add_Cmd_Achat', methods=['POST'])
def add_Cmd_Achat():
    conn = mysql.connect()
    cur0 = conn.cursor(pymysql.cursors.DictCursor)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        Id_Commande_Achat = request.form['Id_Commande_Achat']
        Id_Produit = request.form['Id_Produit']
        Date_Commande_Achat = request.form['Date_Commande_Achat']
        Id_Fournisseur = request.form['Id_Fournisseur']
        Quantite_A_Acheter = request.form['Quantite_A_Acheter']
        TOTAL_HT = request.form['TOTAL_HT']
        TVA = request.form['TVA']
    
    
    var = cur0.execute("SELECT Id_Commande_Achat,Id_Produit from commande_achat where Id_Commande_Achat = %s and Id_Produit = %s",(Id_Commande_Achat,Id_Produit))
    if var==0:
        cur.execute("INSERT INTO commande_achat (Id_Commande_Achat,Id_Produit,Date_Commande_Achat, Id_Fournisseur , Quantite_A_Acheter, TOTAL_HT , TVA ) VALUES (%s,%s,%s,%s,%s,%s,%s)", (Id_Commande_Achat,Id_Produit, Date_Commande_Achat, Id_Fournisseur,Quantite_A_Acheter,TOTAL_HT,TVA))
        conn.commit()
        flash('Commande achat ajouté avec succés')
    else:
        flash('Commande achat existe déjà')
    return redirect(url_for('commandeAchat'))

@app.route('/edit_commande_achat/<id>', methods = ['POST', 'GET'])
def get_commande_achat(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM commande_achat WHERE Id_Commande_Achat = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_commande_achat.html', commandeAchat = data[0])

@app.route('/update_commande_achat/<id>', methods=['GET', 'POST'])
def update_commande_achat(id):
    if request.method == 'POST':
        #Id_Client = request.form['Id_Client']
        Id_Produit = request.form['Id_Produit']
        Date_Commande_Achat = request.form['Date_Commande_Achat']
        Id_Fournisseur = request.form['Id_Fournisseur']
        Quantite_A_Acheter = request.form['Quantite_A_Acheter']
        TOTAL_HT = request.form['TOTAL_HT']
        TVA = request.form['TVA']
        
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("UPDATE commande_achat SET Id_Produit = %s, Date_Commande_Achat = %s , Id_Fournisseur = %s,Quantite_A_Acheter = %s , TOTAL_HT = %s , TVA = %s   WHERE Id_Commande_Achat = %s ", (Id_Produit,Date_Commande_Achat, Id_Fournisseur, Quantite_A_Acheter,TOTAL_HT,TVA, id))
        flash('Commande modifié avec succés')
        conn.commit()
        return redirect(url_for('commandeAchat'))
 
@app.route('/delete_commande_achat/<string:id>', methods = ['POST','GET'])
def delete_commande_achat(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
   
    cur.execute("DELETE FROM commande_achat WHERE Id_Commande_Achat = %s",(id))
    conn.commit()
    flash('Commande achat supprimée avec succés')
    return redirect(url_for('commandeAchat'))
#********************************************************************************************************************************************
#**********************************************************************************************************************************************
#commande vente hajar hajar
@app.route('/commandeVente')
def commandeVente():
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur1 = conn.cursor(pymysql.cursors.DictCursor)
    cur2 = conn.cursor(pymysql.cursors.DictCursor)
    # Get articles
    result = cur.execute("SELECT * FROM commande_vente")
    commandeVente = cur.fetchall()
    cur1.execute("SELECT Id_Produit,Nom_Produit  FROM produit")
    cur2.execute("SELECT Id_Client,Nom_Client ,Prenom_Client FROM client")
    produits =cur1.fetchall()
    clients = cur2.fetchall()   
    if result > 0:
        return render_template('commandeVente.html', commandeVente=commandeVente,produits=produits,clients=clients)
    else:
        msg = 'Aucune commande vente trouvée'
        return render_template('commandeVente.html', msg=msg)
    # Close connection
    cur.close()


#PDF REPORT achat

@app.route('/download/report/pdfVente')
def download_report_Cmd_Vente():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
         
        cursor.execute("SELECT * FROM commande_vente")
        result = cursor.fetchall()
 
        pdf = FPDF()
        pdf.add_page()
         
        page_width = pdf.w - 2 * pdf.l_margin
         
        pdf.set_font('Times','B',14.0) 
        pdf.cell(page_width, 0.0, 'commande_vente Data', align='C')
        pdf.ln(7)
 
        pdf.set_font('Courier', '', 12)
         
        col_width = page_width/6
         
        pdf.ln(1)
         
        th = pdf.font_size
         
        for row in result:
            pdf.cell(col_width, th, str(row['Id_Commande_Vente']), border=1)
            
            pdf.cell(col_width, th, str(row['Id_Produit']), border=1)
            pdf.cell(col_width, th, str(row['Date_Commande_Vente']), border=1)
            pdf.cell(col_width, th, row['Id_Client'], border=1)
            pdf.cell(col_width, th, str(row['Quantite_A_Vendre']), border=1)
            pdf.cell(col_width, th, str(row['TOTAL_HT']), border=1)
            pdf.cell(col_width, th, str(row['TVA']), border=1)
            pdf.ln(th)
         
        pdf.ln(10)
         
        pdf.set_font('Times','',10.0) 
        pdf.cell(page_width, 0.0, '- end of report -', align='C')
         
        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=Commande_Vente_report.pdf'})
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


@app.route('/add_Cmd_Vente', methods=['POST'])
def add_Cmd_Vente():
    conn = mysql.connect()
    cur0 = conn.cursor(pymysql.cursors.DictCursor)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        Id_Commande_Vente = request.form['Id_Commande_Vente']
        Id_Produit = request.form['Id_Produit']
        Date_Commande_Achat = request.form['Date_Commande_Vente']
        Id_Client = request.form['Id_Client']
        Quantite_A_Vendre = request.form['Quantite_A_Vendre']
        TOTAL_HT = request.form['TOTAL_HT']
        TVA = request.form['TVA']
    var = cur0.execute("SELECT Id_Commande_Vente ,Id_Produit from commande_vente where Id_Commande_Vente = %s and Id_Produit = %s",(Id_Commande_Vente,Id_Produit))
    if var==0:
        cur.execute("INSERT INTO commande_vente (Id_Commande_Vente,Id_Produit,Date_Commande_Vente, Id_Client , Quantite_A_Vendre, TOTAL_HT , TVA ) VALUES (%s,%s,%s,%s,%s,%s,%s)", (Id_Commande_Vente,Id_Produit, Date_Commande_Achat, Id_Client,Quantite_A_Vendre,TOTAL_HT,TVA))
        conn.commit()
        flash('Commande achat ajouté avec succés')
    else:
        flash('Commande achat existe déjà')
    return redirect(url_for('commandeAchat'))

@app.route('/edit_commande_vente/<id>', methods = ['POST', 'GET'])
def get_commande_vente(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM commande_vente WHERE Id_Commande_Vente = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_commande_vente.html', commandeVente = data[0])

@app.route('/update_commande_vente/<id>', methods=['GET', 'POST'])
def update_commande_vente(id):
    if request.method == 'POST':
        #Id_Client = request.form['Id_Client']
        Id_Produit = request.form['Id_Produit']
        Date_Commande_Vente = request.form['Date_Commande_Vente']
        Id_Client = request.form['Id_Client']
        Quantite_A_Vendre = request.form['Quantite_A_Vendre']
        TOTAL_HT = request.form['TOTAL_HT']
        TVA = request.form['TVA']
        
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("UPDATE commande_vente SET Id_Produit = %s, Date_Commande_Vente = %s , Id_Client = %s,Quantite_A_Vendre = %s , TOTAL_HT = %s , TVA = %s   WHERE Id_Commande_Vente = %s ", (Id_Produit,Date_Commande_Vente, Id_Client, Quantite_A_Vendre,TOTAL_HT,TVA, id))
        flash('Commande modifié avec succés')
        conn.commit()
        return redirect(url_for('commandeVente'))
 
@app.route('/delete_commande_vente/<string:id>', methods = ['POST','GET'])
def delete_commande_vente(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
   
    cur.execute("DELETE FROM commande_vente WHERE Id_Commande_Vente = %s",(id))
    conn.commit()
    flash('Commande vente supprimée avec succés')
    return redirect(url_for('commandeVente'))
#********************************************************************************************************************************************
'''
#commande vente hajar hajar
@app.route('/commandeVente')
def commandeVente():
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur2 = conn.cursor(pymysql.cursors.DictCursor)
    # Get articles
    result = cur.execute("SELECT * FROM commande_vente")
    commandeVente = cur.fetchall()

    cur2.execute("SELECT Id_Client,Nom_Client ,Prenom_Client FROM client")
    clients = cur2.fetchall()   
    if result > 0:
        return render_template('commandeVente.html', commandeVente=commandeVente,clients=clients)
    else:
        msg = 'Aucune commande vente trouvée'
        return render_template('commandeVente.html', msg=msg)
    # Close connection
    cur.close()


#repport commande achat
def downloadCmdVente():
 
    return render_template('commandeVente.html')
@app.route('/download/report/csvCmdVente')
def download_report_Cmd_Vente():
 conn = None
 cursor = None
 try:
  conn = mysql.connect()
  cursor = conn.cursor(pymysql.cursors.DictCursor)
   
  cursor.execute("SELECT Id_Commande_Vente,Date_Commande_Vente,Id_Client,TOTAL_HT,TVA,TOTAL_TTC  FROM commande_vente")
  result = cursor.fetchall()
 
  output = io.StringIO()
  writer = csv.writer(output)
   
  line = ['Id, Date, Client, Prix HT, TVA , Prix TTC ']
  writer.writerow(line)
 
  for row in result:
   line = [str(row['Id_Commande_Vente']) + ',' + row['Date_Commande_Achat'] + ',' + row['Id_Client'] + ',' + str(row['TOTAL_HT']) + ',' + str(row['TVA'])+ ',' + str(row['TOTAL_TTC'])]
   writer.writerow(line)
 
  output.seek(0)
   
  return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=Commandes_Ventes_report.csv"})
 except Exception as e:
  print(e)
 finally:
  cursor.close() 
  conn.close()

@app.route('/download/report/pdfVente')
def download_report_Cmd_Vente():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
         
        cursor.execute("SELECT * FROM commande_vente")
        result = cursor.fetchall()
 
        pdf = FPDF()
        pdf.add_page()
         
        page_width = pdf.w - 2 * pdf.l_margin
         
        pdf.set_font('Times','B',14.0) 
        pdf.cell(page_width, 0.0, 'commande_vente Data', align='C')
        pdf.ln(7)
 
        pdf.set_font('Courier', '', 12)
         
        col_width = page_width/6
         
        pdf.ln(1)
         
        th = pdf.font_size
         
        for row in result:
            pdf.cell(col_width, th, str(row['Id_Commande_Vente']), border=1)
            pdf.cell(col_width, th, str(row['Date_Commande_Vente']), border=1)
            pdf.cell(col_width, th, row['Id_Client'], border=1)
            pdf.cell(col_width, th, str(row['TOTAL_HT']), border=1)
            pdf.cell(col_width, th, str(row['TVA']), border=1)
            pdf.cell(col_width, th, str(row['TOTAL_TTC']), border=1)
            pdf.ln(th)
         
        pdf.ln(10)
         
        pdf.set_font('Times','',10.0) 
        pdf.cell(page_width, 0.0, '- end of report -', align='C')
         
        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=Commande_Vente_report.pdf'})
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


@app.route('/add_Cmd_Vente', methods=['POST'])
def add_Cmd_Vente():
    conn = mysql.connect()
    cur0 = conn.cursor(pymysql.cursors.DictCursor)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        Id_Commande_Vente = request.form['Id_Commande_Vente']
        Date_Commande_Vente = request.form['Date_Commande_Vente']
        Id_Client= request.form['Id_Client']
        TOTAL_HT = request.form['TOTAL_HT']
        TVA = request.form['TVA']
        TOTAL_TTC = request.form['TOTAL_TTC']
    var = cur0.execute("SELECT Id_Commande_Vente from commande_vente where Id_Commande_Vente = %s",Id_Commande_Vente)
    if var==0:
        cur.execute("INSERT INTO commande_vente (Id_Commande_Vente, Date_Commande_Vente , Id_Client , TOTAL_HT , TVA , TOTAL_TTC) VALUES (%s,%s,%s,%s,%s,%s)", (Id_Commande_Vente,Date_Commande_Vente, Id_Client,TOTAL_HT,TVA,TOTAL_TTC))
        conn.commit()
        flash('Commande vente ajoutée avec succés')
    else:
        flash('Commande vente existe déjà')
    return redirect(url_for('commandeVente'))

@app.route('/edit_commande_vente/<id>', methods = ['POST', 'GET'])
def get_commande_vente(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM commande_vente WHERE Id_Commande_Vente = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_commande_vente.html', commandeVente = data[0])

@app.route('/update_commande_vente/<id>', methods=['GET', 'POST'])
def update_commande_vente(id):
    if request.method == 'POST':
        #Id_Client = request.form['Id_Client']
        Date_Commande_Vente = request.form['Date_Commande_Vente']
        Id_Client = request.form['Id_Client']
        TOTAL_HT = request.form['TOTAL_HT']
        TVA = request.form['TVA']
        TOTAL_TTC = request.form['TOTAL_TTC']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("UPDATE commande_vente SET Date_Commande_Vente = %s , Id_Client = %s , TOTAL_HT = %s , TVA = %s , TOTAL_TTC = %s  WHERE Id_Commande_Vente = %s ", (Date_Commande_Vente, Id_Client, TOTAL_HT,TVA,TOTAL_TTC, id))
        flash('Commande modifiée avec succés')
        conn.commit()
        return redirect(url_for('commandeVente'))
 
@app.route('/delete_commande_vente/<string:id>', methods = ['POST','GET'])
def delete_commande_vente(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
   
    cur.execute("DELETE FROM commande_vente WHERE Id_Commande_Vente = %s",(id))
    conn.commit()
    flash('Commande vente supprimée avec succés')
    return redirect(url_for('commandeVente'))
'''
#*********************************************************************************************************************************************

if __name__ == '__main__':
 app.run(debug=True)
#</string:id></string:id></string:id>