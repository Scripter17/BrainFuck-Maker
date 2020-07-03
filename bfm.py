import msvcrt

class BrainFuck:		
	def __init__(self, rules, state):
		self.rules=rules # {"+":addOp, ..., "[":[whileBlock, "]"], ...}
		self.state=state # {"tape":[...], "pointer":0, ...}

	def getMatching(self, code, start):
		indent=0
		openBrace=code[start]
		closeBrace=self.rules[openBrace][1]
		for index in range(start, len(code)):
			if code[index]==openBrace: indent+=1
			if code[index]==closeBrace: indent-=1
			if indent==0: return index

	def run(self, code):
		instruction=0
		while instruction<len(code):
			if code[instruction] in self.rules:
				if type(self.rules[code[instruction]])==list:
					sub=code[instruction+1:self.getMatching(code, instruction)]
					self.rules[code[instruction]][0](self, sub)
					instruction+=len(sub)
				else:
					self.rules[code[instruction]](self)
			instruction+=1

class defaultBF:
	def addOp(self):
		self.state["tape"][self.state["pointer"]]+=1
		self.state["tape"][self.state["pointer"]]%=256
	def subOp(self):
		self.state["tape"][self.state["pointer"]]+=255
		self.state["tape"][self.state["pointer"]]%=256
	def incOp(self):
		self.state["pointer"]+=1
		self.state["pointer"]%=30000
	def decOp(self):
		self.state["pointer"]+=29999
		self.state["pointer"]%=30000
	def outOp(self):
		print(chr(self.state["tape"][self.state["pointer"]]), end="") # .
	def cinOp(self):
		self.state["tape"][self.state["pointer"]]=ord(msvcrt.getch()) # ,
	def loopB(self, code): # [code]
		while self.state["tape"][self.state["pointer"]]!=0:
			self.run(code)
	rules={
		"+": addOp,
		"-": subOp,
		">": incOp,
		"<": decOp,
		".": outOp,
		",": cinOp,
		"[": [loopB, "]"]
	}
	state={
		"tape":[0 for x in range(30000)],
		"pointer":0
	}

if __name__=="__main__":
	import sys
	a=BrainFuck(defaultBF.rules, defaultBF.state)
	if len(sys.argv)==1:
		a.run("+[-[<<[+[--->]-[<<<]]]>>>-]>-.---.>..>.<<<<-.<+.>>>>>.>.<<.<-.")
	else:
		a.run(sys.argv[1])