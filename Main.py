# This is a lexical analyzer. A file is imported to go through and the text of that file is separated into tokens. To
# do this, a file is taken and checked to see if it is not blank. If not blank, the fle is read line by line. A class
# LexicalAnalyzer is initialized to 1, and a function tokenize sets the rules for key terms and what the lexical
# analyzer can accept. The analyzer is trained to separate tokens by whitespace. token_join is responsible for
# consolidating all the operator ids into one function that is then run on the code. An empty array is created for
# tokens, lexemes and rows. A for loop is created that is responsible for separating the input file into whichever
# category each word belongs along with its line number, filling up those earlier empty arrays. Lastly, those values
# are returned.

import re


# loads the test file and prepares it for use
def load_file():
    test_file = open('testfile.txt', 'r')
    text = test_file.readline()
    to_be_read = []

    while text != "":
        to_be_read.append(text)
        text = test_file.readline()

        if text == '':
            small_text_amount = ''.join(to_be_read)
            yield small_text_amount
            to_be_read = []

    test_file.close()


class LexicalAnalyzer:
    lin_num = 1

    # loads the terms being used for the test file and prints the output
    def tokenize(self, code):
        rules = [
            ('function', r'function'),
            ('terminate', r'end'),
            ('print_statement', r'print'),
            ('for_loop', r'for'),
            ('while_loop', r'while'),
            ('if_statement', r'if'),
            ('else', r'else'),
            ('MAIN', r'main'),
            ('id', r'[a-zA-Z]\w*'),
            ('literal_integer', r'\d(\d)*'),
            ('block', r'\( \)'),
            ('leftPar', r'\('),
            ('rightPar', r'\)'),
            ('le_operator', r'<='),
            ('lt_operator', r'<'),
            ('ge_operator', r'>='),
            ('gt_operator', r'>'),
            ('eq_operator', r'=='),
            ('assignment_operator', r'='),
            ('ne_operator', r'!='),
            ('add_operator', r'\+'),
            ('sub_operator', r'\-'),
            ('mul_operator', r'\*'),
            ('div_operator', r'\/'),
            ('NEXT_LINE', r'\n'),  # to go to next line
            ('EMPTY', r'[ \t]+'),  # White space

        ]

        tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        lin_start = 0
        tokens = []
        lexemes = []
        rows = []

        for x in re.finditer(tokens_join, code):
            token_type = x.lastgroup
            token_lexeme = x.group(token_type)

            if token_type == 'NEXT_LINE':
                tokens.append(token_type)
                lexemes.append("NEXT_LINE")
                lin_start = x.end()
                self.lin_num += 1
            elif token_type == 'EMPTY':
                continue
            else:
                tokens.append(token_type)
                lexemes.append(token_lexeme)
                rows.append(self.lin_num)

        return tokens, lexemes, rows


