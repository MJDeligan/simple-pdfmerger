#! python3
from tkinter.filedialog import askopenfilenames, askdirectory
from PyPDF2 import PdfFileMerger
import os
import argparse
import sys

if __name__ == "__main__":
    desktop_path = os.path.expanduser("~/Desktop")
    # Setting up the parser
    parser = argparse.ArgumentParser(description="Merges PDFs")
    parser.add_argument(
        "--nogui",
        action="store_true",
        dest="nogui",
        help="Sets the program to take pdf-files and target directory as\
             command lines args instead of opening filedialog"
    )
    parser.add_argument(
        "-out",
        nargs="?",
        metavar="out_filename",
        dest="out",
        const="merged.pdf",
        default="merged.pdf",
        help='Name of the outputfile. Default: "merged.pdf"'
    )
    parser.add_argument(
        "-dir",
        nargs="?",
        metavar="directory",
        dest="dir",
        const=desktop_path,
        default=desktop_path,
        help="The directory to store the file in.\
             Only necessary when --nogui is used. Default: desktop"
    )
    parser.add_argument(
        "-pdfs",
        nargs="*",
        help="The pdfs you want to merge. Only necessary when --nogui is used."
    )
    args = parser.parse_args()

    # Merging section
    merger = PdfFileMerger()
    # use file dialog if option is set
    if args.nogui:
        files = [f for f in args.pdfs if f.endswith('.pdf')]  # filter non-pdfs
        dir = args.dir
    else:
        # get file selection and filter non pdfs
        title = (
            "Select Files to merge"
            " (File order might be different from selection order)"
        )
        unfiltered_files = askopenfilenames(title=title)
        files = [f for f in unfiltered_files if f.endswith('.pdf')]
        dir = askdirectory(title="Choose target directory")

    if not files:
        os.system("echo No valid pdf-files were provided for merging")
        sys.exit(1)
    os.system("echo Merging:")
    for file in files:
        os.system(f"echo {file}")
    # Append pdf extension to outputfile name if not there
    out_name = args.out if args.out.endswith(".pdf") else f"{args.out}.pdf"
    try:
        for pdf in files:
            merger.append(pdf)
    except Exception as e:
        os.system(f"echo {e}")
        os.system("echo Couldn't merge files")
        sys.exit(1)
    try:
        merger.write(os.path.join(dir, out_name))
        os.system("echo Files merged!")
    except Exception as e:
        os.system(f"echo {e}")
        os.system(f"echo Couldn't write to {os.path.join(dir, args.out)}")
    merger.close()
