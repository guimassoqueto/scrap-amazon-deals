from re import findall


def get_category(element: str, delimiter: str = " > ") -> str:
    inner_text = findall(r">\n([\s/\n\w]+)<", element)
    if inner_text:
        return delimiter.join(
            set([txt.strip() for txt in inner_text if txt.strip() != ""])
        )
    return "Not Defined"
