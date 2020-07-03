import bfm, sys
def ifBlock(self, code):
	code=code.split("|")
	curCell=self.state["tape"][self.state["pointer"]]
	if curCell!=0 and (len(code)==1 or len(code)==2):
		self.run(code[0])
	elif curCell==0 and (len(code)==2 or len(code)==3):
		self.run(code[1])
	elif len(code)==3:
		self.run(code[1-(curCell<0)+(curCell>0)])
def twiceBlock(self, code):
	self.run(code)
	self.run(code)
def mulOp(self):
	self.state["tape"][self.state["pointer"]]*=2
def divOp(self):
	self.state["tape"][self.state["pointer"]]=int(self.state["tape"][self.state["pointer"]]/2)
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
superFuck.run(">>>&-@&?")
#superFuck.run(sys.argv[1])
