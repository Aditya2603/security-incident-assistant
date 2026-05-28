mapping = {

    "Impossible Travel":
    "T1078",

    "Brute Force":
    "T1110"
}

def get_technique(alert):

    return mapping.get(
        alert,
        "Unknown"
    )