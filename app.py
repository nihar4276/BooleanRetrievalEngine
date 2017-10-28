from flask import Flask, render_template,redirect,url_for, request,session
import sqlite3
from collections import defaultdict
import re




#inverted index container
a=defaultdict(list);

# stop words
stop_words = ['is','to','can','the','they','or','and','me','I'];

#length dictionary for query optimization
length= {'init':0};

#document Id's number
num=1;

#final answer(for query)
answer=[]

app = Flask(__name__)
app.secret_key = 'yolo'

def intersection(a,b):
	a=set(a);

	return list(a.intersection(b))

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

#brute force. compute only not's and and's
def evaluateExpression(exp):
	exp.strip();
	ans=[]
	if bool(re.search('OR|NOT',exp,re.I)):

		

		if bool(re.search('OR',exp,re.I)) and not bool(re.search('NOT',exp,re.I)):

			ev = exp.split('OR')
			

			for words in ev:
				words.strip()
				ans = union(ans,a[words])

			

		elif not bool(re.search('OR',exp,re.I)) and  bool(re.search('NOT',exp,re.I)):
			env = exp.split('NOT')

			temp=[x for x in range(0,num+1)]
			

			length=len(env)

			for j in range(1,length,2):
				env[j].strip()
				ans = union(ans,a[env[j-1]])
				temp1= [x for x in temp if x not in a[env[j]]]
				ans = union(ans,temp1)

				
		return ans		
	else:

		return a[exp]

@app.route('/query',methods=['POST','GET'])
def solve():


	quer = str(request.form['query'])


	query = quer.split('AND')
	#evaluate  sub expressions and then AND
	answer=evaluateExpression(query[0])


	for words in query:

		ans1 = evaluateExpression(words)
		answer= intersection(answer,ans1)



	
	return render_template("answer.html",ans=answer,query=quer)

@app.route("/invindex",methods=['POST','GET'])
def create():
	if request.method == "POST":
		r= str(request.form['data']).split('|');

	i=1

	for file in r:

		file=file.strip();
		f=open(file,"r");
		lines=f.readlines()
		

		for line in lines:
			line=line.split()

			for words in line:
				words=words.strip()
				if  words not in stop_words and i not in a[words]:
					a[words].append(i)

					if words in length:
						length[words] += 1
					else:
						length[words] = 1;




		f.close()
		#increment document id
		i=i+1

	keys=a.keys()
	length.pop('init',None)
	num=i
	


			
	return render_template("query.html",inv=a,key=keys)

@app.route("/")
def init():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
