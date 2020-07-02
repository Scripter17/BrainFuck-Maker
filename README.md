# BrainFuck-Maker

## A Python module that makes it easy to make any kind of BrainFuck derivative you want

# Basic usage

Execute normal BF code

```Python
import bfm
a=bfm.BrainFuck()
a.exec("+[-[<<[+[--->]-[<<<]]]>>>-]>-.---.>..>.<<<<-.<+.>>>>>.>.<<.<-.")
```

You may notice that, instead of printing "hello world", this just gets stuck forever (I think)\ 
This is because instead of each cell ranging from 0-255, the cells can be any integer.\ 
To fix this, change `BrainFuck()` to `BrainFuck(nprop="char")`

```Python
import bfm
a=bfm.BrainFuck(nprop="char")
a.exec("+[-[<<[+[--->]-[<<<]]]>>>-]>-.---.>..>.<<<<-.<+.>>>>>.>.<<.<-.")
```