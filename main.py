import requests
import sqlite3
import json
import time
import os
import sys
import PyQt5
import matplotlib.pyplot as plt
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, \
    QCheckBox
import initialization


def main():
    checkInternetConnection = initialization.checkInternetConnection()
    isNewUser = initialization.isNewUserMethod()


