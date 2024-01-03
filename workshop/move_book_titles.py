"""
This script moves the book titles of book chapters and the like from the annotation field to the bookTitle field. 
"""

from os.path import join
import re


incoming = join("workshop", "BIB18_incoming.bib")
outgoing = join("workshop", "BIB18_outgoing.bib")


def read_bibtex(): 
    with open(incoming, "r", encoding="utf8") as infile: 
        bibtex = infile.read()
    #print(bibtex[0:200])
    return bibtex


def move_title(bibtex): 
    entries = re.findall("(\@.*?)\n\n", bibtex, re.DOTALL)
    print("total entries:", len(entries))
    num_annotations = 0
    new_entries = ""
    for entry in entries[:]: 
        #print(entry)
        if "annotation =" in entry: 
            num_annotations +=1
            title = re.findall("annotation = \{Book\: (.*?)\}", entry)
            if title: 
                title = str(title[0])
                title = re.sub("\{", "", title)
                title = re.sub("\}", "", title)
                title = re.sub("\\\\", "", title)
                booktitle_str = "booktitle = {" + title + "},\n  annotation "
                #print(booktitle_str)
                try: 
                    new_entry = re.sub("annotation ", booktitle_str, entry)
                except: 
                    print(booktitle_str)
            #print(entry)
            new_entries = new_entries + new_entry + "\n\n"
        else: 
            new_entries = new_entries + entry + "\n\n"            
    return new_entries


def save_bibtex(bibtex): 
    with open(outgoing, "w", encoding="utf8") as outfile: 
        outfile.write(bibtex)
    print("Done.")


def main(): 
    bibtex = read_bibtex()
    bibtex = move_title(bibtex)
    save_bibtex(bibtex)

main()