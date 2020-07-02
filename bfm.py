import msvcrt, sys

class BrainFuck:		
	def getMatching(self, code, start):
		indent=0
		openBrace=code[start]
		closeBrace=self.rules[openBrace][1]
		for index in range(start, len(code)):
			if code[index]==openBrace: indent+=1
			if code[index]==closeBrace: indent-=1
			if indent==0: return index
	
	"""def handleState(self):
		# Pointer looping
		if (self.pointer<0 and self.ploop[0]) or (self.pointer>=len(self.tape) and self.ploop[1]):
			# Can loop, so do
			pt, uv=self.pointer, len(self.tape)
			self.pointer=((pt%uv)+uv)%uv
		elif self.pointer<0 and not self.ploop[0]:
			# Can't loop under
			raise ValueError("Pointer index ("+str(self.pointer)+") is below 0 ")
		elif self.pointer>=len(self.tape) and not self.ploop[1]:
			# Can't loop over
			raise ValueError("Pointer index ("+str(self.pointer)+") is above the tape length ("+str(len(tape))+")")
		
		# Number looping
		if (self.nprop[1]!=None and self.tape[self.pointer]<self.nprop[1] and self.nprop[0]) or (self.nprop[2]!=None and self.tape[self.pointer]>self.nprop[2] and self.nprop[3]):
			v, l, u=self.tape[self.pointer], self.nprop[1], self.nprop[2]
			self.tape[self.pointer]=(v-l)%(u-l+1)+l
		elif (self.nprop[1]!=None and self.tape[self.pointer]<self.nprop[1] and not self.nprop[0]):
			raise ValueError("Tape cell "+str(self.pointer)+" is below the min value of "+str(self.nprop[1]))
		elif (self.nprop[2]!=None and self.tape[self.pointer]>self.nprop[2] and not self.nprop[3]):
			raise ValueError("Tape cell "+str(self.pointer)+" is above the max value of "+str(self.nprop[2]))"""
	
	def reset(self):
		for x in self.resetData:
			setattr(self, x, self.resetData[x])
	
	def __init__(self, rules, state):
		self.rules=rules
		self.state=state
	
	def run(self, code):
		instruction=0
		while instruction<len(code):
			if code[instruction] in self.rules:
				if type(self.rules[code[instruction]])==list:
					self.rules[code[instruction]][0](self, code[instruction+1:self.getMatching(code, instruction)])
				else:
					self.rules[code[instruction]](self)
			instruction+=1

	"""def exec(self, code, dep=0):
		self.locs.append(0)
		while self.locs[-1]<len(code):
			#print(self.locs)
			char=code[self.locs[-1]]
			if char in self.blocks: # if char=="[", then it's the start of a while block
				endLoc=self.getMatching(code, self.locs[-1]) # Get location of matching block ending ("[" won't look for or even notice ")")
				blockCode=code[self.locs[-1]+1:endLoc] # Get the code to be run by the block
				r=self.blocks[char][0](self, code=blockCode, loc=self.locs[-1], source=code, dep=dep) # Things like while loops are handled inside the function
				self.locs[-1]=endLoc
			elif char in self.ops:
				r=self.ops[char](self, out=self.out, loc=self.locs[-1], source=code, dep=dep)
			
			if type(r)==dict: # Special operations
				self.locs[-1]=r["loc"] if "loc" in r else self.locs[-1]+1
				if "return" in r and r["return"]==True: return self
			else:
				self.locs[-1]+=1
			if self.safe:
				self.handleState()
		self.locs.pop()
		return self # This is so that you can get the final tape data and stuff when the code is done
		"""

class defaultBF:
	def handleOverflow(self):
		self.state["pointer"]=(self.state["pointer"]+30000)%30000
		self.state["tape"][self.state["pointer"]]=(self.state["tape"][self.state["pointer"]]+256)%256
	def addOp(self):
		self.state["tape"][self.state["pointer"]]+=1
		defaultBF.handleOverflow(self)
	def subOp(self):
		self.state["tape"][self.state["pointer"]]-=1
		defaultBF.handleOverflow(self)
	def incOp(self): self.state["pointer"]+=1
	def decOp(self): self.state["pointer"]-=1
	def outOp(self): print(chr(self.state["tape"][self.state["pointer"]]), end="") # .
	def cinOp(self): self.state["tape"][self.state["pointer"]]=ord(msvcrt.getch()) # ,
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
	a=BrainFuck(defaultBF.rules, defaultBF.state)
	#a.run("+[-[<<[+[--->]-[<<<]]]>>>-]>-.---.>..>.<<<<-.<+.>>>>>.>.<<.<-.")
	a.run("+[.+]")