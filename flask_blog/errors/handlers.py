from flask import url_for,Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    image = url_for('static', filename = 'images/')
    return render_template('errors/404.html',image=image), 404

## Error code mentioned because correct response.


@errors.app_errorhandler(403)
def error_403(error):
    image = url_for('static', filename = 'images/')
    return render_template('errors/403.html',image=image), 403


@errors.app_errorhandler(500)
def error_500(error):
    image = url_for('static', filename = 'images/')
    return render_template('errors/500.html',image=image), 500