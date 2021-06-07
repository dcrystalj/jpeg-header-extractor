from struct import unpack
import argparse


class ImagePart:
    START_OF_IMAGE = 0xFFD8
    APPLICATION_DEFAULT_HEADER = 0xFFE0
    QUANTIZATION_TABLE = 0xFFDB
    START_OF_FRAME = 0xFFC0
    DEFINE_HUFFMAN_TABLE = 0xFFC4
    START_OF_SCAN = 0xFFDA
    END_OF_IMAGE = 0xFFD9


class JPEG:
    def __init__(self):
        self.args = self._validate_args()
        self._read()

    def _validate_args(self):
        parser = argparse.ArgumentParser(description='Remove content of JPEG image file and keep header only.')
        parser.add_argument('file_in', help='input file')
        parser.add_argument('file_out', help='output file')
        args = parser.parse_args()
        return args

    def clean_content(self):
        data = self.img_data
        i = 0
        while True:
            (marker,) = unpack(">H", data[i : i + 2])
            if marker == ImagePart.START_OF_IMAGE:
                i += 2
            elif marker == ImagePart.END_OF_IMAGE:
                return
            elif marker == ImagePart.START_OF_SCAN:
                self._write(data[:i] + data[-2:])
                return
            else:
                (lenchunk,) = unpack(">H", data[i + 2 : i + 4])
                i += 2 + lenchunk

    def _read(self):
        with open(self.args.file_in, 'rb') as f:
            self.img_data = f.read()

    def _write(self, data):
        with open(self.args.file_out, 'wb') as f:
            f.write(bytearray(data))


if __name__ == '__main__':
    JPEG().clean_content()