# gets the program started by creating the objects/data structures and calles the tokenize function.
if __name__ == '__main__':
    Analyzer = LexicalAnalyzer()
    token = []
    lexeme = []
    row = []
    for i in load_file():
        t, lex, lin = Analyzer.tokenize(i)
        token += t
        lexeme += lex
        row += lin

    lexemesByLine = []
    tokensByLine = []
    statementBlock = []
    statements = []
    branchList = []
    opList = []
    arithExpressionList = []
    relOpList = []
    errorLine = []
    errorToken = []
    errorBNF = []
    errorExpectedSyntax = []
    errorDescription = []
    assignedLex = []
    assignedVal = []
    lineCount = 1

    # This loop adds each branch of the statement to a list
    for x, y in zip(lexeme, token):
        if y != "NEXT_LINE":
            lexemesByLine.append(x)
            tokensByLine.append(y)
        elif y == "NEXT_LINE":
            if "for_loop" in tokensByLine:
                statementBlock.append("for_loop")
            elif "while_loop" in tokensByLine:
                statementBlock.append("while_loop")
            elif "print_statement" in tokensByLine:
                statementBlock.append("print_statement")
            elif "if_statement" in tokensByLine:
                statementBlock.append("if_statement")
            elif "terminate" in tokensByLine:
                statementBlock.append("terminate")
            elif "assignment_operator" in tokensByLine:
                statementBlock.append("assignment_statement")
            lexemesByLine.clear()
            tokensByLine.clear()

    # This loop descends down the branchs of the parse tree. It adds the parent nodes that have children to the
    # branch list. This list is how it will proceed down the branches.
    for x, y in zip(lexeme, token):
        if y != "NEXT_LINE":
            lexemesByLine.append(x)
            tokensByLine.append(y)
            if y == "leftPar":
                tokensByLine[tokensByLine.index(y)] = "("
            if y == "rightPar":
                tokensByLine[tokensByLine.index(y)] = ")"
            if y == "literal_integer":
                arithExpressionList.append(tokensByLine[tokensByLine.index(y)])
                tokensByLine[tokensByLine.index(y)] = "arithmetic_expression"
            if y == "le_operator" or y == "lt_operator" or y == "ge_operator" or y == "gt_operator" or y == \
                    "ne_operator":
                relOpList.append(tokensByLine[tokensByLine.index(y)])
                tokensByLine[tokensByLine.index(y)] = "relative_op"
            if y == "add_operator" or y == "sub_operator" or y == "mul_operator" or y == "div_operator":
                opList.append(tokensByLine[tokensByLine.index(y)])
                tokensByLine[tokensByLine.index(y)] = "arithmetic_op"
        elif y == "NEXT_LINE":
            for a in lexemesByLine:
                if a in assignedLex:
                    temp = lexemesByLine.index(a)
                    temp2 = assignedLex.index(a)
                    lexemesByLine.remove(a)
                    lexemesByLine.insert(temp, assignedVal[temp2])
            if "function" in tokensByLine:
                print("<program> -> ", *tokensByLine)
                print("<block> -> <statement>")
                lexemesByLine.clear()
                tokensByLine.clear()
                statements.append("statement")
                for i in statements:
                    print("<statement> -> ", *statementBlock)
            elif "while_loop" in tokensByLine:
                tokensByLine.remove(tokensByLine[0])
                lexemesByLine.remove(lexemesByLine[0])
                if tokensByLine[tokensByLine.index("relative_op") - 1] != "id" or \
                        tokensByLine[tokensByLine.index("relative_op") - 1] != "arithmetic_expression" or \
                        tokensByLine[tokensByLine.index("relative_op") + 1] != "id" or \
                        tokensByLine[tokensByLine.index("relative_op") + 1] != "arithmetic_expression":
                    errorLine.append(lineCount)
                    errorToken.append(tokensByLine[tokensByLine.index("relative_op")])
                    errorBNF.append(
                        "<while_loop> -> while < id/arithmetic_expression relative_op id/arithmetic_expression")
                    errorExpectedSyntax.append(lexemesByLine[tokensByLine.index("relative_op")])
                    errorDescription.append("The relative_op is in the wrong space."
                                            " its need to after an ID/literal_integer")
                print("<while_loop> -> while <", *tokensByLine, " >")
                for a in tokensByLine:
                    branchList.append(a)
                lexemesByLine.clear()
                tokensByLine.clear()
            elif "for_loop" in tokensByLine:
                tokensByLine.remove(tokensByLine[0])
                print("<for_loop> -> for <", *tokensByLine, " >")
                for a in tokensByLine:
                    branchList.append(a)
                lexemesByLine.clear()
                tokensByLine.clear()
            elif "print_statement" in tokensByLine:
                print("<print_statement> ->", *tokensByLine)
                branchList.append(a)
                lexemesByLine.clear()
                tokensByLine.clear()
            elif "if_statement" in tokensByLine:
                tokensByLine.remove(tokensByLine[0])
                lexemesByLine.remove(lexemesByLine[0])
                if tokensByLine[tokensByLine.index("relative_op") - 1] != "id" or \
                        tokensByLine[tokensByLine.index("relative_op") - 1] != "arithmetic_expression" or \
                        tokensByLine[tokensByLine.index("relative_op") + 1] != "id" or \
                        tokensByLine[tokensByLine.index("relative_op") + 1] != "arithmetic_expression":
                    errorLine.append(lineCount)
                    errorToken.append(tokensByLine[tokensByLine.index("relative_op")])
                    errorBNF.append(
                        "<if_statement> -> if < id/arithmetic_expression relative_op id/arithmetic_expression")
                    errorExpectedSyntax.append(lexemesByLine[tokensByLine.index("relative_op")])
                    errorDescription.append("The relative_op is in the wrong space."
                                            " its need to after an ID/literal_integer")
                print("<if_statement> -> if <", *tokensByLine, " >")
                for a in tokensByLine:
                    branchList.append(a)
                lexemesByLine.clear()
                tokensByLine.clear()
            elif "terminate" in tokensByLine:
                print("<terminate> -> end state")
                lexemesByLine.clear()
                tokensByLine.clear()
            elif "assignment_operator" in tokensByLine:
                # This is the error handling
                if tokensByLine[0] != "id" or tokensByLine[1] != "assignment_operator" or tokensByLine[2] == \
                        "arithmetic_op":
                    errorLine.append(lineCount)
                    errorToken.append(tokensByLine[2])
                    errorBNF.append(
                        "<assignment_statement> -> id/litteral_integer assignment_operator "
                        "id/litteral_integer arithmetic_op"
                        " id/literal_integer")
                    errorExpectedSyntax.append(lexemesByLine[2])
                    errorDescription.append("The arithmetic_op is in the wrong space. "
                                            "its need to after an ID/literal_integer")

                # This will be setting up the interpreter
                # assignedLex = []
                # assignedVal = []
                # res = [sub.replace('4', '1') for sub in test_list]

                if "arithmetic_op" not in tokensByLine:
                    assignedLex.append(lexemesByLine[0])
                    assignedVal.append(lexemesByLine[2])
                elif "arithmetic_op" in tokensByLine:
                    assignedLex.append(lexemesByLine[0])
                    assignedVal.append(
                        int(lexemesByLine[tokensByLine.index("arithmetic_op") - 1]) + int(
                            lexemesByLine[tokensByLine.index(
                                "arithmetic_op") + 1]))

                print("<assignment_statement> -> ", *tokensByLine)
                for a, b in zip(tokensByLine, lexemesByLine):
                    if "assignment_operator" not in branchList:
                        branchList.append(a)
                    elif a != "assignment_operator":
                        branchList.append(a)
                lexemesByLine.clear()
                tokensByLine.clear()
            lineCount += 1

    for e in branchList:
        if e == "assignment_operator":
            print("<assignment_operator> -> eq_operator")
        if e == "arithmetic_expression":
            print("<arithmetic_expression> -> ", arithExpressionList[0])
            arithExpressionList.remove(arithExpressionList[0])
        if e == "arithmetic_op":
            print("<arithmetic_op> -> ", opList[0])
            opList.remove(opList[0])
        if e == "relative_op":
            print("<relative_op> -> ", relOpList[0])
            relOpList.remove(relOpList[0])

    # This loop prints out the Lexical analyzer output below the parser's
    print("\n\nLexical Output")
    for d, q in zip(lexeme, token):
        if d and q != "NEXT_LINE":
            print(d, " -> ", q)

    # This loop prints out the errors found in the parser and the specified output with it.
    print("\n\nSyntax Errors \nThere are no errors\n")
    for a, b, c, d, e in zip(errorLine, errorToken, errorBNF, errorExpectedSyntax, errorDescription):
        print("Line Number: ", a)
        print("token: ", b)
        print("BNF Grammer: ", c)
        print("Expression: ", d)
        print("Description of error: ", e)
        print("\n")

    print("Assigned Lex", *assignedLex)
    print("Assigned Val", *assignedVal)
    print("System Output")
    for x, y in zip(lexeme, token):
        if y != "NEXT_LINE":
            lexemesByLine.append(x)
            tokensByLine.append(y)
        elif y == "NEXT_LINE":
            for a in lexemesByLine:
                if a in assignedLex:
                    temp = lexemesByLine.index(a)
                    temp2 = assignedLex.index(a)
                    lexemesByLine.remove(a)
                    lexemesByLine.insert(temp, assignedVal[temp2])
            if "print_statement" in tokensByLine:
                lexemesByLine.reverse()
                lexemesByLine.pop()
                if "+" in lexemesByLine:
                    print("FOUND IT")
                elif "-" in lexemesByLine:
                    print("FOUND IT")
                elif "*" in lexemesByLine:
                    print(int(lexemesByLine[lexemesByLine.index("*") - 1]) * int(
                        lexemesByLine[lexemesByLine.index(
                            "*") + 1]))
                    lexemesByLine.clear()
                elif "/" in lexemesByLine:
                    print("FOUND IT")

                print(*lexemesByLine)
                lexemesByLine.clear()
                tokensByLine.clear()

            lexemesByLine.clear()
            tokensByLine.clear()
