import requests
from bs4 import BeautifulSoup
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.core.window import Window


class card_of_detail_faiz(MDCard):
    name_of_bank = StringProperty()
    yillik_faiz_orani = StringProperty()
    net_getiri = StringProperty()
    toplam_kazanc = StringProperty()
    banka_link = StringProperty()


class MainScreen(MDScreen):
    pass


class DetailScreen(MDScreen):
    pass


Window.size = (350, 625)


class MainApp(MDApp):
    def build(self):
        self.title = 'Faiz Bulucu'



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
            banka_veri = veri[i].find(class_="col-xs-7 col-md-6")
            banka_link = ""
            banka_adı = ""
            try:
                banka_adı = banka_veri.find('a').get("title")
                banka_link = banka_veri.find(class_="result-details").get("href")

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
            result.update({banka_adı: [information,{"banka_link":banka_link}]})
            print("-" * 40)

        #***********************************
        print(result)
        liste_sonucu = list(result.keys())
        for i in range(len(liste_sonucu)):
            name_of_bank = liste_sonucu[i]
            yeni_widget = card_of_detail_faiz(name_of_bank=name_of_bank, yillik_faiz_orani=result[name_of_bank][0]['Yıllık Faiz Oranı'], net_getiri=result[name_of_bank][0]['Net Getiri'], toplam_kazanc=result[name_of_bank][0]["Toplam Kazanç"],
                                              banka_link=result[name_of_bank][1]['banka_link'],  )
            self.root.ids['main_screen'].ids.daily.add_widget(yeni_widget
                )

    def detail_of_bank(self,banka,link):
        layout = AnchorLayout()
        #second_layout = AnchorLayout()

        # -------------------------------
        for_row_data_list = []
        print(banka, link)
        url = "https://www.enuygun.com" + str(link)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        veri = soup.find('table', attrs={'class': 'table table-striped'})
        for i in veri.find_all("tr")[1:]:
            gün = i.find("th").get_text()
            tutarlar = i.find_all("td")
            tutar = tutarlar[0].get_text()
            faiz_oranı = tutarlar[1].get_text()
            print(gün)
            print(tutar)
            print(faiz_oranı)
            for_row_data_list.append([gün,tutar,faiz_oranı])

        # -------------------------------
        second_veri = soup.find('table', attrs={'class': 'table'})
        data_sol_col = []
        x = 0
        for i in second_veri.find_all("tr"):
            if x == 0:
                x += 1
                row_1 = i.find("th").get_text()
                row_2 = i.find("img").get("alt")
            else:
                row_1 = i.find("th").get_text()
                row_2 = i.find("td").get_text()
            data_sol_col.append([row_1, row_2])
        # ---------------------------------
        details_of_bank_name = data_sol_col[0]
        data_sol_col.remove(data_sol_col[0])

        data_tables = MDDataTable(
            size_hint=(0.9, 1),  # 0.9 , 0.6
            use_pagination=True,
            column_data=[
                ("Gün", dp(20)),
                ("Tutar", dp(30)),
                ("Faiz oranı", dp(50)),

            ],
            row_data=for_row_data_list)
        layout.add_widget(data_tables)
        self.root.ids['detail_screen'].ids.data.add_widget(layout)
        self.root.ids['detail_screen'].ids.bank.text = f"BANK OF {str(details_of_bank_name[1]).upper()}"
        self.root.ids['detail_screen'].ids.bank.valign ="center"

        """
        second_data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("Gün", dp(20)),
                ("Tutar", dp(30)),],

            row_data=data_sol_col)
        second_layout.add_widget(second_data_tables)
        self.root.ids['detail_screen'].ids.data_2.add_widget(second_layout)
        """

        self.root.ids['screen_manager'].current = "detail_screen"

        Window.size = (475, 625)

    def on_row_press(self, *args):
        pass

    def on_check_press(self, *args):
        '''Called when the check box in the table row is checked.'''

        pass

    def back(self):
        self.root.ids['screen_manager'].current = "main_screen"
        self.root.ids['detail_screen'].ids.data.clear_widgets()
        Window.size = (350, 625)


MainApp().run()
