# OwenFuck - An alias of brainfuck using 8 words given by my friend Jackson
import bfm

bf=bfm.Brainfuck(
	{
		"big":bfm.defaultBF.addOp,
		"chungus":bfm.defaultBF.subOp,
		"but":bfm.defaultBF.incOp,
		"gay":bfm.defaultBF.decOp,
		"but":bfm.defaultBF.outOp,
		"neo":[bfm.defaultBF.loopBlock, "nazi"]
	},
	{
		"tape":[0 for x in range(30000)],
		"pointer":0
	}
)