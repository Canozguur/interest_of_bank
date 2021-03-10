import requests
from bs4 import BeautifulSoup
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.core.window import Window


class card_of_detail_faiz(MDCard):
    name_of_bank = StringProperty()
    yillik_faiz_orani = StringProperty()
    net_getiri = StringProperty()
    toplam_kazanc = StringProperty()


class MainScreen(MDScreen):
    pass


Window.size = (350, 625)
class MainApp(MDApp):
    def build(self):
        self.title = 'Faiz Bulucu'
        
    def detail_of_bank(self,bank_name):
        pass

    def find(self,tutar,day):
        self.root.ids['main_screen'].ids.daily.clear_widgets()

        url = "https://www.enuygun.com/mevduat/karsilastir/" + f"{tutar}-tl-{day}-gunde-ne-kadar-faiz-getirir/"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        veri = soup.find_all(class_="panel-body")
        print(len(veri))
        result = {}
        for i in range(1, len(veri) - 3):
            # x = veri[i].find(class_="col-xs-7 col-md-6")
            x = veri[i].find_all(class_="col-xs-4 text-center")
            banka_adı = veri[i].find(class_="col-xs-7 col-md-6")
            try:
                banka_adı = banka_adı.find('a').get("title")
            except Exception:
                print("hata alındı", i)
            print("-" * 40)
            print(banka_adı)
            information = {}
            for i in x:
                name = str(i.get_text()).split(":")
                isim = str(name[0]).replace("\n", "")
                tutar = name[1].replace("\n", "").replace("  ", "")

                print(f"{isim} : {tutar}")
                information.update({isim: tutar})
            result.update({banka_adı: information})
            print("-" * 40)

        #***********************************
        print(result)
        liste_sonucu = list(result.keys())
        for i in range(len(liste_sonucu)):
            name_of_bank = liste_sonucu[i]
            yeni_widget = card_of_detail_faiz(name_of_bank=name_of_bank, yillik_faiz_orani=result[name_of_bank]['Yıllık Faiz Oranı'], net_getiri=result[name_of_bank]['Net Getiri'], toplam_kazanc=result[name_of_bank]["Toplam Kazanç"],
                              )
            self.root.ids['main_screen'].ids.daily.add_widget(yeni_widget
                )

    def on_start(self):
        pass

MainApp().run()
