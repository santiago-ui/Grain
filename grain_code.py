import keystream_generator
from keystream_generator import KeystreamGenerator
class Grain:
    def __init__(self, clave, semilla, textoPlano):
        self.keystreamGenerator = KeystreamGenerator(self.to_short_array(clave), self.to_short_array(semilla))
        self.textoPlano = textoPlano
        self.keystream = self.to_byte_array(self.keystreamGenerator.generar_keystream(len(self.textoPlano) - 54))
        self.longitud = len(self.textoPlano)
        if self.longitud - 54 != len(self.keystream):
            raise Exception

    def xor(self):
        xored = bytearray(self.longitud)
        header = self.get_header(self.textoPlano)
        body = self.get_body(self.textoPlano)
        
        for i in range(54):
            xored[i] = header[i]
        
        for i in range(self.longitud - 54):
            xored[i + 54] = (body[i] ^ self.keystream[i])
        
        return bytes(xored)

    def to_byte_array(self, s):
        b = bytearray(len(s) // 8)
        for i in range(len(s) // 8):
            b[i] = (s[i * 8] * 128 + s[i * 8 + 1] * 64 + s[i * 8 + 2] * 32 + s[i * 8 + 3] * 16
                    + s[i * 8 + 4] * 8 + s[i * 8 + 5] * 4 + s[i * 8 + 6] * 2 + s[i * 8 + 7])
        return b

    def to_short_array(self, b):
        s = [0] * (len(b) * 8)
        for i in range(len(b)):
            aux = b[i]
            for j in range(7, -1, -1):
                s[i * 8 + j] = aux % 2
                aux = aux // 2
        return s

    def get_header(self, textoPlano):
        return textoPlano[:54]

    def get_body(self, textoPlano):
        return textoPlano[54:]
