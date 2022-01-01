

SAMPLE_INSTRUCTIONS_14="""inp w
mul x 0
add x z
mod x 26
div z 26
add x -1
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 5
mul y x
add z y"""

SAMPLE_INSTRUCTIONS_13="""inp w
mul x 0
add x z
mod x 26
div z 26
add x -1
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y"""

SAMPLE_INSTRUCTIONS_12 = """inp w
mul x 0
add x z
mod x 26
div z 26
add x -4
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
"""

def test_sample():
    instructions = SAMPLE_INSTRUCTIONS_12.splitlines()
    state = run_instructions(instructions, [0,"x","y","z"])
    z_state = state[3]
    print(z_state.size())
    print(z_state)
    simplify_tree(z_state)
    print(z_state.size())
    print(z_state)


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


def run_instructions(instructions, state=(0,0,0,0), input_idx_start=1):
    state = list(state)
    input_idx = input_idx_start
    for instruction in instructions:
        op,*args = instruction.split(" ")
        if op == "inp":
            arg1 = "w" + str(input_idx)
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
    return state

if __name__ == "__main__":
    with open("input.txt") as file:
        instructions = file.read().splitlines()

    w_vals="94992994195998"
    instructions_block = [instructions[0]]
    block_ct = 1
    #import pdb; pdb.set_trace()
    state = (0,0,0,0)
    for i in range(1,len(instructions)):
        if instructions[i].startswith("inp"):
            state = run_instructions(instructions_block, state=state, input_idx_start=block_ct)
            print(state[3])
            state = [simplify_tree(s, w_vals=w_vals) for s in state]
            print(f"z{block_ct}=",state[3])
            print("\n")
            instructions_block = []
            block_ct += 1
        instructions_block.append(instructions[i])
    state = run_instructions(instructions_block, state=state, input_idx_start=block_ct)
    print(state[3])
    state = [simplify_tree(s, w_vals=w_vals) for s in state]
    print(f"z{block_ct}=",state[3])
    
    state = run_instructions(instructions)
    state_z = state[3]
    val = simplify_tree(state_z, w_vals="94992994195998")
    print("Part 1 is it 0?", val)

    state = run_instructions(instructions)
    state_z = state[3]
    val = simplify_tree(state_z, w_vals="21191861151161")
    print("Part2 is it 0?", val)


"""
z1= w1
z2= add(mul('w1',        add(mul(25,eql(eql(add(w1,12),'w2'),0)),1)),mul(add('w2',6),eql(eql(add(w1,12),'w2'),0)))
    if w2 = w1 + 12:  NOT POSSIBLE
        z2 = w1
    if w2 != w1 + 12:
        z2 = 26*w1 + w2 + 6
z3= add(mul('z2',        add(mul(25,eql(eql(add(mod('z2',26),13),'w3'),0)),1)),mul(add('w3',4),eql(eql(add(mod('z2',26),13),'w3'),0)))
    if w3 = mod(z2, 26) + 13: NOT POSSIBLE
        z3 = z2
    if w3 != mod(z2, 26) + 13:
        z3 = 26*z2 + w3 + 4
z4= add(mul('z3',        add(mul(25,eql(eql(add(mod('z3',26),13),'w4'),0)),1)),mul(add('w4',2),eql(eql(add(mod('z3',26),13),'w4'),0)))
    if w4 = mod(z3, 26) + 13: NOT POSSIBLE
        z4 = z6
    if w4 != mod(z3, 26) + 13:
        z4 = 26*z3 + w4 + 2
z5= add(mul('z4',        add(mul(25,eql(eql(add(mod('z4',26),14),'w5'),0)),1)),mul(add('w5',9),eql(eql(add(mod('z4',26),14),'w5'),0)))
    if w5 = mod(z4, 26) + 14: NOT POSSIBLE
        z5 = z4
    if w5 != mod(z4, 26) + 14:
        z5 = 26*z4 + w5 + 9
z6= add(mul(div('z5',26),add(mul(25,eql(eql(add(mod('z5',26),-2),'w6'),0)),1)),mul(add('w6',1),eql(eql(add(mod('z5',26),-2),'w6'),0)))
    if w6 = mod(z5, 26) - 2:
        z6 = div(z5,26)
    if w6 != mod(z5, 26) - 2:
        z6 = z5 + w6 + 1
z7= add(mul('z6',        add(mul(25,eql(eql(add(mod('z6',26),11),'w7'),0)),1)),mul(add('w7',10),eql(eql(add(mod('z6',26),11),'w7'),0)))
    if w7 = mod(z6, 26) + 11: IMPOSSIBLE
        z7 = z6
    if w7 != mod(z8, 26) + 11:
        z7 = 26*z6 + w7 + 10
z8= add(mul(div('z7',26),add(mul(25,eql(eql(add(mod('z7',26),-15),'w8'),0)),1)),mul(add('w8',6),eql(eql(add(mod('z7',26),-15),'w8'),0)))
    if w8 = mod(z7, 26) - 15:
        z8 = div(z7,26)
    if w8 != mod(z8, 26) - 15:
        z8 = z7 + w8 + 6
z9= add(mul(div('z8',26),add(mul(25,eql(eql(add(mod('z8',26),-10),'w9'),0)),1)),mul(add('w9',4),eql(eql(add(mod('z8',26),-10),'w9'),0)))
    if w9 = mod(z8, 26) - 10:
        z9 = div(z8,26)
    if w9 != mod(z8, 26) - 10:
        z9 = z8 + w9 + 4
z10= add(mul('z9',add(mul(25,eql(eql(add(mod('z9',26),10),'w10'),0)),1)),mul(add('w10',6),eql(eql(add(mod('z9',26),10),'w10'),0)))
    if w10 = mod(z9, 26) + 10:
        z10 = z9
    if w10 != mod(z9, 26) + 10:
        z10 = 26*z9 + w10 + 6
z11= add(mul(div('z10',26),add(mul(25,eql(eql(add(mod('z10',26),-10),'w11'),0)),1)),mul(add('w11',3),eql(eql(add(mod('z10',26),-10),'w11'),0)))
    if w11 = mod(z10, 26) - 10:
        z11 = div(z10,26)
    if w11 != mod(z11, 26):
        z11 = z10 + w11 + 3
z12= add(mul(div('z11',26),add(mul(25,eql(eql(add(mod('z11',26),-4),'w12'),0)),1)),mul(add('w12',9),eql(eql(add(mod('z11',26),-4),'w12'),0)))
    if w12 = mod(z11, 26) - 4:
        z12 = div(z11,26)
    if w12 != mod(z12, 26):
        z12 = z11 + w12 + 9
z13= add(mul(div('z12',26),add(mul(25,eql(eql(add(mod('z12',26),-1),'w13'),0)),1)),mul(add('w13',15),eql(eql(add(mod('z12',26),-1),'w13'),0)))
    if w13 = mod(z12, 26) - 1:
        z13 = div(z12,26)
    if w13 != mod(z12, 26):
        z13 = z12 + w13 + 15

z14= add(mul(div('z13',26),add(mul(25,eql(eql(add(mod('z13',26),-1),'w14'),0)),1)),mul(add('w14',5),eql(eql(add(mod('z13',26),-1),'w14'),0)))
    if w14 = mod(z13, 26) - 1:
        z14 = div(z13,26) == 0
    if w14 != mod(z13, 26):
        z14 = z13 + w14 + 5 == 0

"""