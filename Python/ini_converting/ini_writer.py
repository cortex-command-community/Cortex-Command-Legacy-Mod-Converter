from pathlib import Path
from Python import shared_globals as cfg


def write_converted_ini_cst(parsed_portion, output_folder_path):
    for name, dict_or_list in parsed_portion.items():
        if isinstance(
            dict_or_list, dict
        ):  # If dict_or_list contains a dictionary of more filenames.
            write_converted_ini_cst(dict_or_list, Path(output_folder_path) / name)
        else:  # Else dict_or_list contains a list of the sections of a file.
            p = str(Path(output_folder_path) / name)
            with open(p, mode="w") as f:
                lines = []
                for section in dict_or_list:
                    write_recursively(section, lines)
                f.write("".join(lines))
                cfg.progress_bar.inc()
                cfg.progress_bar.setSubtext(f"writing file {p}")


def write_recursively(line_tokens, lines):
    for token in line_tokens:
        if token["type"] != "children":
            lines.append(token["content"])
        elif token["type"] == "children":
            for new_line_tokens in token["content"]:
                write_recursively(new_line_tokens, lines)
