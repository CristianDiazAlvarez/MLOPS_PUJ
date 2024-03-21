import request
import json
r = requests.get('http://10.43.101.149:80/data?group_number=10')
d = json.loads(r.content.decode('utf-8'))
d['data'][0]
import readline
readline.write_history_file('python_command_history.py')
