#!/usr/bin/python3
"""
Produce a hex diff file into structure raw data
"""

VERSION = '1.0.0'

USAGE = '''hexpack: parse hex diff file into structure raw data.
Usage:
	python hexpack.py [options] HEX_DIFF_FILE RAW_DATA_FILE
Options:
	-h, --help	this help message.
	-v, --version	version info.
'''

class Hexpack:

    '''
    function of parsing argv
    mainly get the diff file and the raw file
    '''
    def parse_args(self, argv):
        import getopt
        try:
            opts, args = getopt.gnu_getopt(argv, 'hv', ['help', 'version'])
            
            for o,a in opts:
                if o in ('-h', '--help'):
                    print(USAGE)
                    return 1
                elif o in ('-v', '--version'):
                    print(VERSION)
                    return 1
                    
        except getopt.GetoptError:
            e = sys.exc_info()[1]    # current exception
            sys.stderr.write(str(e)+"\n")
            sys.stderr.write(USAGE+"\n")
            return 1
            
        if len(args) != 2:
            sys.stderr.write("Error: You should specify the hex diff file and the raw data file.\n")
            sys.stderr.write(USAGE+"\n")
            return 1
        
        self.diff_file, self.raw_file = args

        return 0
    
    '''
    function of generate raw data file
    '''
    def generate(self):
        data_len = 40 # 4 byte for address, 4*4 byte for data. That's 20*2 = 40 chars.
        try:
            with open(self.diff_file, r"r") as f_diff, \
                open(self.raw_file, r"wb") as f_raw, \
                open(self.raw_file+".txt", r"w") as f_txt:

                # skip the first two lines
                f_diff.readline()
                f_diff.readline()

                count = 0
                for diff_line in f_diff:
                    if diff_line.startswith(r"+"):
                        end_index = diff_line.find(r"  |")
                        useful_data = diff_line[1:end_index].replace(' ', '').replace('-', 'F').strip()
                        f_raw.write(bytes.fromhex(useful_data.zfill(data_len)))
                        f_txt.write(useful_data+'\n')
                        # print("round {:8d} data is {}".format(count, useful_data))
                        count += 1

                f_raw.flush()
                f_txt.flush()

                f_diff.close()
                f_raw.close()
                f_txt.close()

                print("diff line is {}".format(count))

        except IOError:
            e = sys.exc_info()[1]    # current exception
            sys.stderr.write(str(e)+"\n")
            return 1

        return 0

'''
Main procedure 
'''
import sys
def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    hexpack_tool = Hexpack()
    ret = hexpack_tool.parse_args(argv)
    if (ret != 0):
        sys.stderr.write("parse args Error\n")
        return ret

    ret = hexpack_tool.generate()
    if (ret != 0):
        sys.stderr.write("generate Error\n")
        return ret

    return 0

'''
if main, may it used as module
'''
if __name__ == '__main__':
    sys.exit(main())