# OwenFuck - An alias of BrainFuck using 8 words given by my friend Owen
import bfm

bf=bfm.BrainFuck(
	ops={
		"um":BrainFuck.BFStateFuncs.addOp,
		"poo":BrainFuck.BFStateFuncs.subOp,
		"barack obama":BrainFuck.BFStateFuncs.incOp,
		"skinny":BrainFuck.BFStateFuncs.decOp,
		"joj":BrainFuck.BFStateFuncs.outOp # He probably meant "jojo", but he said to keep it like this
	},
	blocks={
		"jesus":[BrainFuck.BFStateFuncs.loopB, "minecraft"]
	},
	nprop=_nprop.char
)
code=["um","jesus","poo","jesus","skinny","skinny","jesus","um","jesus","poo","poo","poo","barack obama","minecraft","poo","jesus","skinny","skinny","skinny","minecraft","minecraft","minecraft","barack obama","barack obama","barack obama","poo","minecraft","barack obama","poo","joj","poo","poo","poo","joj","barack obama","joj","joj","barack obama","joj","skinny","skinny","skinny","skinny","poo","joj","skinny","um","joj","barack obama","barack obama","barack obama","barack obama","barack obama","joj","barack obama","joj","skinny","skinny","joj","skinny","poo","joj"]
bf.exec(code)
