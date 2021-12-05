import math
import sys
def print_bytes(a):
    bl=a.bit_length()//8
    residue=a.bit_length()%8
    if (residue!=0):
        bl+=1
    print(a.to_bytes(bl,"big"))
MODE_BINARY=0
MODE_8_BIT_ASCII=1
input_buffer=0
input_string=""
input_count=0
output_buffer=0
output_count=0
def my_output(bit, mode):
    global output_buffer,output_count
    if mode==MODE_BINARY:
        print(end=str(bit))
    elif mode==MODE_8_BIT_ASCII:
        output_buffer<<=1
        output_buffer+=bit
        output_count+=1
        if (output_count>=8):
            print(end=chr(output_buffer))
            output_count=0
            output_buffer=0

def my_input(mode):
    global input_buffer,input_string,input_count
    if mode==MODE_BINARY:
        while True:
            bit_in=input()
            if (not (bit_in=="0" or bit_in=="1")):
                print("Input must be 0 or 1")
            else:
                return int(bit_in)
    elif mode==MODE_8_BIT_ASCII:
        if(input_count==0 or input_count>=8):
            if (input_string==""):
                input_string=input()
            if (input_string==""):
                input_buffer=0
                input_string=""
                input_count=0
            else:
                input_buffer=ord(input_string[0])
                input_string=input_string[1:]
                input_count=0
        bit_in=input_buffer&128
        input_count+=1
        input_buffer<<=1
        input_buffer%=256
        return bit_in//128
        
                
            

def interpret(src_file, mode=MODE_BINARY):
    src_file.seek(0,2)
    size=src_file.tell()*8
    line_length=3
    line_num=1
    while(True):
        line_length=(line_num-1).bit_length()*2+3
        if(size>line_length*line_num>=size-8):
            break
        line_num+=1
    src_file.seek(0,0)
    raw_bytes=src_file.read(-1)
    entire_bitcode_in_int=int.from_bytes(raw_bytes,"big")
    shift_1_bit=entire_bitcode_in_int.bit_length()-1
    shift_x_bit=entire_bitcode_in_int.bit_length()-(line_num-1).bit_length()
    mask_1_bit=1
    mask_x_bit=(1<<(line_num-1).bit_length())-1

    while(True):
        A=(entire_bitcode_in_int>>shift_1_bit)&mask_1_bit
        shift_1_bit-=1
        shift_x_bit-=1
        B=(entire_bitcode_in_int>>shift_x_bit)&mask_x_bit
        shift_1_bit-=(line_num-1).bit_length()
        shift_x_bit-=(line_num-1).bit_length()
        C=(entire_bitcode_in_int>>shift_x_bit)&mask_x_bit
        shift_1_bit-=(line_num-1).bit_length()
        shift_x_bit-=(line_num-1).bit_length()
        D=(entire_bitcode_in_int>>shift_1_bit)&mask_1_bit
        shift_1_bit-=1
        shift_x_bit-=1
        E=(entire_bitcode_in_int>>shift_1_bit)&mask_1_bit
        shift_1_bit-=1
        shift_x_bit-=1
        if (int(D)==1):
            my_output(E,mode)
        if(A==1):
            bit_in=None
            while(not (bit_in==0 or bit_in==1)):

                bit_in=my_input(mode)
            if(bit_in==0):
                IP=B
            else:
                IP=C
        else: #A==0
            if (C==mask_x_bit):
                break
            IP=B

        shift_1_bit=entire_bitcode_in_int.bit_length()-1-IP*line_length
        shift_x_bit=entire_bitcode_in_int.bit_length()-(line_num-1).bit_length()-IP*line_length


    print()
        
    
        





if __name__ == "__main__":
    mode=MODE_BINARY
    if (sys.argv[1]=="-a"):
        src_file=open(sys.argv[2],"rb")
        mode=MODE_8_BIT_ASCII
    else:
        src_file=open(sys.argv[1],"rb")
    interpret(src_file,mode)
