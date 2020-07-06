import bfm

def exitOperator(self):
	return {"exit":True}

def loopBlock(self, code): # [code]
	while self.state["tape"][self.state["pointer"]]!=0:
		returnData=self.run(code)
		# Handle the exit condition
		if type(returnData)==dict and "exit" in returnData and returnData["exit"]==True:
			return {"exit":True}

BF=bfm.BrainFuck({"E":exitOperator, **bfm.defaultBF.rules, "[":[loopBlock, "]"]}, bfm.defaultBF.state)
BF.run("+[[[E]]].") # Expected output: 
