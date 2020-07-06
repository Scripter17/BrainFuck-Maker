# Brainfuck-Maker

A Python module that makes it easy to make any kind of [brainfuck](https://esolangs.org/wiki/BrainFuck) derivative you want

# Basic usage

#### Execute normal BF code
```Python
import bfm
BF=bfm.Brainfuck(bfm.defaultBF.rules, bfm.defaultBF.state)
BF.run("+[-[<<[+[--->]-[<<<]]]>>>-]>-.---.>..>.<<<<-.<+.>>>>>.>.<<.<-.")
```

#### Custom operators

Let's say you want to add a custom doubling operator `*`. You would use the following code:
```Python
import bfm
def doubleOperator(self):
	self.state["tape"][self.state["pointer"]]*=2
BF=bfm.Brainfuck({
		"*":doubleOperator,
		**bfm.defaultBF.rules
	}, bfm.defaultBF.state)
BF.run("+******+.+.+.") # Expected output: ABC
```

#### Loops

And now let's say you want to add an if statement
```Python
import bfm
def ifBlock(self, code):
	if self.state["tape"][self.state["pointer"]]!=0:
		self.run(code)
BF=bfm.Brainfuck({
		"(":[ifBlock, ")"],
		**bfm.defaultBF.rules
	}, bfm.defaultBF.state)
BF.run("(.)+(.)") # Expected output: <0x01>
```

#### States
```Python
class defaultBF:
	state={
		"tape":[0 for x in range(30000)],
		"pointer":0
	}
```
Yeah you can just use any old object as a state variable
