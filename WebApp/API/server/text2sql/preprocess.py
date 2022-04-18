
from typing import List, Tuple

def default_preprocessing(schema: str, question: str, sql:str="") -> Tuple[str]:
    # For dataset builder
    schema = ", ".join(schema).upper()
    if sql == "":
        return schema, question

    else:
        return schema, question, sql

