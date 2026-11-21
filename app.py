import secrets
from flask import Flask, render_template, request, redirect, url_for, session, flash
from stack_model import Stack

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)


@app.route('/')
def index():
    items = session.get('stack', [])
    popped = session.get('popped', [])
    highlight = session.pop('peek', False)
    return render_template('index.html',
                           items=list(reversed(items)),   # top muna
                           size=len(items),
                           popped=list(reversed(popped)),
                           highlight=highlight)


@app.route('/stack', methods=['POST'])
def operate():
    action = request.form.get('action', '')
    value = request.form.get('value', '').strip()
    stack = Stack(session.get('stack', []))
    popped = session.get('popped', [])

    if action == 'push':
        if not value:
            flash('Please enter a value.', 'error')
        elif len(value) > 24:
            flash('Maximum of 24 characters only.', 'error')
        elif stack.size() >= 20:
            flash('Stack is full (20 items max).', 'error')
        else:
            stack.push(value)
            flash(f'Pushed {value}.')
    elif action == 'pop':
        if stack.is_empty():
            flash('Stack is empty. Nothing to pop.', 'error')
        else:
            item = stack.pop()
            popped.append(item)
            flash(f'Popped {item}.')
    elif action == 'peek':
        if stack.is_empty():
            flash('Stack is empty. Nothing to peek.', 'error')
        else:
            session['peek'] = True
            flash(f'Top item is {stack.peek()}.')
    elif action == 'clear':
        stack.clear()
        popped = []
        flash('Stack cleared.')

    session['stack'] = stack.items
    session['popped'] = popped[-20:]
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
