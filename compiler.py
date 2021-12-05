import sys, math
TOK_L=0
TOK_A=1
TOK_B=2
TOK_C=3
TOK_D=4
TOK_E=5
def numify_line(line):
    if (line[1]=="GOTO"):
        try:
            return[int(line[0]),0,int(line[2]),0,0,0]
        except IndexError:
            raise Exception("No Goto Destination")
        except ValueError:
            raise Exception()

    elif (line[1]=="IF" and line[3]=="THEN" and line[4]=="GOTO" and line[6]=="ELSE" and line[7]=="GOTO"):
        try:
            if(line[2]=="1"):

                return [int(line[0]),1,int(line[8]),int(line[5]),0,0]
            elif (line[2]=="0"):

                return [int(line[0]),1,int(line[5]),int(line[8]),0,0]
            else:
                raise Exception()
        except IndexError:
            raise Exception("No Goto Destination")
        except ValueError:
            raise Exception()
    elif (line[1]=="OUTPUT" and line[3]=="GOTO"):
        try:
            return[int(line[0]),0,int(line[4]),0,1,int(line[2])]
        except IndexError:
            raise Exception("No Goto Destination")
        except ValueError:
            raise Exception()
    elif (line[1]=="OUTPUT" and line[3] == "IF" and line[5] == "THEN" and line[6]=="GOTO" and line[8] == "ELSE" and line[9]=="GOTO"):
            try:
                if(line[4]=="1"):

                    return [int(line[0]),1,int(line[10]),int(line[7]),1,int(line[2])]
                elif (line[4]=="0"):

                    return [int(line[0]),1,int(line[7]),int(line[10]),1,int(line[2])]
                else:
                    raise Exception()
            except IndexError:
                raise Exception("No Goto Destination")
            except ValueError:
                raise Exception()
    else:
        raise Exception("Malformed Line")


def compile(src_file, dest_file=None):
    lines=src_file.readlines()
    total_lines=len(lines)
    lines_as_nums=[]
    max_line_num=0
    for line in lines:
        split_line=line.split()
        if (len(split_line)==0):
            continue
        labcde=numify_line(split_line )
        line_num=labcde[TOK_L]
        if (line_num > max_line_num):
            max_line_num=line_num
        success=False
        while(not success):
            try:
                lines_as_nums[line_num]=labcde
                success=True
            except IndexError:
                lines_as_nums.append(None)
                success=False
    max_line_num+=1
    length_line_addr_in_bits=max_line_num.bit_length()
    lines_as_nums.append([max_line_num, 0,0,(1<<length_line_addr_in_bits)-1, 0,0 ])
    line_length=length_line_addr_in_bits*2+3
    result=0

    for labcde in lines_as_nums:
        if (labcde == None):
            result<<=length_line_addr_in_bits*2+3
        else:
            result<<=1
            result+=labcde[TOK_A]
            result<<=length_line_addr_in_bits
            result+=labcde[TOK_B]
            result<<=length_line_addr_in_bits
            result+=labcde[TOK_C]
            result<<=2
            result+=labcde[TOK_D]*2+labcde[TOK_E]
    prg_size=line_length*len(lines_as_nums)
    if(prg_size%8!=0):
        result<<=(8-(prg_size%8))

    if (dest_file):
        dest_file.write(result.to_bytes(prg_size%8,"big"))
    else:
        print(result.to_bytes(math.ceil(result.bit_length()/8),'big'))







if __name__ == "__main__":
    src_file=open(sys.argv[1],"rt")
    argc=len(sys.argv)
    if (argc==2):
        compile(src_file)
    else:
        dest_file=open(sys.argv[2],"wb")
        compile(src_file,dest_file)
