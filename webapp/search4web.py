from flask import Flask, render_template, request, escape, session, copy_current_request_context
from vsearch import search4letters
from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError
from checker import check_logged_in
from threading import Thread
from time import sleep

app = Flask(__name__)

app.secret_key = 'Yuef'

app.config['dbconfig'] = {'host' : '127.0.0.1',
                'user' : 'vsearch',
                'password' : 'vsearchpasswd',
                'database' : 'vsearchlogDB'}


@app.route('/search4',methods=['POST'])
def do_search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))

    @copy_current_request_context
    def log_request(req: 'flask_request', res: str) -> None:
        """Логирует запрос в БД"""
        with UseDatabase(app.config['dbconfig']) as cursor:
            sleep(15)
            _SQL = """insert into log
                (phrase, letters, ip, browser_string, results)
                values
                (%s,%s,%s,%s,%s)"""
            cursor.execute(_SQL, (req.form['phrase'],
                                  req.form['letters'],
                                  req.remote_addr,
                                  req.user_agent.browser,
                                  res,))
    try:
        log_thread = Thread(target=log_request, args=(request, results))
        log_thread.start()
    except Exception as err:
        print('Доигрался чёрт ушастый!', str(err))
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
@check_logged_in
def view_the_log() -> 'html':
    try:
        with UseDatabase(app.config['dbconfig'] ) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        return render_template('viewlog.html',
                           the_title='Log search4wed',
                           the_row_titles=('Phrase', 'Letters', 'IP', 'Browser', 'Results'),
                           the_data = contents,)
    except ConnectionError as err:
        print('БД включил? Error: ', str(err))
    except CredentialsError as err:
        print('неправильный логин или пароль. Error: ', str(err))
    except SQLError as err:
        print('Ошибка в запросе. Ошибка: ',str(err))
    except Exception as err:
        print('Error: ',str(err))
    return 'Error'

@app.route('/login')
def login() -> str:
    session['logged_in'] = True
    return 'You are now logged in.'

@app.route('/logout')
def logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out.'
    

app.run(debug=True)
