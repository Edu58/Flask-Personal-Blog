from . import main


@main.route('/')
def index():
    return 'Home'
