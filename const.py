ALGORITHMS = {
    "1_LOW": """Интервенционная терапия:
    - отказ от лапаротомных
    хирургических вмешательств;
    - проведение грудной
    эпидуральной анальгезии.
Консервативная терапия:
    - энтеральная нутритивная
    поддержка;
    - стандартная терапия.""",
    "1_HIGH": """Интервенционная терапия:
    - отказ от всех хирургических методов
    лечения (при отсутствии «жизненных»
    показаний)
    - проведение грудной эпидуральной
    анальгезии.
Консервативная терапия:
    - энтеральная нутритивная поддержка;
    - отказ от наркотических анальгетиков
    и иммуномодуляторов.""",
    "3_LOW": "Стандартная терапия",
    "3_HIGH": """Стандартная + седативная терапия
Консультация невролога""",
}
THRESHOLDS = {
    "1": 15.5,
    "3": 20.5,
}
UNKNOWN = "N/A"
