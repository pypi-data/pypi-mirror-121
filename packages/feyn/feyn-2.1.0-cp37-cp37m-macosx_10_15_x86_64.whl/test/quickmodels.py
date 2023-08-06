from feyn._context import Context
from feyn._program import Program

def get_identity_model(inputs=["x"], output="y"):
    # Returns a model that predicts it's input, but scales it down and up internally
    ctx = Context()
    ctx.registers += [output] + inputs

    program = Program([10000, 10001], qid=1, autopad=True)
    model = ctx.to_model(program, output, {})
    model[0].params.update({"scale": 1, "w":2.0, "bias": +1})
    model[1].params.update({"scale": 1, "w":0.5, "bias": -.5})
    return model

def get_unary_model(inputs=["x"], output="y", fname="log", stypes={}):
    ctx = Context()
    ctx.registers += [output] + inputs

    opcode = ctx.lookup_by_fname(fname, 1)
    program = Program([10000, opcode, 10001], qid=1, autopad=True)
    return ctx.to_model(program, output, stypes)


def get_simple_binary_model(inputs, output, stypes={}):
    ctx = Context()
    ctx.registers += [output] + inputs

    program = Program([10000, 2000, 10001, 10002], qid=1, autopad=True)
    return ctx.to_model(program, output, stypes)


def get_complicated_binary_model(inputs, output, fname, stypes={}):
    ctx = Context()
    ctx.registers += [output] + inputs

    opcode = ctx.lookup_by_fname(fname, 1)

    program = Program([10000, 2000, opcode, 10001, 10002], qid=1, autopad=True)
    return ctx.to_model(program, output, stypes)


def get_ternary_model(inputs, output, stypes={}):
    ctx = Context()
    ctx.registers += [output] + inputs

    program = Program([10000, 2000, 2001, 10001, 10002, 10003], qid=1, autopad=True)
    return ctx.to_model(program, output, stypes)


def get_quaternary_model(inputs, output, stypes={}):
    ctx = Context()
    ctx.registers += [output] + inputs

    program = Program([10000, 2000, 2002, 2002, 10001, 10002, 10003, 10004], qid=1, autopad=True)
    return ctx.to_model(program, output, stypes)


def get_n_unique_models(n: int):
    ctx = Context()
    ctx.registers += ["y", "a"] + [f"x{i}" for i in range(n)]

    models = []
    for i in range(n):
        codes = [10000, 2000, 10001, 10002 + i]

        program = Program(codes, qid=1, autopad=True)
        model = ctx.to_model(program, "y")

        models.append(model)

    return models


def get_fixed_model():
    """
    Used in test_shap and test_importance_table.
    They expect specific states for the registers to be able to test against fixed shap values.
    """
    model = get_simple_binary_model(["x", "y"], "z")

    model[0].params.update({"scale": 1.7049912214279175, "w": 0.6332976222038269, "bias": 0.0})
    model[2].params.update({"scale": 1.0, "w": 0.9261354804039001, "bias": 0.18130099773406982})
    model[3].params.update({"scale": 1.0, "w": 2.7783772945404053, "bias": -0.18129898607730865})
    return model
