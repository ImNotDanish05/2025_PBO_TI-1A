class Handphone:
    def __init__(self, ID, Nama, Merek, Model, Tahun_Rilis, Harga):
        self.Nama = Nama
        self.Merek = Merek
        self.Model = Model
        self.Tahun_Rilis = Tahun_Rilis
        self.Harga = Harga
        self.Status = "Dijual"
    def pl():
        print(" ")
        print("=======================================================================")
        print(" ")
    def info(self):
        Handphone.pl()
        print(f'Handphone ini bernama "{self.Nama}", bermerek "{self.Merek}", dan model "{self.Model}". Handphone ini dirilis pada Tahun {self.Tahun_Rilis} dengan harga {self.Harga}$ saja!')
        print(f'Status: {self.Status}')
        Handphone.pl()

    def beli(self):
        Handphone.pl()
        Handphone.info(self)
        Kondisi = True
        while Kondisi:
            jawaban = input("Apakah anda yakin ingin membeli ini ? (y/n)")
            if jawaban == "y":
                Kondisi = False
                print(f"HP {self.Nama} telah dibeli oleh anda!")
                self.Status = "Dibeli"
            if jawaban == "n":
                Kondisi = False
                print(f"Its okay, you can buy it later hehe")
            else:
                print(f"Seng genah! jawaban anda tidak valid")
