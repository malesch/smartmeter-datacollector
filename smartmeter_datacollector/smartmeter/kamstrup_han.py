#
# Copyright (C) 2023 Supercomputing Systems AG
# This file is part of smartmeter-datacollector.
#
# SPDX-License-Identifier: GPL-2.0-only
# See LICENSES/README.md for more information.
#
import logging
from typing import Optional

import serial

from .cosem import Cosem
from .meter import MeterError, SerialHdlcDlmsMeter
from .reader import ReaderError
from .serial_reader import SerialConfig

LOGGER = logging.getLogger("smartmeter")


class KamstrupHAN(SerialHdlcDlmsMeter):
    BAUDRATE = 2400
    DATA_BITS = serial.EIGHTBITS
    PARITY = serial.PARITY_NONE
    STOP_BITS = serial.STOPBITS_ONE

    def __init__(self, port: str,
                 baudrate: int,
                 data_bits: int,
                 parity: str,
                 stop_bits: int,
                 decryption_key: Optional[str] = None,
                 use_system_time: bool = False) -> None:
        serial_config = SerialConfig(
            port=port,
            baudrate=baudrate,
            data_bits=data_bits,
            parity=parity,
            stop_bits=stop_bits,
            termination=SerialHdlcDlmsMeter.HDLC_FLAG
        )
        cosem = Cosem(fallback_id=port)
        try:
            super().__init__(serial_config, cosem, decryption_key, use_system_time)
        except ReaderError as ex:
            LOGGER.fatal("Unable to setup serial reader for Kamstrup HAN. '%s'", ex)
            raise MeterError("Failed setting up Kamstrup HAN.") from ex

        LOGGER.info("Successfully set up Kamstrup HAN smart meter on '%s'.", port)
