from flask import Flask, render_template, request, escape
from vsearch import search4letters
import mysql.connector

app = Flask(__name__)

dbconfig = {'host' : '127.0.0.1',
                'user' : 'vsearch',
                'password' : 'vsearchpasswd',
                'database' : 'vsearchlogDB'}

def log_request(req: 'flask_request',res: str) -> None:
    with UseDatabase(dbconfig) as cursor:
        _SQL = """insert into log
            (phrase, letters, ip, browser_string, result)
            values
            (%s,%s,%s,%s,%s)"""
    cursor.execute(_SQL,(req.form['phrase'],
                         req.form['letters'],
                         req.remote_addr,
                         req.user_agent.browser,
                         res,))

@app.route('/search4',methods=['POST'])
def do_search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
def view_the_log() -> 'html':
#    contents = []
#    with open('vsearch.log')as log:
#        for row in log:
#            contents.append(escape(row).split('|'))
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """select phrase, letters, ip, browser_string, result from log"""
    cursor.execute(_SQL)
    contents = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('viewlog.html',
                           the_title='Log search4wed',
                           the_row_titles=('Phrase', 'Letters', 'IP', 'Browser', 'Results'),
                           the_data = contents,)
    

app.run(debug=True)
