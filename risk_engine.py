def calculate_risk(country, severity):

    score = 0

    if country in ["Russia","China"]:
        score += 50

    if severity == "high":
        score += 40

    return score