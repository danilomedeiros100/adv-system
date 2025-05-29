from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required

csrf_teste_bp = Blueprint('csrf_teste', __name__)

@csrf_teste_bp.route('/csrf-teste', methods=['GET', 'POST'])
@login_required
def csrf_teste():
    if request.method == 'POST':
        flash('Formulário enviado com sucesso! CSRF validado.', 'success')
        return redirect(url_for('csrf_teste.csrf_teste'))
    return render_template('csrf_teste.html')