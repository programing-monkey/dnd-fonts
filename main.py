from flask import Flask,render_template,request
from googletrans import Translator
import unicodedata
def translate(text,lang):
	translator = Translator()
	prexput = translator.translate(text,dest=lang)
	if prexput.pronunciation:
		exput = prexput.pronunciation
	else:
		exput = prexput.text

	return unicodedata.normalize('NFKD', exput).encode('ascii','ignore')


def to_Abysal(text):
	out = ""
	a = lambda n:((n+1)&0b11111111)
	e = lambda n:((n&0b00010101)<<2)|((n&0b10101000)>>2)|((n&0b01000000)<<1)|((n&0b00000010)>>1)
	u = lambda n:((n+0b11111111)&0b11111111)
	
	metaexprs = [[]]*256
	
	for metaindex,exprs in enumerate(metaexprs):
		exprs = [""]*256
		exprs[metaindex] = "c" if metaindex else "z"
	
		length = 1
	
		while not all(exprs):
			for index,expr in enumerate(exprs):
				if len(expr) == length:
					candidate_a = a(index)
					candidate_e = e(index)
					candidate_u = u(index)
					if (not exprs[candidate_a]) or (length+1 < len(exprs[candidate_a])):
						exprs[candidate_a] = expr+"a"
					if (not exprs[candidate_e]) or (length+1 < len(exprs[candidate_e])):
						exprs[candidate_e] = expr+"e"
					if (not exprs[candidate_u]) or (length+1 < len(exprs[candidate_u])):
						exprs[candidate_u] = expr+"u"
			length += 1
	
		metaexprs[metaindex] = exprs

	for prev,curr in zip("\x00"+text, text+"\n"):
		candidate1 = metaexprs[ord(prev)][ord(curr)]+"c"
		candidate1 = candidate1[1:] if candidate1[0]=="c" else candidate1
		candidate2 = metaexprs[0][ord(curr)]+"c"
		out += (sorted([candidate1,candidate2],key=len)[0])+"\n"
	return out	
app = Flask('app')

@app.route('/')
def index():
  return render_template('template.html')

@app.route('/', methods=['GET','POST'])
def main():
	if request.method == 'POST':
		lang = request.form['lang'].split(",")
		lang[2] = bool(lang[2])
		print(lang)
		text = request.form['text']
		out = str(translate(text,lang[1]))[2:-1]

		if lang[2]:
			pass
		return '<p>'+out+'</p><style>p{font-family:"'+lang[0]+'";}@font-face {  font-family: '+lang[0]+';  src: url(https://github.com/programing-monkey/dnd-fonts/blob/master/languages/'+lang[0]+'/'+lang[0]+'.otf?raw=true);}</style>'
	else:
		return request.form


app.run(host='0.0.0.0', port=8080)
