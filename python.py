import pandas as pd
import sys
r = [['S' , 'CODE'],['CODE' , 'VDECL CODE' ],['CODE' , 'FDECL CODE' ],['CODE' , ''],['VDECL' , 'vtype id semi'],['VDECL' , 'vtype ASSIGN semi'],['ASSIGN' ,'id assign RHS'],['RHS' , 'EXPR' ],['RHS' , 'literal' ],['RHS' , 'character' ],['RHS' , 'boolstr'],['EXPR' , 'EXPR\' addsub EXPR'],['EXPR' , 'EXPR\' multdiv EXPR'],['EXPR' , 'EXPR\''],['EXPR\'' , 'lparen EXPR\' rparen'],['EXPR\'' , 'id'],['EXPR\'' , 'num'],['FDECL' , 'vtype id lparen ARG rparen lbrace BLOCK RETURN rbrace'],['ARG' , 'vtype id MOREARGS' ],['ARG' , ''],['MOREARGS' , 'comma vtype id MOREARGS' ],['MOREARGS' , ''],['BLOCK' , 'STMT BLOCK' ],['BLOCK' , ''],['STMT' , 'VDECL' ],['STMT' , 'ASSIGN semi'],['STMT' , 'if lparen COND rparen lbrace BLOCK rbrace ELSE'],['STMT' , 'while lparen COND rparen lbrace BLOCK rbrace'],['COND' , 'COND comp COND\''],['COND' , 'COND\''],['COND\'', 'boolstr'],['ELSE' , 'else lbrace BLOCK rbrace'],['ELSE' , ''],['RETURN' , 'return RHS semi']]
stack = []
current_state = 0
handle = 0
table = pd.read_excel(r'F:\Workspace\0_CAU\3-1\Compiler\SLR_parser\SLR.xlsx')
table = pd.DataFrame(table)
input_string = str(open(sys.argv[1], 'r').readline())
input_string = input_string.split(' ')
input_string.append('$')

command = []

print(input_string)

# input_string = list(map(str, input_string.split(' ')))

def func_length(s):
    if s=='':
        return 0
    temp = s.split(' ')
    if temp == 0:
        return 1
    return len(temp)

if __name__ == "__main__":
    stack.append(current_state)
    while True:
        input_symbol = input_string[handle]
        current_state = stack.pop()
        action = table[input_symbol][current_state]
        print(input_symbol+ ":"+ str(action))
        if action is None:
            print('error')
            break
        elif type(action) == str and action[0] == 's':
            handle += 1
            stack.append(current_state)
            stack.append(int(action[1:]))
        elif type(action) == str and action[0] == 'r':
            print(r[int(action[1:])])
            length  = func_length(r[int(action[1:])][1])
            print(handle)
            command.append(int(action[1:]))
            for _ in range(length):
                print(input_string)
                current_state = stack.pop()
                del input_string[handle-length]
            stack.append(current_state)
            input_string.insert(handle-length, r[int(action[1:])][0])
            print(input_string)
            handle -= length
            stack.append(int(table[r[int(action[1:])][0]][current_state]))
            handle += 1
            print(stack)
        elif action == 'acc':
            print("Success!")
            command.reverse()
            print(command)
            break
    output = [['CODE',[0]]]
    layer = 1
    index = 0
    i = 0
    while True:
        if len(command) == i:
            break
        print(index)
        print(r[command[i]][0])
        if output[index][0] == r[command[i]][0] and len(output[index][1]) == layer:
            index2 = 0
            for j in r[command[i]][1].split(' '):
                temp = [j, []]
                for k in  output[index][1]:
                    temp[1].append(k)
                temp[1].append(index2)
                index2+=1
                output.append(temp)
            layer += 1
            i += 1
            print(output)
            index = len(output)-1
            print(index)
            print(layer)
        else:
            index -= 1
            if index == -1:
                layer -= 1
                index = len(output)-1
    print(output)

# import os

# def print_tree(startpath, indent=''):
#     items = sorted(os.listdir(startpath))
#     for i, item in enumerate(items):
#         path = os.path.join(startpath, item)
#         is_last = i == len(items) - 1
#         if os.path.isdir(path):
#             print(f"{indent}{'└── ' if is_last else '├── '}{item}/")
#             new_indent = indent + ('    ' if is_last else '│   ')
#             print_tree(path, new_indent)
#         else:
#             print(f"{indent}{'└── ' if is_last else '├── '}{item}")

# if __name__ == '__main__':
#     startpath = '.'  # Replace with the desired starting directory path
#     print(startpath)
#     print_tree(startpath)
