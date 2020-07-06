import bfm

def ifBlock(self, code):
	if self.state["tape"][self.state["pointer"]]!=0:
		self.run(code)

BF=bfm.Brainfuck({"(":[ifBlock, ")"], **bfm.defaultBF.rules}, bfm.defaultBF.state)
BF.run("(.)+(.)") # Expected output: <0x01>
