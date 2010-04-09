 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97

	

#!/usr/bin/python2.2
"""
A very simple Session Handling example
using plain Python CGI (tested only under Python 2.2+)

License: GPL 2; share and enjoy!
Author: Jonas Galvez <jonasgalvez@gmail.com>
Contributor: Patrick Hall <pathall@gmail.com>

Usage: /script.cgi?start=1
"""

import cgitb; cgitb.enable()
import sys, os, cgi, pickle
from Cookie import SimpleCookie

class form(dict):
    def __init__(self, fields):
        dict.__init__(self, fields)
        for k, v in self.items(): self[k] = v.value

form = form(cgi.FieldStorage())

# hard-coded index numbers
# to make it easier to pass to functions
questions = (
    (0, "What's your name?"),
    (1, "How old are you?"),
    (2, "Where are you from?")
)
#questions = [(i, q.strip()) for i, q in enumerate(open('questions.txt').readlines())]

def generate_hash():
    import sha, time
    return sha.new(str(time.time())).hexdigest()

def print_headers(headers):
    for k, v in headers.items():
        sys.stdout.write('%s: %s\n' % (k, v))
    sys.stdout.write('\n')

def print_form(question):
    form_template = """<html><body><form action="%(script)s" method="POST">
    %(question)s:<br /><input type="hidden" name="question_id" value="%(id)s" />
    <input type="text" name="answer" /><input type="submit" /></form></body></html>"""
    id, question = question
    script = os.environ.get('SCRIPT_NAME', sys.argv[0])
    sys.stdout.write(form_template % locals())

def print_result(questions):
    sys.stdout.write('<html><body>')
    for i, q, a in questions:
        sys.stdout.write('<p>Question: %s<br />Answer:%s</p>' % (q[1], a))
    sys.stdout.write('</body></html>')

if not os.path.exists('.sessions'):
    os.mkdir('.sessions')

def main():

    if not form.has_key('start'):

        sid = SimpleCookie(os.environ['HTTP_COOKIE'])['sid'].value
        id, answer = form['question_id'], form['answer']

        if os.path.exists(os.path.join('.sessions', sid)):
            session_file = open(os.path.join('.sessions', sid), 'rb')
            session_obj = pickle.load(session_file)
            session_file.close()
        else:
            session_obj = {}
            session_obj['questions'] = []

        session_obj['questions'].append((id, questions[int(id)], answer))
        session_file = open(os.path.join('.sessions', sid), 'wb')
        pickle.dump(session_obj, session_file, 1)
        session_file.close()

        if len(session_obj['questions']) == len(questions):
            print_headers({'Content-type':'text/html'})
            print_result(session_obj['questions'])
        else:
            headers = {}
            headers['Content-type'] = 'text/html'
            headers['Set-Cookie'] = 'sid=%s;' % sid
            print_headers(headers)
            print_form(questions[int(id)+1]) # funky

    else:
        headers = {}
        headers['Content-type'] = 'text/html'
        headers['Set-Cookie'] = 'sid=%s;' % generate_hash()
        print_headers(headers)
        print_form(questions[0])

if __name__ == '__main__':
    main()
