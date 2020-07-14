import bfm
def returnCodeTest(self):
	return {"code": "C+."}
BF=bfm.Brainfuck({"C":returnCodeTest, **bfm.defaultBF.rules}, bfm.defaultBF.state)
BF.run("+[C]")