# -*- coding: utf-8 -*-
import pip._internal

class Setup:
    @staticmethod
    def install(package: str):
        pip._internal.main(["install", package])

if __name__ == '__main__':
    Setup.install("requests")