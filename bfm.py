import msvcrt

# TODO:
# - Allow languages to:
#   - Modify the instruction index
#   - Modify the code being run
#   - Modify rulesets (Might be possible with dedicated operators?)
# - Syntax checking
#   - Make sure all blocks are properly closed (`[(])` is eiter officially supported or explicitly disallowed)

class Brainfuck:
	def __init__(self, rules, state):
		self.rules=rules # {"+":addOp, ..., "[":[whileBlock, "]"], ...}
		self.state=state # {"tape":[...], "pointer":0, ...}

	def getMatching(self, code, start):
		# Get matching closing brace of an opening brace
		# code: Indexable (str, list, etc.): Segment of code
		# start: Index (int, etc.): Position of starting brace in <code>
		indent=0
		openBrace=code[start]
		closeBrace=self.rules[openBrace][1]
		for index in range(start, len(code)):
			if code[index]==openBrace : indent+=1
			if code[index]==closeBrace: indent-=1
			if indent==0: return index

	def run(self, code):
		instruction=0
		while instruction<len(code):
			returnData={}
			if code[instruction] in self.rules:
				if type(self.rules[code[instruction]])==list:
					# Code block (Like [ and ] in normal BF)
					sub=code[instruction+1:self.getMatching(code, instruction)] # Get code inside the block (containing braces excluded)
					returnData=self.rules[code[instruction]][0](self, sub)
					instruction+=len(sub)
				else:
					# Operator
					returnData=self.rules[code[instruction]](self)
				if type(returnData)==dict:
					if "exit" in returnData and returnData["exit"]==True:
						return {"exit":True}
			instruction+=1

class defaultBF:
	def addOp(self):
		self.state["tape"][self.state["pointer"]]+=1
		self.state["tape"][self.state["pointer"]]%=256
	def subOp(self):
		self.state["tape"][self.state["pointer"]]+=255 # Faster than -1+256
		self.state["tape"][self.state["pointer"]]%=256
	def incOp(self):
		self.state["pointer"]+=1
		self.state["pointer"]%=30000
	def decOp(self):
		self.state["pointer"]+=29999 # Faster than -1+30000
		self.state["pointer"]%=30000
	def outOp(self):
		# TODO: Make sure `end=""` doesn't cause any issues in non-terminating code
		print(chr(self.state["tape"][self.state["pointer"]]), end="") # .
	def cinOp(self):
		# TODO: Linux (:thumbsup:)/Mac (:vomit:) compatibility
		self.state["tape"][self.state["pointer"]]=ord(msvcrt.getch()) # ,
	def loopBlock(self, code): # [code]
		while self.state["tape"][self.state["pointer"]]!=0:
			self.run(code)
	rules={
		"+": addOp,
		"-": subOp,
		">": incOp,
		"<": decOp,
		".": outOp,
		",": cinOp,
		"[": [loopBlock, "]"]
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
