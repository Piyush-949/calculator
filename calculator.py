import ast
import operator as op
import tkinter as tk

# Safe arithmetic evaluator replacing insecure eval()
_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def safe_calculate(expression: str):
    """Safely evaluates basic arithmetic expressions without arbitrary code execution."""
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        elif isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](_eval(node.operand))
        raise ValueError("Unsupported operation")

    parsed = ast.parse(expression.strip(), mode="eval")
    result = _eval(parsed)
    # Return int if result is an exact whole number
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result

def click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = safe_calculate(screen.get())
            screen.set(result)
        except Exception:
            screen.set("Error")
    elif text == "C":
        screen.set("")
    else:
        screen.set(screen.get() + text)

root = tk.Tk()
root.title("Calculator")
root.geometry("300x400")

screen = tk.StringVar()
entry = tk.Entry(root, textvar=screen, font="Arial 20")
entry.pack(fill="both", ipadx=8, pady=10)

buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", "C", "=", "+"
]

frame = tk.Frame(root)
frame.pack()

row = 0
col = 0

for button in buttons:
    b = tk.Button(frame, text=button, font="Arial 18", width=4, height=2)
    b.grid(row=row, column=col)
    b.bind("<Button-1>", click)
    col += 1
    if col > 3:
        col = 0
        row += 1

if __name__ == "__main__":
    root.mainloop()
