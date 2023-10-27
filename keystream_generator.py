class KeystreamGenerator:
    LONGITUD_CLAVE = 80
    LONGITUD_SEMILLA = 64

    def __init__(self, clave, semilla):
        if len(clave) == KeystreamGenerator.LONGITUD_CLAVE:
            self.clave = list(clave)
        else:
            raise Exception("Longitud de la clave: {}. Longitud requerida: {}".format(len(clave), KeystreamGenerator.LONGITUD_CLAVE))

        if len(semilla) == KeystreamGenerator.LONGITUD_SEMILLA:
            self.semilla = list(semilla)
        else:
            raise Exception("Longitud de la semilla: {}. Longitud requerida: {}".format(len(semilla), KeystreamGenerator.LONGITUD_SEMILLA))

        self.lfsr = [0] * KeystreamGenerator.LONGITUD_CLAVE
        self.nfsr = [0] * KeystreamGenerator.LONGITUD_CLAVE

        self.inicializar()

    def inicializar(self):
        i = 0
        for i in range(len(self.clave)):
            self.nfsr[i] = self.clave[i]

        for i in range(len(self.semilla)):
            self.lfsr[i] = self.semilla[i]

        for i in range(len(self.lfsr), KeystreamGenerator.LONGITUD_CLAVE):
            self.lfsr[i] = 1

        for i in range(160):
            self.clock_inicial()

    def generar_keystream(self, bytes):
        keystream = [0] * (bytes * 8)

        for i in range(len(keystream)):
            keystream[i] = self.clock()

        return keystream

    def clock(self):
        output = self.output()
        self.shift_left_nfsr(self.feedback_nfsr())
        self.shift_left_lfsr(self.feedback_lfsr())
        return output

    def clock_inicial(self):
        output = self.output()
        self.shift_left_nfsr((self.feedback_nfsr() + output) % 2)
        self.shift_left_lfsr((self.feedback_lfsr() + output) % 2)

    def feedback_lfsr(self):
        return (self.lfsr[0] + self.lfsr[13] + self.lfsr[23] + self.lfsr[38] + self.lfsr[51] + self.lfsr[62]) % 2

    def shift_left_lfsr(self, bit):
        for i in range(len(self.lfsr) - 1):
            self.lfsr[i] = self.lfsr[i + 1]
        self.lfsr[-1] = bit

    def feedback_nfsr(self):
        return (self.lfsr[0] + self.nfsr[62] + self.nfsr[60] + self.nfsr[52] + self.nfsr[45] + self.nfsr[37] +
                self.nfsr[33] + self.nfsr[28] + self.nfsr[21] + self.nfsr[14] + self.nfsr[9] + self.nfsr[0] +
                self.nfsr[63] * self.nfsr[60] + self.nfsr[37] * self.nfsr[33] + self.nfsr[15] * self.nfsr[9] +
                self.nfsr[60] * self.nfsr[52] * self.nfsr[45] + self.nfsr[33] * self.nfsr[28] * self.nfsr[21] +
                self.nfsr[63] * self.nfsr[45] * self.nfsr[28] * self.nfsr[9] + self.nfsr[60] * self.nfsr[52] *
                self.nfsr[37] * self.nfsr[33] + self.nfsr[63] * self.nfsr[60] +
                self.nfsr[63] * self.nfsr[60] * self.nfsr[52] * self.nfsr[45] * self.nfsr[37] +
                self.nfsr[33] * self.nfsr[28] * self.nfsr[21] * self.nfsr[15] * self.nfsr[9] +
                self.nfsr[52] * self.nfsr[45] * self.nfsr[37] * self.nfsr[33] * self.nfsr[28] * self.nfsr[21]) % 2

    def shift_left_nfsr(self, bit):
        for i in range(len(self.nfsr) - 1):
            self.nfsr[i] = self.nfsr[i + 1]
        self.nfsr[-1] = bit

    def output(self):
        bi = (self.nfsr[1] + self.nfsr[2] + self.nfsr[4] + self.nfsr[10] + self.nfsr[31] + self.nfsr[43] + self.nfsr[56])
        h = self.filtro()
        return (bi + h) % 2

    def filtro(self):
        return (self.lfsr[25] + self.nfsr[63] + self.lfsr[3] * self.lfsr[64] + self.lfsr[46] * self.lfsr[64] +
                self.lfsr[64] * self.nfsr[63] + self.lfsr[3] * self.lfsr[25] * self.lfsr[46] +
                self.lfsr[3] * self.lfsr[46] * self.lfsr[64] + self.lfsr[3] * self.lfsr[46] * self.nfsr[63] +
                self.lfsr[25] * self.lfsr[46] * self.nfsr[63] + self.lfsr[46] * self.lfsr[64] * self.nfsr[63]) % 2