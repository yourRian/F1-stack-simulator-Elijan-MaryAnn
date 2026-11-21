import secrets
from flask import Flask, render_template, request, redirect, url_for, session, flash
from queue_model import Queue

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)


@app.route('/')
def index():
    items = session.get('queue', [])
    removed = session.get('dequeued', [])
    highlight = session.pop('peek', False)
    return render_template('index.html',
                           items=items,                      # front muna, hindi nire-reverse
                           size=len(items),
                           removed=list(reversed(removed)),  # pinakabago sa taas
                           highlight=highlight)


@app.route('/queue', methods=['POST'])
def operate():
    action = request.form.get('action', '')
    value = request.form.get('value', '').strip()
    q = Queue(session.get('queue', []))
    dequeued = session.get('dequeued', [])

    if action == 'enqueue':
        if not value:
            flash('Please enter a value.', 'error')
        elif len(value) > 24:
            flash('Maximum of 24 characters only.', 'error')
        elif q.size() >= 20:
            flash('Queue is full (20 items max).', 'error')
        else:
            q.enqueue(value)
            flash(f'Enqueued {value} at the rear.')
    elif action == 'dequeue':
        if q.is_empty():
            flash('Queue is empty. Nothing to dequeue.', 'error')
        else:
            item = q.dequeue()
            dequeued.append(item)
            flash(f'Dequeued {item} from the front.')
    elif action == 'peek':
        if q.is_empty():
            flash('Queue is empty. Nothing to peek.', 'error')
        else:
            session['peek'] = True
            flash(f'Front item is {q.peek()}.')
    elif action == 'clear':
        q.clear()
        dequeued = []
        flash('Queue cleared.')

    session['queue'] = q.items
    session['dequeued'] = dequeued[-20:]
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
