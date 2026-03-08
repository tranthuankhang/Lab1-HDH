import sys
from models import Sys
from file_io import read_input_file, write_output_file

def main():
    if len(sys.argv) >= 3:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    else:
        input_filename = "Input.txt"
        output_filename = "Output.txt"
    
    System = Sys()
    read_input_file(System, input_filename)
    System.Run()
    System.calculate_time()
    write_output_file(System, output_filename)

if __name__ == "__main__":
    main()