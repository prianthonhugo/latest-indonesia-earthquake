import requests
from bs4 import BeautifulSoup
"""
Method = fungsi
Field / Attribute = variabel
"""

class GempaTerkini:
    def __init__(self, url):
        self.description = 'To get the latest earthquake in Indonesia from BMKG.go.id'
        self.result = None
        self.url = url


    def ekstraksi_data(self):
        """
        Tanggal: 17 September 2024
        Waktu: 08:15:21 WIB
        Magnitudo: 3.0
        Kedalaman: 8 km
        Koordinat: LS=7.27 BT=109.66
        Lokasi Gempa: Pusat gempa berada di darat 16 Km BaratLaut BANJARNEGARA
        Dirasakan: Dirasakan (Skala MMI): II Banjarnegara
        :return:
        """
        try:
            content = requests.get(self.url)
        except Exception:
            return None

        if content.status_code == 200:
            soup = BeautifulSoup(content.text, 'html.parser')

            tangwak = soup.find('span', {'class': 'waktu'})
            tanggal = tangwak.text.split(', ')[0]
            waktu = tangwak.text.split(', ')[1]

            dalamdiv = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            dalamdiv = dalamdiv.findChildren('li')

            i = 0
            magnitudo = None
            kedalaman = None
            ls = None
            bt = None
            lokasi = None
            dirasakan = None

            for dal in dalamdiv:
                # print(i, dal)
                if i == 1:
                    magnitudo = dal.text
                elif i == 2:
                    kedalaman = dal.text
                elif i == 3:
                    koordinat = dal.text.split(' - ')
                    ls = koordinat[0]
                    bt = koordinat[1]
                elif i == 4:
                    lokasi = dal.text
                elif i == 5:
                    dirasakan = dal.text
                i = i + 1

            hasil = dict()
            hasil['tanggal'] = tanggal #'17 September 2024'
            hasil['waktu'] = waktu #'08:15:21 WIB'
            hasil['magnitudo'] = magnitudo #3.0
            hasil['kedalaman'] = kedalaman #'8 km'
            hasil['koordinat'] = {'ls': ls, 'bt': bt} # {'ls': 7.27, 'bt': 109.66}
            hasil['lokasi'] = lokasi # 'Pusat gempa berada di darat 16 Km BaratLaut BANJARNEGARA'
            hasil['dirasakan'] = dirasakan # 'Dirasakan (Skala MMI): II Banjarnegara'
            self.result = hasil
        else:
            return None


    def tampilkan_data(self):
        if self.result is None:
            print("Tidak bisa menemukan data gempa terkini")
            return
        print('Gempa terakhir berdasarkan BMKG')
        print(f"Tanggal: {self.result['tanggal']}")
        print(f"Waktu: {self.result['waktu']}")
        print(f"Magnitudo: {self.result['magnitudo']}")
        print(f"Kedalaman: {self.result['kedalaman']}")
        print(f"Koordinat: LS={self.result['koordinat']['ls']}, BT={self.result['koordinat']['bt']}")
        print(f"Lokasi: {self.result['lokasi']}")
        print(f"Dirasakan: {self.result['dirasakan']}")

    def run(self):
        self.ekstraksi_data()
        self.tampilkan_data()

if __name__ == '__main__':
    gempa_di_indonesia = GempaTerkini('https://bmkg.go.id/')
    print('Deskripsi class GempaTerkini', gempa_di_indonesia.description)
    gempa_di_indonesia.run()

    gempa_di_dunia = GempaTerkini('https://bmkg.go.id/')
    print('Deskripsi class GempaTerkini', gempa_di_dunia.description)
    gempa_di_dunia.run()
    # gempa_di_indonesia.ekstraksi_data()
    # gempa_di_indonesia.tampilkan_data()
