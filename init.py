# CHIPSEL_M355 = 0  # define later
import sys
from dataclasses import dataclass

from AD5940 import SeqGenDB

AD5940ERR_OK = 0  # No error
REG_AFECON_CHIPID = 0x00000404  # AFECON Chip Identification
bIsS2silicon = False
AD5940LIB_VER_MAJOR = 0  # Major Number
AD5940LIB_VER_MINOR = 2  # Minor Number
AD5940LIB_VER_PATCH = 1  # Path Number


def AD5941_CsSet():
    pass


# Specify a method to print out debug message
def ADI_Print(message):
    print(message)


def AD5940_CsSet():
    pass


def AD5941_SEQWriteReg(RegAddr, RegData):
    pass


def AD5940_D2DWriteReg(RegAddr, RegData):
    pass


def AD5940_SPIWriteReg(RegAddr, RegData):
    pass


def AD5941_SEQReadReg(RegAddr):
    pass


def AD5941_D2DReadReg(RegAddr):
    pass


def AD5941_SPIReadReg(RegAddr):
    pass


def AD5941_WriteReg(RegAddr, RegData):
    if ('SEQUENCE_GENERATOR' in globals()):
        if (SeqGenDB.EngineStart == True):
            AD5941_SEQWriteReg(RegAddr, RegData)
        else:
            if ('CHIPSEL_M355' in globals()):
                AD5940_D2DWriteReg(RegAddr, RegData)
            else:
                AD5940_SPIWriteReg(RegAddr, RegData)


def AD5941_ReadReg(RegAddr):
    if ('SEQUENCE_GENERATOR' in globals()):
        if (SeqGenDB.EngineStart == True):
            return AD5941_SEQReadReg(RegAddr)
        else:
            if ('CHIPSEL_M355' in globals()):
                return AD5941_D2DReadReg(RegAddr)
            else:
                return AD5941_SPIReadReg(RegAddr)


def AD5941_Initialize(void):
    RegTable = [{b'\x09\x08': b'\x02\xc9'},
                {b'\x0c\x08': b'\x20\x6C'},
                {b'\x21\xF0': b'\x00\x10'}, ]
    if ('CHIPSEL_M355' in globals()):
        # This is AD5940
        RegTable.append({b'\x04\x10': b'\x02C9'})
        RegTable.append({b'\x0A\x28': b'\x0009'})
    else:
        # This is ADuCM355
        RegTable.append({b'\x04\x10': b'\x00\x1A'})
        RegTable.append({b'\x0A\x28': b'\x00\x08'})

    RegTable.append({b'\x23\x8C': b'\x01\x04'})
    RegTable.append({b'\x0A\x04': b'\x48\x59'})
    RegTable.append({b'\x0A\x04': b'\xF2\x7B'})
    RegTable.append({b'\x0A\x00': b'\x80\x09'})
    RegTable.append({b'\x22\xF0': b'\x00\x00'})
    RegTable.append({b'\x22\x30': b'\xDE\x87\xA5\xAF'})
    RegTable.append({b'\x22\x50': b'\x10\x3F'})
    RegTable.append({b'\x22\xB0': b'\x20\x3C'})
    RegTable.append({b'\x22\x30': b'\xDE\x87\xA5\xA0'})

    # Initialize global variables
    SeqGenDB.SeqLen = 0
    SeqGenDB.RegCount = 0
    SeqGenDB.LastError = AD5940ERR_OK
    SeqGenDB.EngineStart = False

    if ('CHIPSEL_M355' in globals()):
        AD5940_CsSet()

    for i in range(0, int(len(RegTable) / sys.getsizeof(RegTable[0]))):  # TODO: Check - Numerator < Denominator. Should be reverse for the loop to run
        reg_addr, reg_data = RegTable[i].items()
        AD5941_WriteReg(reg_addr, reg_data)

    i = AD5941_ReadReg(REG_AFECON_CHIPID)

    if (i == b'\x55\x01'):
        bIsS2silicon = True
    elif (i == b'\x55\x02'):
        bIsS2silicon = True
    elif (i == b'\x55\x00'):
        bIsS2silicon = False
    else:
        if 'ADI_DEBUG' not in globals():
            pass
        else:
            print("CHIPID read error:0x%04x. AD5940 is not present?\n", i)
            while (1):
                pass

    global bIsS2silicon
    if ('CHIPSEL_M355' in globals()):
        ADI_Print("This ADuCM355!\n")
    else:
        ADI_Print("This AD594x!\n")

    if 'ADI_DEBUG' in globals():
        ADI_Print("Note: Current Silicon is %s\n" + "S2" if bIsS2silicon else "S1")
        ADI_Print("AD5940LIB Version:v%d.%d.%d\n" + str(AD5940LIB_VER_MAJOR) + str(AD5940LIB_VER_MINOR) + str(AD5940LIB_VER_PATCH))
