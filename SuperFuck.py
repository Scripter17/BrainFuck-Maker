import bfm, sys

def ifBlock(self, code):
	carr=[]
	cind=0
	# Properly parse only the top level if-statement
	# "(+(?|??)|???)" -> ["+(?|??)", "???"]
	# Probably breaks when the code has syntax errors, but like, that should just break regardless
	# <jank>
	for i in range(len(code)):
		if code[i]=="(": cind+=1
		if code[i]==")": cind-=1
		if code[i]=="|" and cind==0:
			carr.append(code[sum(map(len, carr))+len(carr):i])
	carr.append(code[sum(map(len, carr))+len(carr):]) # Jank as FUCK
	# </jank>
	curCell=self.state["tape"][self.state["pointer"]]
	if curCell!=0 and (len(carr)==1 or len(carr)==2):
		self.run(carr[0])
	elif curCell==0 and (len(carr)==2 or len(carr)==3):
		self.run(carr[1])
	elif len(carr)==3:
		self.run(carr[1-(curCell<0)+(curCell>0)])

def twiceBlock(self, code):
	self.run(code)
	self.run(code)

def mulOp(self):
	self.state["tape"][self.state["pointer"]]*=2

def divOp(self):
	self.state["tape"][self.state["pointer"]]//=2

def atOp(self):
	self.state["pointer"]=self.state["tape"][self.state["pointer"]]

def refOp(self):
	self.state["tape"][self.state["pointer"]]=self.state["pointer"]

def printRaw(self):
	print(self.state["tape"][self.state["pointer"]], end="")

def addOp(self):
	self.state["tape"][self.state["pointer"]]+=1

def subOp(self):
	self.state["tape"][self.state["pointer"]]-=1

superFuck=bfm.BrainFuck(
	{
		# Old BrainFuck stuff
		"+": addOp,
		"-": subOp,
		">": bfm.defaultBF.incOp,
		"<": bfm.defaultBF.decOp,
		".": bfm.defaultBF.outOp,
		",": bfm.defaultBF.cinOp,
		"[":[bfm.defaultBF.loopB, "]"],
		# New SuperFuck stuff
		"*": mulOp,
		"/": divOp,
		"@": atOp,
		"&": refOp,
		"?": printRaw,
		"(":[ifBlock,")"],
		"{":[twiceBlock, "}"]
	},
	{
		"tape":[0 for x in range(30000)],
		"pointer":0
	}
)

superFuck.run("(+(?|??)|???)") # Expected output: 000
#superFuck.run(sys.argv[1])
