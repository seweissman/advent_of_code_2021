
SAMPLE_INSTRUCTIONS="""inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 0
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y"""

# inp a - Read an input value and write it to variable a.
# add a b - Add the value of a to the value of b, then store the result in variable a.
# mul a b - Multiply the value of a by the value of b, then store the result in variable a.
# div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
# mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
# eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.

class Operation:
    def __init__(self, op, arg1, arg2):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    def size(self):
        if isinstance(self.arg1, Operation):
            size_arg1 = self.arg1.size()
        else:
            size_arg1 = 1
        if isinstance(self.arg2, Operation):
            size_arg2 = self.arg2.size()
        else:
            size_arg2 = 1
        return size_arg1 + size_arg2 + 1

    def __repr__(self):
        return self.op + "("  +  self.arg1.__repr__() + "," + self.arg2.__repr__() + ")"

    def copy(self):
        if isinstance(self.arg1, Operation):
            new_arg1 = self.arg1.copy()
        else:
            new_arg1 = self.arg1
        if isinstance(self.arg2, Operation):
            new_arg2 = self.arg2.copy()
        else:
            new_arg2 = self.arg2
        return Operation(self.op, new_arg1, new_arg2)

def test_sample():
    instructions = SAMPLE_INSTRUCTIONS.splitlines()
    state = run_instructions(instructions)
    z_state = state[3]
    print(z_state.size())
    print(z_state)
    simplify_tree(z_state)
    print(z_state.size())
    print(z_state)
VARS = ["w","x","y","z"]

def simplify_tree(op_tree, w_vals=None):    
    w_vals_dict = {}
    if w_vals:
        for i,v in enumerate(list(w_vals)):
            key = f"w{i+1}"
            val = int(v)
            w_vals_dict[key] = val


    #print(op_tree)
    if isinstance(op_tree,int):
        return op_tree
    if isinstance(op_tree, str):
        if op_tree in w_vals_dict:
            return w_vals_dict[op_tree]
        return op_tree
    op_tree.arg1 = simplify_tree(op_tree.arg1, w_vals)
    op_tree.arg2 = simplify_tree(op_tree.arg2, w_vals)
    if op_tree.op == "mul":
        if isinstance(op_tree.arg1, int) and isinstance(op_tree.arg2, int):
            return op_tree.arg1 * op_tree.arg2
        if op_tree.arg1 == 0 or op_tree.arg2 == 0:
            import pdb; pdb.set_trace()
            return 0
        if op_tree.arg1 == 1:
            return op_tree.arg2
        if op_tree.arg2 == 1:
            return op_tree.arg1
    if op_tree.op == "eql":
        if isinstance(op_tree.arg1, int) and isinstance(op_tree.arg2, int):
            return op_tree.arg1 == op_tree.arg2
        if isinstance(op_tree.arg1, str) and isinstance(op_tree.arg2, str):
            return op_tree.arg1 == op_tree.arg2
        if isinstance(op_tree.arg1, str) and greater_than_9(op_tree.arg2):
            return 0
        if isinstance(op_tree.arg2, str) and greater_than_9(op_tree.arg1):
            return 0
        if op_tree.arg1 == 0 and greater_than_0(op_tree.arg1):
            return 0
        if op_tree.arg2 == 0 and greater_than_0(op_tree.arg2):
            return 0
        if tree_equal(op_tree.arg1, op_tree.arg2):
            return 0
    if op_tree.op == "mod":
        if isinstance(op_tree.arg1, int) and isinstance(op_tree.arg2, int):
            return op_tree.arg1 % op_tree.arg2
        if isinstance(op_tree.arg1, str) and greater_than_9(op_tree.arg2):
            return op_tree.arg1
    if op_tree.op == "add":
        if isinstance(op_tree.arg1, int) and isinstance(op_tree.arg2, int):
            return op_tree.arg1 + op_tree.arg2
        if isinstance(op_tree.arg1, int) and op_tree.arg1 == 0:
            return op_tree.arg2
        if isinstance(op_tree.arg2, int) and op_tree.arg2 == 0:
            return op_tree.arg
    if op_tree.op == "div":
        if isinstance(op_tree.arg1, int) and isinstance(op_tree.arg2, int):
            return op_tree.arg1 // op_tree.arg2
        if isinstance(op_tree.arg2, int) and op_tree.arg2 == 1:
            return op_tree.arg1


    return op_tree

