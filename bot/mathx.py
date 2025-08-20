from __future__ import annotations
import re, ast, math

OPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a**b,
    ast.USub: lambda a: -a,
    ast.UAdd: lambda a: +a,
}


def _num(s: str):
    m = re.search(r"-?\d+(\.\d+)?", s)
    return float(m.group()) if m else None


def _nums(s: str):
    return list(map(float, re.findall(r"-?\d+(?:\.\d+)?", s)))


def eval_expr(expr: str):
    repl = {
        "plus": "+",
        "minus": "-",
        "times": "*",
        "divided by": "/",
        "divide": "/",
        "over": "/",
        "mod": "%",
        "x": "*",
        "mins": "-",
        "min ": "- ",
    }
    for k, v in repl.items():
        expr = re.sub(rf"\b{k}\b", v, expr, flags=re.I)
    expr = re.sub(r"(\d+)\s*!", r"fact(\1)", expr)
    node = ast.parse(expr.replace("^", "**"), mode="eval").body

    def E(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](E(n.left), E(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in OPS:
            return OPS[type(n.op)](E(n.operand))
        if (
            isinstance(n, ast.Call)
            and getattr(n.func, "id", "") == "fact"
            and len(n.args) == 1
        ):
            v = E(n.args[0])
            if not float(v).is_integer() or v < 0:
                raise ValueError("factorial needs non-negative int")
            return math.factorial(int(v))
        raise ValueError("Unsupported")

    return E(node)


def math_verb(t: str):
    if m := re.search(r"\badd\s+(-?\d+(?:\.\d+)?)\s*(?:and\s*)?(-?\d+(?:\.\d+)?)", t):
        return float(m[1]) + float(m[2])
    if m := re.search(r"\bsubtract\s+(-?\d+(?:\.\d+)?)\s*from\s*(-?\d+(?:\.\d+)?)", t):
        return float(m[2]) - float(m[1])
    if m := re.search(
        r"\bmultiply\s+(-?\d+(?:\.\d+)?)\s*(?:by\s*)?(-?\d+(?:\.\d+)?)", t
    ):
        return float(m[1]) * float(m[2])
    if m := re.search(r"\bdivide\s+(-?\d+(?:\.\d+)?)\s*(?:by\s*)?(-?\d+(?:\.\d+)?)", t):
        return float(m[1]) / float(m[2])
    return None


def conversions(text: str):
    def n():
        return _num(text)

    t = text.lower()
    if any(k in t for k in ("km", "kilometer", "kilometre")) and "mile" in t:
        x = n()
        return (
            f"{x} km = {x*0.621371:.4f} miles"
            if x is not None
            else "Format: <number> km to miles"
        )
    if "mile" in t and any(k in t for k in ("km", "kilometer", "kilometre")):
        x = n()
        return (
            f"{x} miles = {x/0.621371:.4f} km"
            if x is not None
            else "Format: <number> miles to km"
        )
    if "kg" in t and any(k in t for k in ("pound", "lbs")):
        x = n()
        return (
            f"{x} kg = {x*2.20462:.4f} pounds"
            if x is not None
            else "Format: <number> kg to pounds"
        )
    if any(k in t for k in ("pound", "lbs")) and "kg" in t:
        x = n()
        return (
            f"{x} pounds = {x/2.20462:.4f} kg"
            if x is not None
            else "Format: <number> pounds to kg"
        )
    return None


def table_cmd(text: str):
    vs = _nums(text)
    if not vs:
        return "Format: table <number> [up to N]"
    base = int(vs[0])
    upto = int(vs[1]) if len(vs) > 1 else 10
    upto = max(1, min(upto, 25))
    return "\n".join([f"{base} x {i} = {base*i}" for i in range(1, upto + 1)])
