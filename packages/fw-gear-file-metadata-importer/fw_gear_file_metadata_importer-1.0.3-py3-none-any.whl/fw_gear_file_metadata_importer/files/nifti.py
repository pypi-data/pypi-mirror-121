import logging
import typing as t

from fw_file.nifti import Nifti
from fw_meta import MetaData
from fw_utils import AnyPath

log = logging.getLogger(__name__)


def decode(val: bytes):
    """Decode decoded val or hex repr if cannot be decoded."""
    try:
        val = val.decode("utf-8")
    except UnicodeDecodeError:
        log.debug(f"Cannot decode bytes {val} in nifti_header.  Replacing with hex")
        val = val.hex()
    return val


def process(file_path: AnyPath) -> t.Tuple[t.Dict, MetaData, t.Dict]:
    """Process `file_path` and returns a `flywheel.FileEntry` and its corresponding meta.

    Args:
        file_path (Path-like): Path to input-file.

    Returns:
        dict: Dictionary of file attributes to update.
        dict: Dictionary containing the file meta.
        dict: Dictionary containing the qc metrics.

    """
    nifti_file = Nifti(file_path)
    # Populate header by getting values of iterated header keys.
    nifti_header = dict()
    for key in nifti_file:
        # Convert from numpy list to value
        val = nifti_file[key].tolist()
        # If still bytes try to decode, else use hex string.
        if isinstance(val, bytes):
            val = decode(val)
        nifti_header[key] = val
    fe = {"info": {"header": {"nifti": nifti_header}}}
    qc = {}
    return fe, nifti_file.get_meta(), qc
