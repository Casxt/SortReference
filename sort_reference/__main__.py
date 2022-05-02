from .SortReference import ExtraTextBlock, ExtraSimpleReference, ReorderReference, ReplaceSimpleReference
import zipfile
from lxml import etree
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="input file")
parser.add_argument("output", type=str, help="output file")
parser.add_argument("-v", dest="verbose", action="store_true", help="output file")
args = parser.parse_args()

from pathlib import Path
input_path = Path(args.input)
output_path = Path(args.output)
if not input_path.exists():
    print(f"{args.input} not exists.")
    exit(0)

if str(output_path.resolve().absolute()) == str(input_path.resolve().absolute()):
    print(f"can not output to input file.")
    exit(0)

archive = zipfile.ZipFile(args.input, 'r')

with archive.open('word/document.xml') as document:
    document_xml = document.read()
print("Scanning reference...")
root = etree.fromstring(document_xml)
texts = ExtraTextBlock(root)
refs, ref_texts = ExtraSimpleReference(texts)
if args.verbose:
    for ref, texts in zip(refs, ref_texts):
        content = "".join([t.text for t in texts])
        print(f"Found reference [{ref}] in snippet '{content}'")
print(f"Scanning reference complete, total {len(set(refs))} references found in {len(refs)} places.")

print("Analysis reference...")
ref_count, replace_map = ReorderReference(refs)
for ref, count in ref_count.items():
    if count == 1:
        print(f"WARNING: Reference [{ref}] used at just one place, which means it may only be used in your Reference section.")
change_ref_count = 0
change_place_count = 0
for old_id, new_id in replace_map.items():
    if old_id != new_id:
        change_ref_count += 1
        change_place_count += ref_count[old_id]
        if args.verbose:
            print(f"reference [{old_id}] now change to [{new_id}]")
print(f"Analysis reference complete, reorder {change_ref_count} references, {change_place_count} place will be changed.")

print("Reorder reference...")
ReplaceSimpleReference(texts, replace_map)

with zipfile.ZipFile(args.output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=archive.compresslevel) as dest:
    for file in archive.filelist:
        if file.filename == "word/document.xml":
            data = etree.tostring(root, encoding='UTF-8', standalone=True)
        else:
            data = archive.read(file.filename)
        dest.writestr(file.filename, data)
print("Reorder reference succeed!")
print("Don't forget to edit the Reference section manually.")