def greater_than_9(op_tree):
    if isinstance(op_tree, int):
        return op_tree > 9
    if isinstance(op_tree, str):
        return False
    if op_tree.op == "mul":
        if isinstance(op_tree.arg1, str) and isinstance(op_tree.arg2, int) and op_tree.arg2 > 1:
            return True
        if isinstance(op_tree.arg2, str) and isinstance(op_tree.arg1, int) and op_tree.arg1 > 1:
            return True
    if op_tree.op == "add":
        if isinstance(op_tree.arg1, str) and isinstance(op_tree.arg2, int) and op_tree.arg2 > 8:
            return True
        if isinstance(op_tree.arg2, str) and isinstance(op_tree.arg1, int) and op_tree.arg1 > 8:
            return True
        if greater_than_0(op_tree.arg1) and isinstance(op_tree.arg2, int) and op_tree.arg2 > 9:
            return True
        if greater_than_equal_0(op_tree.arg1) and isinstance(op_tree.arg2, int) and op_tree.arg2 >= 9:
            return True
        if greater_than_0(op_tree.arg2) and isinstance(op_tree.arg1, int) and op_tree.arg1 > 9:
            return True
        if greater_than_equal_0(op_tree.arg2) and isinstance(op_tree.arg1, int) and op_tree.arg1 >= 9:
            return True
    return False

def greater_than_0(op_tree):
    if isinstance(op_tree, int) and op_tree > 0:
        return True
    if isinstance(op_tree, int) and op_tree <= 0:
        return False
    if isinstance(op_tree, str):
        return True
    if op_tree.op == "add":
        return greater_than_0(op_tree.arg1) and greater_than_0(op_tree.arg2)
    if op_tree.op == "mul":
        return greater_than_0(op_tree.arg1) and greater_than_0(op_tree.arg2)
    if op_tree.op == "div":
        return greater_than_0(op_tree.arg1) and greater_than_0(op_tree.arg2)
    return False

def greater_than_equal_0(op_tree):
    if isinstance(op_tree, int) and op_tree >= 0:
        return True
    if isinstance(op_tree, int) and op_tree < 0:
        return False
    if isinstance(op_tree, str):
        return True
    if op_tree.op == "add":
        return greater_than_equal_0(op_tree.arg1) and greater_than_equal_0(op_tree.arg2)
    if op_tree.op == "mul":
        return greater_than_equal_0(op_tree.arg1) and greater_than_equal_0(op_tree.arg2)
    if op_tree.op == "div":
        return greater_than_equal_0(op_tree.arg1) and greater_than_0(op_tree.arg2)
    if op_tree.op == "eql":
        return True
    if op_tree.op == "mod":
        return True
    return False

def tree_equal(op_tree1, op_tree2):
    if isinstance(op_tree1, str) or isinstance(op_tree1, int) or isinstance(op_tree2, str) or isinstance(op_tree2, int):
        return op_tree1 == op_tree2
    if op_tree1.op != op_tree2:
        return False
    if op in ("add", "mul", "eq"):
        return ((tree_equal(op_tree1.arg1, op_tree2.arg1) and tree_equal(op_tree1.arg2, op_tree2.arg2)) or
                (tree_equal(op_tree1.arg1, op_tree2.arg2) and tree_equal(op_tree1.arg2, op_tree2.arg1)))
    return tree_equal(op_tree1.arg1, op_tree2.arg1) and tree_equal(op_tree1.arg2, op_tree2.arg2)


