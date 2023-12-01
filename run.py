from PyQt5.QtWidgets import QApplication
import sys
import subprocess

from main_window.main_window import MainWindow
from coder_parser.parser import parse
from coder_parser.coder import scheme_to_json

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
    # res = parse("scheme_json_files/example.json")
    # print(res["main"]._link)
    # scheme_to_json(res.values(), "scheme_json_files/coder_res.json")



# FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
#     filename = "scheme_json_files/sch1.json"
#     args = "stubs/stub_checker.exe " + filename
#     output = subprocess.run(args, capture_output=True)
#     print(f"out: {output.stdout}, \nerror: {output.stderr}")