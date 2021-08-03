import os
import sys
import random
import subprocess
from flask import Flask, request, render_template, url_for

__author__ = 'Felipe V. Calderan'
__copyright__ = 'Copyright (C) 2021 Felipe V. Calderan'
__license__ = 'BSD 3-Clause "New" or "Revised" License'
__version__ = '1.0'

# How to run this program from the terminal:
# curl -X POST -F "script=$(cat example_script.gd)" "IP:PORT"

# relevant constants for the application
TIMEOUT = 10    # in seconds

FORBIDDEN = ['OS.execute', 'OS.kill', 'OS.shell_open', 'OS.set', 'OS.request',
             'OS.print', 'OS.dump', 'OS.native', 'OS.open', 'OS.close',
             'OS.show', 'file.', 'File.']

DEFAULT_SCRIPT = '''extends SceneTree

func _init():
\tprint("Hello World!")
\tquit() # don't forget to quit!
'''

# set environment language to english (prevent Godot error message)
os.environ['LANG'] = 'en_US.utf8'

# make Godot executable
os.system('chmod +x godot')

# create the Flask Application
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def gdscript_form():
    # handle the POST request
    if request.method == 'POST':
        content = request.form.get('script')

        # fenerate unique name for input/output
        random_num = random.randint(0, sys.maxsize)
        script_name = f'script_{random_num}.gd'
        output_name = f'output_{random_num}.txt'

        # store if forbidden patterns were found (to block script's execution)
        forbidden_found = ''

        # write gdscript file
        with open (script_name, 'w+') as f:
            for forbid in FORBIDDEN:
                if forbid in content:
                    forbidden_found = forbid
                    break
            else:
                f.write(content)

        # execute Godot and read gdscript (if not forbidden)
        godot_ans = ''
        if not forbidden_found:
            command = f'timeout {TIMEOUT} ./godot -s\
                        {script_name} > {output_name} 2>&1\
                        || echo "\n\nERROR: Time Limit Exceeded ({TIMEOUT}s)"\
                        > {output_name}'
            child = subprocess.Popen(command,shell=True,stderr=subprocess.PIPE)
            child.wait()
        else:
            with open(output_name, 'w+') as g:
                g.write(f'\n\nERROR: Forbidden pattern: "{forbidden_found}"\n')

        # write Godot's output to file (except Godot's launch message),
        # after that, delete the file, since it's not needed anymore.
        if os.path.exists(output_name):
            with open(output_name, 'r') as f:
                for line in f.readlines()[2:]:
                    godot_ans += line
            os.remove(output_name)

        # delete gdscript file
        if os.path.exists(script_name):
            os.remove(script_name)

        # check if user is using a Browser or cURL/Non-browser program
        if request.user_agent.browser is not None:
            #return simple_page(content, godot_ans)
            return render_template(
                'index.html', timeout=TIMEOUT, content=content, gans=godot_ans
            )
        else:
            return godot_ans

    # if it's not a POST request, handle a GET request instead
    # return simple_page()
    return render_template(
        'index.html', timeout=TIMEOUT, content=DEFAULT_SCRIPT
    )


# uncomment to run the server locally with debug enabled on port 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)
