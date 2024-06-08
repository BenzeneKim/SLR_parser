import pandas as pd
import sys
r = [['S' , 'CODE'],['CODE' , 'VDECL CODE' ],['CODE' , 'FDECL CODE' ],['CODE' , ''],['VDECL' , 'vtype id semi' ],['VDECL' , 'vtype ASSIGN semi'],['ASSIGN' , 'id assign RHS'],['RHS' , 'EXPR' ],['RHS' , 'literal' ],['RHS' , 'character' ],['RHS' , 'boolstr'],['EXPR' , 'EXPR addsub TERM'],['EXPR' , 'TERM'],['TERM' , 'TERM multdiv FACTOR'],['TERM' , 'FACTOR'],['FACTOR' , 'lparen EXPR rparen'],['FACTOR' , 'id'],['FACTOR' , 'num'],['FDECL' , 'vtype id lparen ARG rparen lbrace BLOCK RETURN rbrace'],['ARG' , 'vtype id MOREARGS' ],['ARG' , ''],['MOREARGS' , 'comma vtype id MOREARGS' ],['MOREARGS' , ''],['BLOCK' , 'STMT BLOCK'],['BLOCK' , ''],['STMT' , 'VDECL'],['STMT' , 'ASSIGN semi'],['STMT' , 'if lparen COND rparen lbrace BLOCK rbrace ELSE'],['STMT' , 'while lparen COND rparen lbrace BLOCK rbrace'],['COND' , 'COND comp COND\''],['COND' , 'COND\''],['COND\'', 'boolstr'],['ELSE' , 'else lbrace BLOCK rbrace'],['ELSE' , ''],['RETURN' , 'return RHS semi']]

stack = []
current_state = 0
handle = 0
table = pd.read_excel(r'.\SLR_new.xlsx')
table = pd.DataFrame(table)
input_string = str(open(sys.argv[1], 'r').readline())
input_string = input_string.split(' ')
input_string.append('$')

command = []

print(input_string)


def func_length(s):
    if s=='':
        return 0
    temp = s.split(' ')
    if temp == 0:
        return 1
    return len(temp)
# ----------------------------------------------------------- Algorithm --------------------------------------------------
if __name__ == "__main__":
    stack.append(current_state)
    while True:
        input_symbol = input_string[handle]
        current_state = stack.pop()
        action = table[input_symbol][current_state]
        #print(input_symbol+ ":"+ str(action))
        if str(action) == "nan":
            #print('error')
            print(f"handle position : {handle-1}, next input symbol : {input_string[handle]}")
            exit()
        elif type(action) == str and action[0] == 's':
            handle += 1
            stack.append(current_state)
            stack.append(int(action[1:]))
        elif type(action) == str and action[0] == 'r':
            #print(r[int(action[1:])])
            length  = func_length(r[int(action[1:])][1])
            #print(handle)
            command.append(int(action[1:]))
            for _ in range(length):
                #print(input_string)
                current_state = stack.pop()
                del input_string[handle-length]
            stack.append(current_state)
            input_string.insert(handle-length, r[int(action[1:])][0])
            #print(input_string)
            handle -= length
            stack.append(int(table[r[int(action[1:])][0]][current_state]))
            handle += 1
            #print(stack)
        elif action == 'acc':
            #print("Success!")
            command.reverse()
            #print(command)
            break
# ----------------------------------------------------------- #printing Code ----------------------------------------------
    output = [['CODE',[0]]]
    layer = 1
    index = 0
    i = 0
    max_layer=0
    while True:
        if len(command) == i:
            break
        #print(index)
        #print(r[command[i]][0])
        if len(output[index]) == 2 and  output[index][0] == r[command[i]][0] and len(output[index][1]) == layer:
            index2 = 0
            output[index].append("s")
            for j in r[command[i]][1].split(' '):
                temp = [j, []]
                for k in  output[index][1]:
                    temp[1].append(k)
                temp[1].append(index2)
                index2+=1
                output.append(temp)
            if max_layer<layer:
                max_layer = layer
            layer += 1
            i += 1
            #print(output)
            index = len(output)-1
            #print(index)
            #print(layer)
        else:
            index -= 1
            if index == -1:
                layer -= 1
                index = len(output)-1
    for i in output:
        if i[0] == '':
            i[0] = 'ε'
    
    result = []
    for i in range(max_layer+1):
        for j in range(len(output)):
            if len(output[j][1]) != i+1:
                continue
            if len(output[j][1]) == 1:
                result.append(output[j])
                break
            for k in range(len(result)):
                if output[j][1][-1] == 0 and result[k][1] == output[j][1][0:len(output[j][1])-1]:
                    result.insert(k, output[j])
                    break
                elif result[k][1][0:len(result[k][1])-1] == output[j][1][0:len(output[j][1])-1] and result[k][1][-1] == output[j][1][-1]-1:
                    result.insert(k, output[j])
                    break
    result.reverse()
    indent = ''
    for i in range(len(result)):
        if i == 0:
            print(result[i][0])
            continue
        if i < len(result)-1 and len(result[i+1][1]) == len(result[i][1]):
            indent = indent[0:(len(result[i][1])-2)*4]
            print(indent+'├── '+result[i][0])
            indent += "│   "
        elif i < len(result)-1:
            last = True
            for j in range(i+1,len(result)):
                if result[i][1][0:len(result[i][1])-1] == result[j][1][0:len(result[j][1])-1]:
                    last = False
                    break
            if last:
                indent = indent[0:(len(result[i][1])-2)*4]
                print(indent+'└── '+result[i][0])
                indent += "    "
            else:
                indent = indent[0:(len(result[i][1])-2)*4]
                print(indent+'├── '+result[i][0])
                indent += "│   "
        else:
            indent = indent[0:(len(result[i][1])-2)*4]
            print(indent+'└── '+result[i][0])
            indent += "    "
