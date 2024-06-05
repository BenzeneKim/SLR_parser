import pandas as pd
import sys
r = [[],['S' , 'CODE'],['CODE' , 'VDECL CODE' ],['CODE' , 'FDECL CODE' ],['CODE' , ''],['VDECL' , 'vtype id semi'],['VDECL' , 'vtype ASSIGN semi'],['ASSIGN' ,'id assign RHS'],['RHS' , 'EXPR' ],['RHS' , 'literal' ],['RHS' , 'character' ],['RHS' , 'boolstr'],['EXPR' , 'EXPR\' addsub EXPR'],['EXPR' , 'EXPR\' multdiv EXPR'],['EXPR' , 'EXPR\''],['EXPR\'' , 'lparen EXPR\' rparen'],['EXPR\'' , 'id'],['EXPR\'' , 'num'],['FDECL' , 'vtype id lparen ARG rparen lbrace BLOCK RETURN rbrace'],['ARG' , 'vtype id MOREARGS' ],['ARG' , ''],['MOREARGS' , 'comma vtype id MOREARGS' ],['MOREARGS' , ''],['BLOCK' , 'STMT BLOCK' ],['BLOCK' , ''],['STMT' , 'VDECL' ],['STMT' , 'ASSIGN semi'],['STMT' , 'if lparen COND rparen lbrace BLOCK rbrace ELSE'],['STMT' , 'while lparen COND rparen lbrace BLOCK rbrace'],['COND' , 'COND comp COND\''],['COND' , 'COND'],['COND\'', 'boolstr'],['ELSE' , 'else lbrace BLOCK rbrace'],['ELSE' , ''],['RETURN' , 'return RHS semi']]
stack = []
current_state = 0
handle = 0
table = pd.read_excel(r'C:\Workspace\1_Univ\CAU\3-1\Compiler\SLR.xlsx')
input_string = str(open(sys.argv[1], 'r').readline())
input_string = input_string.split(' ')
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
        input_symbol, next_input_symbol = input_string[handle], input_string[handle+1]
        print(input_symbol)
        action = table[input_symbol][current_state]
        print(action)
        if type(action) != str:
            print('error')
            break
        elif action[0] == 's':
            handle += 1
            current_state = int(action[1:])
            stack.append(current_state)
        else:
            print(r[int(action[1:])])
            length  = func_length(r[int(action[1:])][1])
            print("length : " + str(length))
            for _ in range(length):
                stack.pop()
                input_string.remove(handle-length+1)
            handle -= length-1
            input_string.insert(handle, r[int(action[1:])][0])
            current_state = stack[len(stack)-1]
            print(current_state)