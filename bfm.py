import msvcrt, sys

class _nprop:
	char=[True, 0, 255, True]
	inf=[True, None, None, True]
	schar=[True, -128, 127, True]
class _DEFS:
	nprop=[True, None, None, True]
	ploop=[True, True]

class BrainFuck:
	class BFStateFuncs:
		def addOp(self, **kwargs): self.tape[self.pointer]+=1; self.handleState()
		def subOp(self, **kwargs): self.tape[self.pointer]-=1; self.handleState()
		def incOp(self, **kwargs): self.pointer+=1; self.handleState()
		def decOp(self, **kwargs): self.pointer-=1; self.handleState()
		
		def outOp(self, **kwargs): self.out(chr(self.tape[self.pointer])) # .
		def kinOp(self, **kwargs): self.tape[self.pointer]=ord(msvcrt.getch()) # ,
		
		def loopB(self, **kwargs): # [code]
			while self.tape[self.pointer]!=0:
				self.exec(kwargs["code"], kwargs["dep"]+1)
		
		
	def getMatching(self, code, start):
		level=0
		for cpos in range(start, len(code)):
			if code[cpos]==code[start]:
				# If the current command is the start for the same block as we're checking, then add 1 to level
				# We don't care about other blocks, because those should be contained within the one we're checking
				# Also there might be use cases for "([)]" and stuff and I do not want to be the guy to break those
				level+=1
			elif code[cpos]==self.blocks[code[start]][1]:
				level-=1
				if level==0:
					# If this block end sets us back to the level we started at, then this is the matching block end
					return cpos
		else:
			return False
	
	def handleState(self):
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
			raise ValueError("Tape cell "+str(self.pointer)+" is above the max value of "+str(self.nprop[2]))
	
	def reset(self):
		for x in self.resetData:
			setattr(self, x, self.resetData[x])
	
	def __init__(self, **kwargs):
		if "tape" not in kwargs:
			self.tape=[0 for x in range(30000)]
		else:
			ktape=kwargs["tape"]
			if type(ktape)==int: # Make an empty array of length `ktape`
				self.tape=[0 for x in range(ktape)]
			elif type(ktape)==tuple: # Make an array of length `ktape[0]` filled with `ktape[1]`
				self.tape=[ktape[1] for x in range(ktape[0])]
			else:
				self.tape=ktape
		
		self.pointer=0 if "pointer" not in kwargs else kwargs["tape"]
		
		# nprop=[bool(Can wrap under), bool|True(Min number), bool|True(Max number), bool(Can wrap over)]
		if "nprop" not in kwargs:
			self.nprop=_DEFS.nprop
		else:
			knprop=kwargs["nprop"]
			if type(knprop)==str: # Get predefiend nprops
				self.nprop=getattr(_nprop,knprop)
			else:
				self.nprop=knprop
		
		# Not all outputs allow for `end=""`, so we're not gonna force it
		self.out=(lambda *args:print(*args, end="")) if "out" not in kwargs else kwargs["out"]
		
		if "ploop" not in kwargs: # [bool(loop from -1 to max), bool(loop from max+1 to 0)]
			# It stands for "pointer loop", not anything else, you ploopy
			self.ploop=_DEFS.ploop
		else:
			kploop=kwargs["ploop"]
			if type(kploop)==bool:
				self.ploop=[kploop, kploop]
			else:
				self.ploop=kploop
		
		self.safe=True if "safe" not in kwargs else kwargs["safe"] # Automatically handle nprop and ploop
		self.locs=[] # Execution locations
		
		clone=lambda x:(x+[] if type(x)==list else x) # Lists are... weird. `a=[0]` `b=a` `b.append(2)` `print(a)` outputs `[0,2]`
		
		self.resetData={
			"tape":clone(self.tape),
			"pointer":clone(self.pointer),
			"nprop":clone(self.nprop),
			"ploop":clone(self.ploop),
			"safe":clone(self.safe),
			"locs":clone(self.locs)
		}
		
		self.ops={
			"+":BrainFuck.BFStateFuncs.addOp,
			"-":BrainFuck.BFStateFuncs.subOp,
			">":BrainFuck.BFStateFuncs.incOp,
			"<":BrainFuck.BFStateFuncs.decOp,
			".":BrainFuck.BFStateFuncs.outOp,
			",":BrainFuck.BFStateFuncs.kinOp
		}
		self.blocks={ # Since we're handling code blocks inside of functions, we have to make it one function and just make it work
			"[":[BrainFuck.BFStateFuncs.loopB, "]"]
		}
		
		# Crude custom operator/block handler
		for x in ["ops", "blocks"]: # Makes me not need two seperate loops
			if x in kwargs:
				for y in kwargs[x]:
					if x=="ops":
						self.ops[y]=((lambda *args, **kwargs:None) if y==None else kwargs[x][y])
					elif x=="blocks":
						self.blocks[y]=((lambda *args, **kwargs:None) if y==None else kwargs[x][y])
	
	def exec(self, code, dep=0):
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

if __name__=="__main__":
	# Should Print "hello world", instead gets stuck in an infinite loop
	# Running it in any other interpreter such as the one at https://copy.sh/brainfuck/ works as expected
	if sys.argv[1]=="hw":
		a=BrainFuck(nprop="char")
		a.exec("+[-[<<[+[--->]-[<<<]]]>>>-]>-.---.>..>.<<<<-.<+.>>>>>.>.<<.<-.")
		a.reset()
		a.exec("+[-[<<[+[--->]-[<<<]]]>>>-]>-.---.>..>.<<<<-.<+.>>>>>.>.<<.<-.")
	else:
		a=BrainFuck(nprop=_nprop.char)
		a.exec(sys.argv[1])
