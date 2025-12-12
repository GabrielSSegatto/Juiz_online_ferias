from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.service.auth_service import create_user, check_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = create_user(username,password)

        flash(f'Usuário {username} criado com sucesso!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if check_password(username, password):
            session['username'] = username  #marca usuario como logado
            flash(f'Bem-vindo, {username}!', 'success')
            return redirect(url_for('home'))  #rota principal da aplicação
        else:
            flash('Usuário ou senha incorretos.', 'danger')

    return render_template('login.html')
    
@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('auth.login'))