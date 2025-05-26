from flask import Flask, render_template, request, redirect, send_file
import os
import json
from docxtpl import DocxTemplate

app = Flask(__name__)
CLIENTES_PATH = "clientes.json"

def carregar_clientes():
    if os.path.exists(CLIENTES_PATH):
        with open(CLIENTES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_clientes(clientes):
    with open(CLIENTES_PATH, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=2, ensure_ascii=False)

@app.route("/", methods=["GET", "POST"])
def index():
    clientes = carregar_clientes()
    if request.method == "POST":
        cliente = {
            "nome": request.form["nome"],
            "cpf": request.form["cpf"],
            "rg": request.form["rg"],
            "orgao": request.form["orgao"],
            "data_emissao": request.form["data_emissao"],
            "nascimento": request.form["nascimento"],
            "nacionalidade": request.form["nacionalidade"],
            "naturalidade": request.form["naturalidade"],
            "estado_civil": request.form["estado_civil"],
            "profissao": request.form["profissao"],
            "filiacao": request.form["filiacao"],
            "endereco": request.form["endereco"],
            "cep": request.form["cep"]
        }
        clientes.append(cliente)
        salvar_clientes(clientes)
        return redirect("/")
    return render_template("index.html", clientes=clientes)

@app.route("/gerar/<int:cliente_id>/<modelo>")
def gerar_documento(cliente_id, modelo):
    clientes = carregar_clientes()
    cliente = clientes[cliente_id]
    doc = DocxTemplate(f"modelos/{modelo}.docx")
    doc.render(cliente)
    nome_arquivo = f"documentos_gerados/{modelo}_{cliente['nome'].replace(' ', '_')}.docx"
    os.makedirs("documentos_gerados", exist_ok=True)
    doc.save(nome_arquivo)
    return send_file(nome_arquivo, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
