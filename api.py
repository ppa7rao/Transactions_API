from flask import Flask, render_template, request
import psycopg2


app =  Flask(__name__)

# Fully - Fledged DB like PostgreSQL
# Keep the data in a PostgreDB
POSTGRESQL_URI = 'postgres://ynijajhr:JcGuDd6fCLFM8JMPlZFHjVQ_23uI21Dp@surus.db.elephantsql.com/ynijajhr'
conn = psycopg2.connect(POSTGRESQL_URI)

try: 
    with conn:
        with conn.cursor() as cursor:
            # This creates a table with 3 columns (date, amount and account)
            cursor.execute('CREATE TABLE transactions (date TEXT, amount REAL, account TEXT);')
except psycopg2.errors.DuplicateTable:
    pass

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.form)
        # Add a table of data
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO transactions VALUES (%s, %s, %s);",
                (
                    request.form.get('date'),
                    float(request.form.get('amount')),
                    request.form.get('account'),   
                ),
            )
        conn.commit()

    return render_template('form.html')


@app.route('/transactions')
def show_transactions():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM transactions;")
            transactions = cursor.fetchall()
    return render_template('transactions.jinja2', 
                           entries=sorted(transactions, 
                                          key=lambda x: x[0])
                            )

