import math

def sympify_element(elm, symbolic_lr=False, include_weights=True):
    import sympy
    mname = lambda s: s.replace(" ","_").replace('_', '').replace('.', '').replace('-', '')
    num_rep = lambda n: n+'_in' if n.isdigit() else n
    cat_rep = lambda c: c+'_cat'
    fmt = lambda s: f"{s:.{15}e}"

    if elm.fname == "in:linear":
        num_str = num_rep(mname(elm.name))
        s = f"{num_str} * {fmt(elm.params['scale'])} * {fmt(elm.params['w'])} + {fmt(elm.params['bias'])}" if include_weights else num_str
    elif elm.fname == "in:cat":
        cat_str = cat_rep(mname(elm.name))
        s = f"{cat_str} + {fmt(elm.params['bias'])}" if include_weights else cat_str
    elif elm.fname =="multiply":
        s = "__x0__ * __x1__"
    elif elm.fname =="add":
        s = "__x0__ + __x1__"
    elif elm.fname =="linear" and elm.name == "":
        s = f"{fmt(elm.params['w0'])} * __x0__ + {fmt(elm.params['bias'])}" if include_weights else '__x0__'
    elif elm.fname =="tanh":
        s = "tanh(__x0__)"
    elif elm.fname =="inverse":
        s = "1/__x0__"
    elif elm.fname =="log":
        s = "log(__x0__)"
    elif elm.fname =="exp":
        s = "exp(__x0__)"
    elif elm.fname == "gaussian2":
        s = "exp(-(__x0__**2 / .5 +__x1__**2 / .5))" if include_weights else "exp(-(__x0__**2 +__x1__**2))"
    elif elm.fname == "gaussian1":
        s = "exp(-(__x0__**2 / .5))" if include_weights else "exp(-(__x0__**2))"
    elif elm.fname == "sqrt":
        s = "sqrt(__x0__)"
    elif elm.fname == "squared":
        s = "__x0__**2"
    elif elm.fname == "out:linear":
        s = f"{fmt(elm.params['scale'])} * ({fmt(elm.params['w'])} * __x0__ + {fmt(elm.params['bias'])})" if include_weights else '__x0__'
    elif elm.fname == "out:lr":
        output = f"{fmt(elm.params['w'])} * __x0__ + {fmt(elm.params['bias'])}" if include_weights else '__x0__'
        if symbolic_lr:
            s = f"1/(1+exp(-({output})))"
        else:
            s = f"logreg({output})"
    else:
        raise ValueError("Unsupported %s"% elm.fname)

    return sympy.sympify(s)

def _signif(x, digits):
    if x == 0 or not math.isfinite(x):
        return x
    digits -= math.ceil(math.log10(abs(x)))
    return round(x, digits)

def _round_expression(expr, digits):
    import sympy
    for a in sympy.preorder_traversal(expr):
        if isinstance(a, sympy.Float):
            expr = expr.subs(a, _signif(a, digits))

    return expr

def sympify_model(m, signif=6, symbolic_lr=False, include_weights=True):
    exprs = [sympify_element(elm, symbolic_lr=symbolic_lr, include_weights=include_weights) for elm in m]

    for elm in reversed(list(m)):
        if elm.arity > 0:
            exprs[elm._ix] = exprs[elm._ix].subs({"__x0__": exprs[elm.children[0]]})
        if elm.arity > 1:
            exprs[elm._ix] = exprs[elm._ix].subs({"__x1__": exprs[elm.children[1]]})

    return _round_expression(exprs[0], signif)
