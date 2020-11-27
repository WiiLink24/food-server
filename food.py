# yummy code
actionlist = {
    'webapi_a_thing':'file_that_this_action_requires.php'
} # that's a placeholder lul
from flask import request, Flask, send_from_directory
app = Flask(__app__)
@app.route('/nwapi.php')
def api():
     try:
        print(action_list[request.args[action]])
        return ''
     except:
        return send_from_directory('.','aio.php')
 
