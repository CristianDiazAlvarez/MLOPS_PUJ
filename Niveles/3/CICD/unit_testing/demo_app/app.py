def normalize_temperature(celsius: float) -> float:
    """Convierte celsius a fahrenheit con redondeo a 2 decimales."""
    return round((celsius * 9 / 5) + 32, 2)


def classify_score(score: float) -> str:
    """Clasifica un score continuo en etiquetas discretas."""
    if score < 0 or score > 1:
        raise ValueError("score debe estar entre 0 y 1")
    if score >= 0.8:
        return "high"
    if score >= 0.5:
        return "medium"
    return "low"
