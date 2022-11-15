# Lexial Analizer
# Mohsen Farajollahi - 991152143
# read the file
from prettytable import PrettyTable
table = PrettyTable()
table.field_names = ["line" , "char" , "block" , "tokenType" , "token"]
reader = open("input.txt" , "r")
writer = open("output.txt" , "w")
def main():
    keywords = ['abstract', 'continue', 'class' 'for', 'new',
        'switch', 'default', 'package', 'synchronized',
        'boolean', 'do', 'if', 'private', 'this', 'break',
        'double', 'implements', 'protected', 'throw', 'byte',
        'else', 'import', 'public', 'throws', 'case', 'instanceof',
        'return', 'transient', 'catch', 'extends', 'int', 'short',
        'try', 'char', 'final', 'interface', 'static', 'void', 'class',
        'finally', 'long', 'volatile', 'float', 'native', 'super', 'while']
    delimiters = ['[' , ']' , '{' , '}' , ',' , ';' , '(' , ')' , '.']
    whiteSpace = ['\t' , '\n' , ' ']
    Operators = ['+' , '-' , '*' , '/' , '%' , '&' , '<' , '>' , '=' , '|' , '!' ]
    literalChars = ["\"" , "\'"]
    def out(text , ln , Coln , block , token):
        table.add_row([ln , Coln , block , token , text ])
        # writer.write(f"{text}\t{ln}\t{Coln}\t{block}\t{token}\n")
        return

    def isOperator(char1 , char2) :
        doubles = ["<=" , ">=" , "!=" , "==" , "||" , "&&" , "++" , "--" , "+=" , "-=" ,
        "/="]
        if ((char1 + char2) in doubles):
            return True
        else:
            return False

    def dump (temp , ln , coln , block) :
        if temp in keywords :
            out(temp, ln, Coln, block, "keyword")
        elif (temp[0] == "\"" and temp[-1] == "\"") or (temp[0] == "\'" and temp[-1] == "\'"):
            out(temp, ln, Coln, block, "literal")
        else :
            out(temp, ln, Coln, block, "identifier")
    ln = 0
    Coln = 0
    block = 1
    temp = ""
    isLiteral = False
    doubleOp = ""
    for line in reader:
        ln += 1
        Coln = 0
        charReader = iter(line)
        for char in charReader:
            Coln += 1
            # if len(temp) > 0 and (char in whiteSpace or char in Operators + delimiters + literalChars):
            #     if isLiteral and char not in literalChars:
            #         pass
            #     elif isLiteral and char in literalChars :
            #         dump(temp, ln, Coln, block)
            #         isLiteral = False
            #         temp = ""
            #     else :
            #         dump(temp, ln, Coln, block)
            #         isLiteral = False
            #         temp = ""
            if isLiteral :
                if char in literalChars :
                    temp += char
                    dump(temp, ln, Coln, block)
                    temp = ""
                    isLiteral = False
                    continue
                else :
                    temp += char
                    continue
            #check for delimiters
            if char in literalChars :
                temp += char
                isLiteral = True
                continue
            if char in whiteSpace:
                if isLiteral == True :
                    temp += char
                    continue
                else:
                    if len(temp) > 0 :
                        dump(temp, ln, Coln, block)
                        temp = ""
                    #Skip the whitespace
                    continue
            if char in delimiters :
                if len(temp) > 0 :
                    dump(temp, ln, Coln, block)
                    temp = ""
                #increase and decrease block NO. in case if { , }
                if char == '{' :
                    block += 1
                elif char == '}' :
                    block += 1
                out(char , ln , Coln , block , "delimiter")
            elif char in Operators :
                if len(temp) > 0 :
                    dump(temp, ln, Coln, block)
                    temp = ""
                char2 = next(charReader)
                if (char2 in Operators and isOperator(char, char2)):
                    out(char + char2 , ln , Coln , block , "operator")
                    continue
                else:
                    out(char, ln, Coln, block, "operator")
            else :
                temp += char
    writer.write(table.get_string())
    writer.close()
    reader.close()
    return
if __name__ == "__main__" :
    main()