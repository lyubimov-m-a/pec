#!/usr/bin/env python3
"""Pancreatitis encephalopathy calculator"""

import logging
import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from math import e

import coloredlogs
from PyQt6.QtWidgets import QApplication, QMainWindow

from const import ALGORITHMS, THRESHOLDS, UNKNOWN
from ui import Ui_MainWindow as MainWindow

LOG_FORMAT = "%(levelname)s %(message)s"
LOG_LEVEL_DEFAULT = "INFO"
LOGGER = logging.getLogger(__name__)


@dataclass()
class InputData:
    alcohol: bool = False
    bilirubin: float = 0
    creatinine: float = 0
    sofa: int = 0
    urea: float = 0

    def __setattr__(self, name, value):
        if getattr(self, name) != value:
            super().__setattr__(name, value)
            LOGGER.debug("Setting %s = %s", name, value)
            CALC.calculate_risk_day1()
            CALC.calculate_risk_day3()

    def reset(self):
        self.__init__()

class Calculator:
    def calculate_risk_day1(self):
        risk = 0
        if DATA.bilirubin and DATA.creatinine and DATA.sofa:
            z = (
                -7.001
                + 1.96 * DATA.alcohol
                - 0.024 * DATA.bilirubin
                + 0.009 * DATA.creatinine
                + 0.406 * DATA.sofa
            )
            risk = 1 / (1 + e**-z) * 100
            LOGGER.debug("Risk on day 1: %s", risk)
        WINDOW.set_risk(1, risk)

    def calculate_risk_day3(self):
        risk = 0
        if DATA.creatinine and DATA.sofa and DATA.urea:
            z = (
                -6.8
                + 1.27 * DATA.alcohol
                - 0.008 * DATA.creatinine
                + 0.165 * DATA.urea
                + 0.43 * DATA.sofa
            )
            risk = 1 / (1 + e**-z) * 100
            LOGGER.debug("Risk on day 3: %s", risk)
        WINDOW.set_risk(3, risk)


class UI(QMainWindow, MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def clear(self):
        DATA.reset()
        self.setupUi(self)

    def set_alcohol(self, alcohol: bool):
        DATA.alcohol = alcohol
        self.alcohol_1.setChecked(alcohol)
        self.alcohol_3.setChecked(alcohol)

    def set_bilirubin(self, bilirubin: float):
        DATA.bilirubin = bilirubin

    def set_creatinine(self, creatinine: float):
        DATA.creatinine = creatinine
        self.creatinine_1.setValue(creatinine)
        self.creatinine_3.setValue(creatinine)

    def set_risk(self, day: int, risk: float):
        value = f"{round(risk, 2)}%" if risk else UNKNOWN
        getattr(self, f"risk_{day}").setText(value)

        if value != UNKNOWN:
            threshold = "LOW" if risk <= THRESHOLDS[str(day)] else "HIGH"
            getattr(self, f"algorithm_{day}").setText(ALGORITHMS[f"{day}_{threshold}"])

    def set_sofa(self, sofa: int):
        DATA.sofa = sofa
        self.sofa_1.setValue(sofa)
        self.sofa_3.setValue(sofa)

    def set_urea(self, urea: float):
        DATA.urea = urea


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-ll",
        "--log-level",
        help=f"Set log level. Default: {LOG_LEVEL_DEFAULT}",
        nargs="?",
        default=LOG_LEVEL_DEFAULT,
    )
    arguments = parser.parse_args()

    numeric_level = getattr(logging, arguments.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {arguments.log_level}")
    coloredlogs.install(fmt=LOG_FORMAT, level=numeric_level)

    CALC = Calculator()
    DATA = InputData()

    app = QApplication(sys.argv)
    WINDOW = UI()
    WINDOW.show()
    sys.exit(app.exec())
