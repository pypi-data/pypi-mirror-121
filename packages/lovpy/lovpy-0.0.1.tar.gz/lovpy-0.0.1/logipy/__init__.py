import sys
import atexit
import os
import logging

# Configure environment of tensorflow before importing any other module.
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
if os.environ.get("LOGIPY_DISABLE_GPU", 0) == "1":
    # Disable GPU usage.
    import tensorflow as tf
    tf.config.set_visible_devices([], 'GPU')

from .monitor.wrappers import LogipyPrimitive, logipy_call
from .models.train_model import load_or_train_model
from . import exception_handler
from . import config


LOGGER_NAME = "logipy"

session_name = os.environ.get("LOGIPY_SESSION_NAME", "")
temp_dir = os.environ.get("LOGIPY_TEMP_DIR", None)
config.tearup_logipy(session_name=session_name, temp_dir=temp_dir)

atexit.register(config.teardown_logipy)
if os.environ.get("LOGIPY_DEV_MODE", 0) == "1":
    sys.excepthook = exception_handler.logipy_dev_exception_handler
else:
    sys.excepthook = exception_handler.logipy_exception_handler


# Choose between hybrid and deterministic prover.
if config.is_neural_selector_enabled():
    logger = logging.getLogger(LOGGER_NAME)
    if not config.set_theorem_selector(config.TheoremSelector.HYBRID):
        config.set_theorem_selector(config.TheoremSelector.DETERMINISTIC)
        logger.warning("\tTrain a model by executing train_model.py script.")
        logger.warning("\tFalling back to deterministic theorem prover.")
