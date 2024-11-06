from flask import Flask,render_template,request, flash,redirect,url_for,session
import urllib.parse
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from Usuario import Usuario
from Hobby import Hobby

app = Flask(__name__)

app.secret_key = 's96y7d8asduissadtyaw78gh7ege67832gryuiasb78stgd678a'

user = "root"
password = urllib.parse.quote_plus("senac")
host = "localhost"
database = "hobbies"

connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

engine = create_engine(connection_string)

metadata = MetaData()
metadata.reflect(engine)
Base = automap_base(metadata=metadata)
Base.prepare()

Usuario = Base.classes.user
Hobby = Base.classes.hobby



Session = sessionmaker(bind=engine)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/registra')
def registra():
  return render_template('cadatraUsuario.html')

@app.route('/hobby')
def hobby():
    usuario_id = session.get('usuario_id') 
    if not usuario_id:
        flash('Você precisa estar logado para ver suas hobby.')
        return redirect(url_for('index'))

    session_db = Session()
    hobby_lista = []

    try:
        hobby_lista = session_db.query(Hobby).filter_by(usuario_id=usuario_id).all()
    except Exception as e:
        flash('Erro ao carregar as hobby: ' + str(e))
    finally:
        session_db.close()

    return render_template('listaHobby.html', hobby=hobby_lista)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        if not email or not senha:  
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('index'))

        session_db = Session()  

        try:
            usuario = session_db.query(Usuario).filter_by(email_user=email).first()
            
            if usuario and usuario.password_user == senha: 
                session['usuario_id'] = usuario.id
                session['usuario_logado'] = usuario.name_user
                flash(usuario.name_user + ' logado com sucesso!')
                return redirect(url_for('hobby'))
            else:
                flash('Email ou senha incorretos.')
                return redirect(url_for('index'))
        
        except Exception as e:
            flash('Erro ao processar o login: ' + str(e))
            return redirect(url_for('index'))
        
        finally:
            session_db.close()
    
    return render_template('index.html')


@app.route('/cadastra', methods=['POST'])
def cadastra_usuario():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    
    session = Session()

    usuario = Usuario(name_user=nome, email_user=email, password_user=senha)

    try:
        session.add(usuario)
        session.commit()
        flash('Usuário criado com sucesso!')
    except Exception as e:
        session.rollback()
        flash('Erro ao criar o Usuário: ' + str(e))
    finally:
        session.close()
    
    return redirect(url_for('index'))

@app.route('/cadastraHobby', methods= ['GET','POST'])
def cadastra_hobby():
    if request.method == 'POST':
        tipo = request.form['tipo']
        nome = request.form['nome']
        
        usuario_id = session.get('usuario_id')  

        session_db = Session()

        hobby = Hobby(tipo=tipo,nome=nome, usuario_id=usuario_id)

        try:
            session_db.add(hobby)
            session_db.commit()
            flash('Hobby cadastrada com sucesso!')
        except Exception as e:
            session_db.rollback()
            flash('Erro ao cadastrar a Hobby: ' + str(e))
        finally:
            session_db.close()
        
        return redirect(url_for('hobby'))
    
    return render_template('cadastrarHobby.html')

@app.route('/logout')
def logout():

    session.pop('usuario_logado', None)
    return redirect(url_for('index'))


app.run(debug=True)
