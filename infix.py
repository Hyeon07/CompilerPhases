OPERATORS=set(['+','-','*','/','(',')','%','^'])
PRIORITY={'+':1,'-':1,'*':2,'/':2,'%':2,'^':3}
def infix_to_postfix(expression):
    stack=[]
    op=''
    for ch in expression:
        if ch not in OPERATORS:
            op+=ch
        elif ch=='(':
            stack.append('(')
        elif ch==')':
            while stack and stack[-1]!='(':
                op=stack.pop()
            stack.pop()
        else:
            while stack and stack[-1]!='(' and PRIORITY[ch]<=PRIORITY[stack[-1]]:
                op+=stack.pop()
            stack.append(ch)
    while stack:
        op+=stack.pop()
    return op
def PostfixResult(expr):
    post=infix_to_postfix(expr)
    stack=[]
    for i in post:
        if i.isnumeric():
            stack.append(i)
        elif i=='*':
            stack.append(int(stack.pop())*int(stack.pop()))
        elif i=='+':
            stack.append(int(stack.pop())+int(stack.pop()))
        elif i=='-':
            first=int(stack.pop())
            second=int(stack.pop())
            stack.append(second-first)
        elif i=='/':
            first=int(stack.pop())
            second=int(stack.pop())
            stack.append(second/first)
        elif i=='%':
            first=int(stack.pop())
            second=int(stack.pop())
            stack.append(second%first)
    return stack