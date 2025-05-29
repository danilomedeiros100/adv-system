from app import create_app, db
from flask.cli import with_appcontext
import click

app = create_app()  # instanciando a app

@click.command('create-db')
@with_appcontext
def create_db_command():
    """Cria as tabelas no banco de dados."""
    db.create_all()
    click.echo('Banco de dados criado com sucesso!')

app.cli.add_command(create_db_command)

if __name__ == '__main__':
    app.run(debug=True)