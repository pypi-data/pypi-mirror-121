from typing import List

import pyarrow as pa

class BlockWriter:
    """
    BlockWriter provides an interface to stream PyArrow records to a RecordBatch.

    If the Block gets too big (>6mb), it will automatically get written to S3.
    If not, the data is returned directly to the Lambda function.
    """
    def __init__(self, spill_location: str) -> None:
        pass

    def spilled(self) -> bool:
        pass

    def writeRows(self, rows: List[pa.RecordBatch]) -> None:
        pass