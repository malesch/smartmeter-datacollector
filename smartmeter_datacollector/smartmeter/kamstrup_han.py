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


class KamstrupHan(SerialHdlcDlmsMeter):
    def __init__(self, port: str, baudrate: int = 2400, decryption_key: Optional[str] = None) -> None:
        serial_config = SerialConfig(
            port=port,
            baudrate=baudrate,
            data_bits=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stop_bits=serial.STOPBITS_ONE,
            termination=SerialHdlcDlmsMeter.HDLC_FLAG
        )
        cosem = Cosem(fallback_id=port)
        try:
            super().__init__(serial_config, cosem, decryption_key)
        except ReaderError as ex:
            LOGGER.fatal("Unable to setup serial reader for Kamstrup HAN. '%s'", ex)
            raise MeterError("Failed setting up Kamstrup HAN.") from ex

        LOGGER.info("Successfully set up Kamstrup HAN smart meter on '%s'.", port)
