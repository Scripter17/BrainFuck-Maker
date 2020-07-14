import bfm

def doubleOp(self):
	self.state["tape"][self.state["pointer"]]*=2

BF=bfm.Brainfuck({"*":doubleOp, **bfm.defaultBF.rules}, bfm.DefaultBF.state)
BF.run("+******+.+.+.") # Expected output: ABC