def run_instructions(instructions):
    # w x y z
    state = [0,0,0,0]
    input_idx = 1
    #import pdb; pdb.set_trace()
    for instruction in instructions:
        # if instruction == "add x 10":
        #     import pdb; pdb.set_trace()
        op,*args = instruction.split(" ")
        #print(op,*args)
        if op == "inp":
            arg1 = "w" + str(input_idx)
            #print("input variable", arg1)
            state[0] = arg1
            input_idx += 1
        else:
            arg1, arg2 = args
            idx1 = VARS.index(arg1)
            val1 = state[idx1]
            if arg2 in VARS:
                idx2 = VARS.index(arg2)
                val2 = state[idx2]
            else:
                val2 = int(arg2)
            if op == "add":
                if val1 == 0:
                    state[idx1] = val2
                elif val2 == 0:
                    state[idx1] = val1
                elif isinstance(val1, int) and isinstance(val2, int):
                    state[idx1] = val1 + val2
                elif isinstance(val1, Operation) or isinstance(val2, Operation) or isinstance(val1, str) or isinstance(val2, str):
                    state[idx1] = Operation("add", val1, val2)
            elif op == "mul":
                if val1 == 0 or val2 == 0:
                    state[idx1] = 0
                elif val1 == 1:
                    state[idx1] = val2
                elif val2 == 1:
                    state[idx1] = val1
                elif isinstance(val1, int) and isinstance(val2, int):
                    state[idx1] = val1 * val2
                elif isinstance(val1, Operation) or isinstance(val2, Operation) or isinstance(val1, str) or isinstance(val2, str):
                    state[idx1] = Operation("mul", val1, val2)
            elif op == "div":
                if val1 == val2:
                    state[idx1] = 1
                elif val2 == 1:
                    state[idx1] = val1
                elif isinstance(val1, int) and isinstance(val2, int):
                    state[idx1] = val1 // val2
                elif isinstance(val1, Operation) or isinstance(val2, Operation) or isinstance(val1, str) or isinstance(val2, str):
                    state[idx1] = Operation("div", val1, val2)
            elif op == "mod":
                if val1 == val2:
                    state[idx1] = 0
                elif isinstance(val1, int) and isinstance(val2, int):
                    state[idx1] = val1 % val2
                elif isinstance(val1, str) and val1.startswith("w") and isinstance(val2, int) and val2 > 10:
                    state[idx1] = val1
                elif isinstance(val1, Operation) or isinstance(val2, Operation) or isinstance(val1, str) or isinstance(val2, str):
                    state[idx1] = Operation("mod", val1, val2)
            elif op == "eql":
                if val1 == val2:
                    state[idx1] = 1
                elif isinstance(val1, int) and isinstance(val2, int):
                    state[idx1] = 0
                elif isinstance(val1, Operation) or isinstance(val2, Operation) or isinstance(val1, str) or isinstance(val2, str):
                    state[idx1] = Operation("eql", val1, val2)
                # elif isinstance(val1, str) and val1.startswith("w") and isinstance(val2, int) and val2 > 9:
                #     state[idx1] = 0
                # elif isinstance(val2, str) and val2.startswith("w") and isinstance(val1, int) and val1 > 9:
                #     state[idx1] = 0
                # elif isinstance(val1, str) and val1 in ["(w1 + 12)","((((w1 * 25) + (w2 + 6)) % 26) + 13)","((((((w1 * 25) + (w2 + 6)) * 25) + (w3 + 4)) % 26) + 13)"] and isinstance(val2, str) and val2.startswith("w"):
                #     state[idx1] = 0
                
        #state = [simplify_tree(s) for s in state]
    return state

if __name__ == "__main__":
    with open("input.txt") as file:
        instructions = file.read().splitlines()
    state = run_instructions(instructions)
    state_z = state[3]
    #print(state_z.size())
    state_z = simplify_tree(state_z)
    #        ..............
    input = "11111111486571"
    state_z = simplify_tree(state_z, input)
    if isinstance(state_z, int):
        print(input, state_z)
    else:
        print(state_z.size())

