import argparse
import os

import markdown


def get_file_text(filepath):
    with open(filepath) as fin:
        return fin.read()


def main(args):
    file_names = os.listdir(args.directory)
    file_names = [x for x in file_names if ".text" in x]

    template_text = get_file_text(args.template)

    for file_name in file_names:
        name, extension = os.path.splitext(file_name)
        filepath = os.path.join(args.directory, file_name)
        source_text = get_file_text(filepath)

        body = markdown.markdown(source_text, output_format='xhtml',
                                 extensions=['markdown.extensions.footnotes'])

        first_line = body.split('\n')[0]
        title = first_line.replace("</h1>", "").split("<br />")[1]
        new_file_text = template_text.replace("{{ body }}", body)
        new_file_text = new_file_text.replace("{{ title }}", title)
        new_file_text = new_file_text.replace("{{ type }}", "chapter")
        with open(os.path.join(args.directory, name + ".xhtml"), 'w') as fout:
            fout.write(new_file_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert conference speeches to xhtml") # noqa
    parser.add_argument("directory", help="Directory of markdown files")
    parser.add_argument("-t", "--template", help="Template file to use",
                        default="template.xhtml")
    args = parser.parse_args()
    main(args)
