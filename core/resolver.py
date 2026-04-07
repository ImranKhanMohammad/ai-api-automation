import re

def resolve(data, context):
    if isinstance(data, dict):
        return {k: resolve(v, context) for k, v in data.items()}

    if isinstance(data, str):
        matches = re.findall(r"\{\{(.*?)\}\}", data)

        for m in matches:
            keys = m.split(".")
            val = context 
            try:
                for k in keys:
                    val = val[k]
                data = data.replace(f"{{{{{m}}}}}", str(val))
            except KeyError:
                print(f"[WARN] Could not resolve: {{{{{m}}}}}")

    return data