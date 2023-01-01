# Lexial Analizer
# Mohsen Farajollahi - 991152143
# read the file
from prettytable import PrettyTable
table = PrettyTable()
table.field_names = ["line" , "char" , "block" , "tokenType" , "token"]
reader = open("input.txt" , "r")
writer = open("output.txt" , "w")
keywords = []

#function to add all keywords to array
def readKeyWords():
    kwfile = open("keywords.txt" , "r")
    for line in kwfile :
        keywords.append(line.strip())

def main():
    readKeyWords()
    delimiters = ['[' , ']' , '{' , '}' , ',' , ';' , '(' , ')' , '.']
    whiteSpace = ['\t' , '\n' , ' ']
    Operators = ['+' , '-' , '*' , '/' , '%' , '&' , '<' , '>' , '=' , '|' , '!' ]
    doubles = ["<=" , ">=" , "!=" , "==" , "||" , "&&" , "++" , "--" , "+=" , "-=" ,
        "/="]
    literalChars = ["\"" , "\'"]

    def out(text , ln , Coln , block , token):
        table.add_row([ln , Coln , block , token , text ])

    def isOperator(char1 , char2) :
        if ((char1 + char2) in doubles):
            return True
        else:
            return False

    ln = 0
    Coln = 0
    block = 1
    for line in reader:
        ln += 1
        Coln = 0
        while(Coln < len(line)):
            char = line[Coln]
            #check for literal
            if char in literalChars :
                mustFind = char
                temp = "" + char
                literalIndex = Coln
                Coln += 1
                while (Coln < len(line) and line[Coln] != mustFind):
                    temp += line[Coln]
                    Coln += 1
                temp += mustFind
                Coln += 1
                out(temp, ln, literalIndex, block, "literal")
                continue
            #skip the white space
            elif char in whiteSpace:
                Coln += 1
                continue
            #check for single line Comment
            elif char == "/" and line[Coln+1] == "/" :
                out(line, ln, Coln, block, "comment")
                break
            #check for delimiters
            elif char in delimiters :
                #increase and decrease block NO. in case if { , }
                if char == '{' :
                    block += 1
                elif char == '}' :
                    block -= 1
                out(char , ln , Coln , block , "delimiter")
                Coln += 1
            #check for operators
            elif char in Operators :
                char2 = line[Coln + 1]
                if (char2 in Operators and isOperator(char, char2)):
                    out(char + char2 , ln , Coln , block , "operator")
                    Coln += 2
                else:
                    out(char, ln, Coln, block, "operator")
                    Coln += 1
            #check for number
            elif char.isnumeric():
                numberIndex = Coln
                temp = "" + char
                Coln += 1
                while (Coln < len(line) and (temp + line[Coln]).isnumeric()):
                    temp += line[Coln].isnumeric()
                    Coln += 1
                out(temp, ln, numberIndex, block, "number")
            #check for identifier and keywords
            elif char.isalpha() or char == "_":
                wordIndex = Coln
                temp = char
                Coln += 1
                while (Coln < len(line) and (line[Coln].isalpha()
                or line[Coln].isnumeric() or line[Coln] == "_")):
                    temp += line[Coln]
                    Coln += 1
                #check if word is in keywords
                if temp in keywords :
                    out(temp, ln, wordIndex, block, "keyword")
                else:
                    out(temp, ln, Coln, block, "identifier")
    writer.write(table.get_string())
    writer.close()
    reader.close()
    return
if __name__ == "__main__" :
    main()
