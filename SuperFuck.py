import bfm, sys
def ifBlock(self, **kwargs):
	code=kwargs["code"].split("|")
	if len(code)==1:
		if self.tape[self.pointer]!=0:
			self.exec(code[0])
	elif len(code)==2:
		if self.tape[self.pointer]!=0:
			self.exec(code[0])
		else:
			self.exec(code[1])
	elif len(code)==3:
		if self.tape[self.pointer]<0:
			self.exec(code[0])
		elif self.tape[self.pointer]==0:
			self.exec(code[1])
		else:
			self.exec(code[2])
def twiceBlock(self, **kwargs):
	code=kwargs["code"]
	for x in range(2):
		self.exec(code)

def mulOp(self, **kwargs):
	self.tape[self.pointer]*=2
def divOp(self, **kwargs):
	self.tape[self.pointer]=int(self.tape[self.pointer]/2)
def atOp(self, **kwargs):
	self.pointer=self.tape[self.pointer]
def refOp(self, **kwargs):
	self.tape[self.pointer]=self.pointer
def printRaw(self, **kwargs):
	self.out(self.tape[self.pointer])
superFuck=bfm.BrainFuck(
	ops={
		"*":mulOp,
		"/":divOp,
		"@":atOp,
		"&":refOp,
		"?":printRaw
	},
	blocks={
		"(":[ifBlock,")"],
		"{":[twiceBlock, "}"]
	},
	nprop="inf"
)
superFuck.exec(sys.argv[1])
