# yummy code
actionlist = {
    'webapi_a_thing':'file_that_this_action_requires.php'
} # that's a placeholder lul
from flask import request, Flask
app = Flask(__app__)
@app.route('/nwapi.php')
def api():
     print(action_list[request.args[action]])
     return ''
 
