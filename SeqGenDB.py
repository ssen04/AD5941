# Data base of Seq Generator
@dataclass
class SeqGenDB:
    EngineStart = None  # Flag to mark start of the generator
    BufferSize = None  # Total buffer size
    pSeqBuff_point = None  # The buffer for sequence generator(both sequences and RegInfo)
    SeqLen = None  # Generated sequence length till now
    pRegInfo_point = None  # Pointer to buffer where stores register info
    RegCount = None  # The count of register info available in buffer *pRegInfo.
    LastError = None  # The last error message.