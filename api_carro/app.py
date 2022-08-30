import mysql.connector
import uuid
from flask import Flask, make_response, jsonify, request


# MySQL connector
mydb = mysql.connector.connect(
    host='localhost',
    user='MyUser',
    password='MainPassword',
    database='ZZironiteDB',
)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/carros', methods=['GET'])
def get_carros():

    m_cursor = mydb.cursor()
    m_cursor.execute('SELECT * FROM carros')
    carros = m_cursor.fetchall()

    return_carros = list()
    for carro in carros:
        return_carros.append(
            {
                'id':carro[0],
                'marca': carro[1],
                'modelo': carro[2],
                'ano': carro[3],
                'id_carro': carro[4]
            }
        )

    return make_response(
        jsonify(
            message="Lista de carros.",
            data=return_carros
        )
    )


@app.route('/cadastrar', methods=['POST'])
def cadastrar_carro():
    carro = request.json
    
    m_cursor = mydb.cursor()

    id_carro = str(uuid.uuid4())
    sql = f"INSERT INTO carros (marca,modelo,ano,id_carro) VALUES ('{carro['marca']}','{carro['modelo']}', '{carro['ano']}', '{id_carro}')"
    m_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
            message=f"Carro cadastrado com sucesso.",
            data=carro
        )
    )


app.run(debug=True)