#import os
#from android.permissions import Permission, request_permissions, check_permission
#from android.storage import app_storage_path, primary_external_storage_path, secondary_external_storage_path
#perms = [Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE]
#if  check_permissions(perms)!= True:
#    request_permissions(perms)    # get android permissions
#    exit()
################### ^^^^^^^^^^^^^ DA TESTARE ED AGGIUNGERE ^^^^^^^^^^^^^ ##################
###             AGGIUNTA LIBRERIE
#                      \/

from kivymd.app import MDApp
from kivy.lang import Builder
#from  kivy.properties import StringProperty
import time
from os import mkdir
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList,OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from KV import KV
from bs4 import BeautifulSoup
###############
# DECOMMENTARE PRIMA DI CREARE L'APP
#   Altrimenti Android non troverà la path

#SAF = '/storage/emulated/0/StraordinApp/Straordinari.txt'
#CFG = '/storage/emulated/0/StraordinApp/Config.xml'

# DECOMMENTARE PER I TEST
#   Con Windows non è possibile utilizzare le variabili sopra

SAF = 'Straordinari.txt'
CFG = 'Config.xml'
#                                           !!! SISTEMARE LISTA NELLA PAGINA RICERCA !!!
############### DEFINIZIONE DELLE VARIABILI

l = []
_file_value_list = [] # lista per il contenuto del file
temp_date_src_l = []  # creo una seconda lista temporanea
onelist = [] # lista items
days = [] # lista giorni mese corrente
ore = [] # lista ore
m = time.strftime('%m')
d = time.strftime('%d')
_data= f'{d}/{m}'
Y = time.strftime('%Y')
ico = 'SA+1.png'
temp_ora = 0.0
tot = 0.0
temp_data = ''
ver= '1.1.0' # MODIFICARE SOLO QUI,
##
################ CONTROLLO SE ESISTE IL FILE NELLA CARTELLA
####### ALTRIMENTI VERRA' CREATO     -------------- SE ESISTE GIA' LA CARTELLA, PASSA ALLA CREAZIONE SOLO DEI FILE
##
try:
    f = open(CFG,'r')
    f.close()
except FileNotFoundError:
    try:
        mkdir('/storage/emulated/0/StraordinApp/')
    except FileExistsError:
        pass
############## SE NON C'E' UN FILE CFG ALLORA NE CREO UNO (FACCIO PRIMA IN QUESTO MODO CHE CON LA ELEMENTREE)
    with open(CFG, mode='w') as C:
        C.write(f'''
<Config>
    <theme n="" theme="Light">Tema</theme>
    <ver n="" ver="{ver}">Ver</ver> 
</Config>
        ''')
######## RIAPRO IL FILE PER PRENDERE I DATI DI CONFIGURAZIONE
##
##          AL MOMENTO SOLO TEMA E VERSIONE
##
##############################################################
with open(CFG,mode='r') as F:
    thm = F.read()
    data = BeautifulSoup(thm, 'xml')
    theme = data.find('theme')
    version = data.find('ver')
    ver_ = version.get('ver')
    cf = theme.get('theme')
_theme = cf
##      COMPLETARE LA MODIFICA AUTOMATICA DEL TEMA
if cf == 'Dark':
    _theme = 'Dark'
    if _data == '31/10':
        _palette = 'Orange'
    else:
        _palette = 'Gray'
    _text = 'white'
else:
    _theme = 'Light'
    if _data == '31/10':
        _palette = 'Red'
    else:
        _palette = 'Blue'
    _text = 'black'
############### CREO UNA FUNZIONE PER IL CALCOLO DEL TOTALE DELLE ORE STRAORDINARIE
def tot_write(self,m, id, **Kwargs):
    '''
    Restituisce il totale delle ore nel mese corrente
    :param self:
    :param m:
    :return:
    '''
    tot = 0.0
    F = open(SAF, 'r') # Apro il file
    temp_list = F.readlines() # Inerisco il tutto in una lista
    F.close() # Chiudo il file
    for i in temp_list:
        if (i[3:5] == m) and (i[6:]!=''): # se trova il mese corrente
            temp_ora = i[7:] #Acquisisce il numero dell'ora
            tot = tot + float(temp_ora) # Sommando al totale
    self.root.ids.tot.text_color = _text
    self.root.ids.src_tot.text_color = _text
    if 18.0 < tot <= 22.0:
        self.root.ids.tot.text_color='#ffac00'
        self.root.ids.src_tot.text_color = '#ffac00'
    elif tot> 22.0:
        self.root.ids.tot.text_color= 'red'
        self.root.ids.src_tot.text_color= 'red'
    if '.0' in str(tot):
        tot = (str(int(float(tot))))
    if id == 1:
        self.root.ids.tot.text = 'Tot.: ' + str(tot)
    elif id == 2:
        self.root.ids.src_tot.text = 'Tot.: ' + str(tot)


state = True   # ------------- Booleana utilizzata per l'icona ricerca/indietro
class modifica(BoxLayout):
    print('Creazione classe <modifica>')
class add(BoxLayout):
    print('Creazione classe <add>')

################################## CREAZIONE DELLA CLASSE PER L'APP ##################################################

class Main(MDApp):
    print (f'Creazione classe {MDApp()}\nl={l}\n_file_value_list={_file_value_list}\ntemp_date_src_l={temp_date_src_l}\ntot={tot}')
            ## PROVO AD APRIRE IL FILE .TXT
    try:
        with open(SAF, mode='r') as F:
            l.append(F.readlines())
    except FileNotFoundError: # Se non lo trova ne crea uno iniziando dall'anno corrente
        with open(SAF, mode='a') as F:
            F.write(f'{Y}\n')
                        ## DA AGGIUNGERE: Possibilità di ricominciare da un anno nuovo
                        #                 (altrimenti ci sarà una somma con le ore dei mesi addietro)
    def build(self):
        '''
        Costruzione dell'App
        :return:
        '''
        print('Richiamo sottoclasse <build>')
        self.icon = ico
        self.title = 'StraordinApp'
        self.theme_cls.theme_style = _theme
        self.theme_cls.primary_palette = _palette
        #self.theme_cls.primary_hue = '700'
        return Builder.load_string(KV)

    def dial(self, switch):
        print('Richiamo sottoclasse <dial>')
        '''
        Funzione a parte per la gestione delle dialogs
        :return:
        '''
        if switch == 1:
            self.dialog = MDDialog(
				title=f'VER. {ver} (Beta)',
				type='simple',
				text='''
- Aggiunta la possibilità di aggiungere giorni ed ore al mese corrente
- Risolto qualche bug minore
''' )
            self.dialog.open()
        elif switch == 2:
            self.dialog = MDDialog(
				title=f'StraordinApp: Info',
				type='simple',
				text=f'''
StraordinApp Versione {ver}
Scritto in Python 3.10.6
    Librerie: 
     - Kivy 2.1.0
     - Kivymd 1.0.2
     - BeautifulSoup4 4.11.1
     
Contatto: 
    andrewdm91@gmail.com
    
Github:
    https://github.com
            
                !!! Attenzione !!!
Se si effettuano operazioni di eliminazione,
modifica o aggiunta, riavviare l'app per 
evitare errori.
Il bug verrà risolto presto
                    '''
                 ) ## TODO Link alla e-mail
            self.dialog.open()
        elif switch == 3:
            self.dialog = MDDialog(
                title=f'Logs',
                type='simple',
                ##### TODO:  CREARE LOG SU FILE !!!!!!!
                text=f'''
1.1.0
- Aggiunta la possibilità di aggiungere giorni ed ore al mese corrente
- Risolto qualche bug minore

0.13.2
- Risolti bug relativi allo sdoppiamento nel file e all visualizzazione nell'app
- Tolta la possibilità di modificare le ore nei mesi precedenti

0.13
- Possibilità di modificare l'orario di una determinata data

0.12.2
- BugFix vari (Lavorazione sulle liste)

0.12
- BugFix vari (Tema + Posizioni + Funzionamento)
- Possibilità di eliminare un elemento dall'elenco
  (La modifica non è ancora implementata) 
    
0.11.3
- Risolto bug colore ore totali all'avvio dell'app
con il tema Light 
- Cambio del colore per i temi + Cambio automatico festività
- Risolto bug mancato inserimento delle ore 
- Risolto bug sui mesi privi di straordinari nella pagina di ricerca
                                '''
            )
            self.dialog.open()

    def _modifica(self,x, index, f_v, i, local, *args):
        '''
        Richiamo la funzione di modifica collegata ad una classe esterna nel file KV
        :param x:
        :param index:
        :param f_v:
        :param args:
        :return:
        '''
        ## print(f'Richiamo <_modifica({index}, {f_v}, {i} -- {len(_file_value_list)})>')
        l = [] # reset lista principale
        _file_value_list = [] # reset lista temporanea
        with open(SAF, mode= 'r') as F: # riapro il file per evitare che ci siano doppioni
            l.append(F.readlines())
        for _ in l:
            for j in _:  # Riscrivo la lista
                _file_value_list.append(j)
        value = self.mod_dialog.content_cls.ids.new_value.text
        _file_value_list[index]=f'{f_v[:5]} +{value}\n'
        #print(_file_value_list2)
        #self.root.ids._oli.remove_widget(i)
        if f_v[:5] != _data:
            i.theme_text_color = 'Custom'
            i.text_color = 'magenta'
            i.text = f'>> {f_v[:5]} +{value}\n'
            # self.root.ids._oli.add_widget(OneLineListItem(text=f'{f_v[:5]} +{value}\n', theme_text_color= 'Custom',text_color= 'orange',
            #                         on_release=lambda x=enumerate(str(index)), num = index: self.menu_(x,num,1)))
            with open(SAF, mode='w') as F:
                F.writelines(_file_value_list)
        self.mod_dialog.dismiss()
        self.menu.dismiss()
        tot_write(self,f_v[3:5],1)

    def menu_(self, i,index,local):
        ## print('Richiamo sottoclasse <menu_>')
        f_v = _file_value_list[index]
        print(f'{index}: {f_v} -- {i}')
        def _remove_():
            '''
            Prende l'index dalla lista creata nello start, per fare una 'pop' nella lista delle ore
            riscrivendo il file aggiornato.
            :return:
            '''
           ## print('Richiamo sottoclasse <_remove_>')
            self.conferma.dismiss() # chiudo il dialog di conferma
            ####### LA LOCAL SERVE AD ASSICURARE L'ELIMINAZIONE DEL WIDGET GIUSTO
            if local == 1:
                print(i)
                self.root.ids._oli.remove_widget(i)
            elif local == 2:
                self.root.ids._src_date.remove_widget(i)
            _file_value_list[index]=f'{f_v[:5]}\n' # Rimuovo il valore dalla lista
            self.menu.dismiss() # Chiudo il menu
            with open(SAF, mode='w') as F:  # riscrivo il file con la lista aggiornata
                F.writelines(_file_value_list)
            tot_write(self, f_v[3:5],local) # riscrivo il totale

                              ##### CREO LA LISTA DEL MENU ####
        menu_items = [
            {
                'viewclass': 'OneLineListItem',
                'theme_text_color': 'Custom',
                'text_color': _text,
                'text': 'Modifica',
                'on_release': lambda: self.mod_dialog.open() if (local==1) else self.not_implemented(3)
            },
            {
                'viewclass': 'OneLineListItem',
                'theme_text_color': 'Custom',
                'text_color': '#f00000',
                'text': 'Rimuovi',
                'on_release': lambda: self.conferma.open()
            }
        ]
        self.menu = MDDropdownMenu(
            caller=i,
            items=menu_items,
            width_mult=3,
        )
        self.menu.open()
            ### CREO UNA DIALOG DI CONFERMA
        self.conferma = MDDialog(
            title='Confermi l\'eliminazione?',
            buttons=[
                MDFlatButton(
                    text='SI',
                    on_release=lambda x: _remove_()
                ),
                MDFlatButton(
                    text='NO',
                    on_release = lambda x: self.conferma.dismiss(lambda x: self.menu.dismiss())
                    #on_release=lambda x: self.menu.dismiss()
                ), ])
        self.mod_dialog = MDDialog(
            title=f'Modifica {f_v[:5]}',
            type='custom',
            content_cls=modifica(),
            buttons=[
                MDFlatButton(
                    text='OK',
                    on_release=lambda x, ind=int(index), fv=f_v, i=i, local=local: self._modifica(x, ind, fv, i,
                                                                                                  local)
                ),
                MDFlatButton(
                    text='Cancella',
                    on_release=lambda x: self.mod_dialog.dismiss()
                )
            ]
        )
    def on_stop(self):
        with open(CFG, mode='w') as F: # Scrivo il file di configurazione con le impostazioni aggiornate
            F.write(f'''
            <Config>
                <theme n="" theme="{cf}">Tema</theme>
                <ver n="" ver="{ver}">Ver</ver> 
            </Config>
                    ''')


    def on_start(self):
        '''
        Funzione che parte all'avvio dell'app
        :return:
        '''
        print('Richiamo sottoclasse <on_start>')
        global temp_data, temp_ora, tot
        if ver != ver_: # Dialog che appare quando con l'aggiornamento della versione
        # Scrivo sul file delle configurazioni la nuova versione
            with open(CFG, mode='w') as C:  # Così non riappare le volte successive
                C.write(f'''            
            <Config>
                <theme n="" theme="{cf}">Tema</theme>
                <ver n="" ver="{ver}">Ver</ver> 
            </Config>
                    ''')
            self.dial(1)
        else:
            pass
        self.root.ids.IN_B.text_color = _text                     ####
        self.root.ids.MDRFIB.text = _theme                          ##
        self.root.ids.src.text_color = _text                        ##
        self.root.ids.MDRFIB.text_color = _text                     ## COLORAZIONI IN BASE AL TEMA
        self.root.ids.MDND_.color = _text                           ##
        self.root.ids.MDND.color = _text                          ####
        self.root.ids.KV_ver.text = f'versione: {ver}'
        self.root.ids.data.title = f'StraordinApp - {_data}'
        _index_list = [] # lista per contenere i 'num'
        num = 0 # contatore per l'index
        tempint = 0 # contatore per l'enumerazione
        for i in l:
            for j in i:                     # Cerco gli elementi in lista in base al mese corrente
                _file_value_list.append(j)
                _index_list.append(num)
                #print(f'{num}: {_file_value_list[num]}')
                if (j[3:5] == m)and (j[6:]!=''):
                   # _name.append(j)             # temp_data da usare in 'Writing'
                    temp_data = j[:5]
                    temp_ora = j[7:]
                   #### CREO LA RIGA DELLA LISTA ISTANTANEAMENTE ACQUISENDO SIA L'ENUMERAZIONE DELL'OGGETTO,
                   #### SIA L'INDEX DELLA LISTA PRESA DAL FILE
                    onelist.append(str(tempint))
                    days.append(int(j[:2]))
                    self.root.ids._oli.add_widget(OneLineListItem( text=j, on_release=lambda
                        x=enumerate(j), num = num: self.menu_(x,num,1)))  # , on_press= lambda x:self.menu_()
                    tempint += 1
                    # tot = tot + float(temp_ora)
                num += 1
        tot_write(self, m, 1)

    def _add_(self):
        def adding():
            temp_list = []
            gg = self.add_dialog.content_cls.ids.day.text
            ora = self.add_dialog.content_cls.ids.ore.text
            if float(int(ora)) == 0.0:
                self.add_dialog.content_cls.ids.ore.hint_text = 'Non valido!!'
            else:
                self.add_dialog.content_cls.ids.day.text = ''
                self.add_dialog.content_cls.ids.ore.text = ''
                self.add_dialog.content_cls.ids.ore.hint_text = 'Inserisci il numero di ore'
                if int(gg) < 10:
                    gg = '0'+gg
                if int(gg) not in days:
                    self.add_dialog.content_cls.ids.add_l.text = f'{gg}/{m}  +{ora}'
                    _ = 0
                    for i in _file_value_list:
                        if i[3:5] == m:
                            if int(gg)<int(i[:2]):
                                _file_value_list.insert(_,f'{gg}/{m} +{ora}\n')
                                self.root.ids._oli_.add_widget(
                                    OneLineListItem(text=f'{gg}/{m} +{ora}', theme_text_color='Custom',
                                                    text_color='#0033cc', on_release=lambda x: self.not_implemented(2)))
                                break
                            elif int(gg)>=int(d):
                                self.add_dialog.dismiss()
                                Snackbar(text= 'Inserire una data precedente a quella odierna').open()
                        _ +=1
                    with open(SAF, mode='w') as F:
                        F.writelines(_file_value_list)
                else:
                    self.add_dialog.dismiss()
                    Snackbar(text='Modificare dall\'apposito menù' ).open()
            tot_write(self,m,1)

        self.add_dialog = MDDialog(
            title= 'Aggiunta ore',
            type= 'custom',
            content_cls = add(),
            buttons = [
                MDFlatButton(
                    text='Aggiungi',
                    on_release= lambda x: adding() if (self.root.ids.S_M.current == 'M') else self.not_implemented(3)
                ),
                MDFlatButton(
                    text= 'Chiudi',
                    on_release= lambda x: self.add_dialog.dismiss()
                )

            ]
        )
        self.add_dialog.open()

    def writing(self):
        '''
        Funzione utilizzata per scrivere sul file .TXT l'ora aggiunta tramite il form (TXT)
        Viene chiamata alla pressione del tasto 'INSERISCI' (IN_B)
        :return:
        '''
        ## print(f'Richiamo sottoclasse <writing>')
        global temp_data, temp_ora, tot
        _temp_txt = str(self.root.ids.TXT.text)
        self.root.ids.TXT.text = ''
        if _temp_txt == '':
            return
        else:
            pass
        ## QUESTA PARTE SERVE NEL CASO VENGANO AGGIUNTE PIU' ORE NELLO STESSO GIORNO
        if _data == temp_data:              # Se il giorno e mese coincidono l'ora aggiunta va a sommarsi con quelle
            _temp_txt = str(float(_temp_txt) + float(temp_ora))     # precedenti, senza creare un'alta linea nel file
            tot = tot + float(_temp_txt)
            # print(tot)
            if '.0' in _temp_txt: # Essendo l'input un float, se non ha altre cifre dopo la virgola, viene trasformato in intero
                _temp_txt = (str(int(float(_temp_txt)))) #  in modo da non avere, per esempio, 01/01 +1.0
            F = open(SAF, 'r')
            lines = F.readlines()[:-1] # Leggo la lista dall'ultimo item
            lines.append(f'{d}/{m} +{_temp_txt}\n') # Appendo il nuovo inserimento nell'ultima parte della lista
            F.close()
            F = open(SAF, 'w') ## Riscrivo il file con l'orario aggiornato
            F.writelines(lines)
            F.close()
        else: # Se il giorno è diverso, aggiungo solo il nuovo orario
            with open(SAF, mode='a') as F:
                F.write(f'{d}/{m} +{_temp_txt}\n')
        self.root.ids._ok.text = f'+{_temp_txt}'
                ## AGGIUNGO IL NUOVO ITEM ALLA LISTA ##
        self.root.ids._oli.add_widget(OneLineListItem(text=f'\n{d}/{m} +{_temp_txt}', theme_text_color= 'Custom',
                                      text_color='green', on_release= lambda x: self.not_implemented(2)))
        temp_data = _data
        temp_ora = _temp_txt
        _file_value_list.append(f'{d}/{m} +{_temp_txt}\n')
        ## print(len(_file_value_list))
        tot_write(self, m,1) ## Richiamo la funzione di scrittura del totale mensile

    def theme_changer(self): ### TODO Creare una pagina di scelta del tema
        '''
        Cambia automaticamente il tema appena viene selezionato, senza dover riavviare l'applicazione
        Colori per le palette: ‘Red’, ‘Pink’, ‘Purple’, ‘DeepPurple’, ‘Indigo’, ‘Blue’, ‘LightBlue’,
        ‘Cyan’, ‘Teal’, ‘Green’, ‘LightGreen’, ‘Lime’, ‘Yellow’, ‘Amber’, ‘Orange’, ‘DeepOrange’,
        ‘Brown’, ‘Gray’, ‘BlueGray’.

        :return:
        '''
        ## print(f'Richiamo sottoclasse <theme_changer>')
        global cf
        if cf == 'Dark':
            _theme = 'Light'
            if _data == '31/10':
                _palette = 'Red'
            else:
                _palette = 'Blue'
            _text = 'black'
            cf = 'Light'
        #     #Snackbar(text='Tema Light').open()
        elif cf == 'Light':
            _theme = 'Dark'
            if _data == '31/10':
                _palette = 'Orange'
            else:
                _palette = 'Gray'
            _text = 'white'
            cf = 'Dark'
            # Snackbar(text='Tema Dark').open()
        self.theme_cls.theme_style = _theme
        self.theme_cls.primary_palette = _palette
        self.root.ids.IN_B.text_color = _text
        self.root.ids.src_tot.text_color = _text
        self.root.ids.tot.text_color = _text
        self.root.ids.src.text_color = _text
        self.root.ids.info.text_color = _text
        self.root.ids.MDND_.color = _text
        self.root.ids.MDND.color = _text
        self.root.ids.MDRFIB.text_color = _text
        self.root.ids.MDRFIB.text = _theme
        #self.root.ids.nav_d.set_state(new_state='close', animation=True)

        tot_write(self, m,1)

    def Search(self,instance,value,range):
        ## print('Richiamo sottoclasse <Search>')
        # creo una lista per i mesi in chiaro
        month_list=[
            'Gennaio',
            'Febbraio',
            'Marzo',
            'Aprile',
            'Maggio',
            'Giugno',
            'Luglio',
            'Agosto',
            'Settembre',
            'Ottobre',
            'Novembre',
            'Dicembre'
        ]
        date_get = value # prendo il valore intero della data
        _date_get= str(date_get) # lo trasformo in stringa
        list_date =_date_get.split('-') # riordino in una lista
        dd= list_date[2] # ne ricavo il secondo
        mm = list_date[1] # ed il primo index
        temp_date_src = dd+'/'+mm # sistemo la data in un modo standard
        _index_list = []  # lista per contenere i 'num'
        num = 0  # contatore per l'index
        for i in l:
            for j in i:  # Cerco gli elementi in lista in base al mese corrente
                temp_date_src_l.append(j)
                _index_list.append(num)
                if j[:5]==temp_date_src:
                    self.root.ids.one_src_date.text= str(j)
                    self.root.ids.one_src_date.text_color= '#005f00'
                    return
                elif j[3:5] == mm:
                    try:
                        self.root.ids._src_date.add_widget(OneLineListItem(text=j,
                                on_press=lambda x=enumerate(j), num = num: self.menu_(x,num,2)))
                    except IndexError:
                        self.root.ids.one_src_date.text = f'Nessun Straordinario \nnel mese  di {month_list[int(mm) - 1]}'
                    tot_write(self, mm, 2)
                else:
                    self.root.ids.one_src_date.font_style = 'H6'
                    self.root.ids.one_src_date.text= f'Nessun Straordinario \nin data {dd}/{mm}'
                    self.root.ids.one_src_date.text_color= '#5f0000'
                num +=1

    def on_cancel(self,instance,value): # Se viene cancellata l'operazione di ricerca (è necessario)
        self.root.ids.one_src_date.text = ''
        ##print(f'closed: {instance} - on: {value}')

    def return_(self):
        '''
        Rimette l'icona allo stato originale, tornando alla schermata iniziale con tutte le sue variabili
        :return:
        '''
        global state
        self.root.ids.src.icon = 'magnify'
        self.root.ids.src.text = 'Cerca'
        self.root.ids.nav_d.closing_time = 0.5
        self.root.ids.nav_d.set_state(new_state='close')
        self.root.ids.S_M.current = 'M'
        state = True # Riporto la booleana allo stato iniziale

    def date_dialog(self):# Istanza per aprire il dialog relativo alla ricerca per data
        date_dialog = MDDatePicker(day=int(d), month=int(m), year=int(Y))
        date_dialog.bind(on_save=self.Search, on_cancel=self.on_cancel)
        date_dialog.open()

    def Nav_Change(self):
        '''
        Porta alla pagina di ricerca cambiando l'icona (da 'magnify' a 'arrow-u-left-top')
        :return:
        '''
        global state
        #self.root.ids.data.left_action_items=[['arrow-u-left-top', lambda x: self.return_()]]
        self.root.ids.src.icon = 'arrow-u-left-top'
        self.root.ids.src.text= 'Indietro'
        self.root.ids.S_M.current = 'S'
        self.root.ids.nav_d.closing_time = 0.5
        self.root.ids.nav_d.set_state(new_state='close')
        state = False # per il Pre_Nav_Ghange

    def Pre_Nav_Change(self):
        '''
        Funzione di switch tra i comandi per il cambio della pagina:
        Se lo stato è impostato su False, verrà chiamata la funzione per il ritorno nella mainpage.
        Se lo stato è impostato su True (di default), verrà chiamata la funzione per entrare nella pagina di ricerca
        :return:
        '''
        if state== False:
            self.return_()
        else:
            self.Nav_Change()

    def not_implemented(self, switch):
        if switch == 1:
            Snackbar(text='Funzione non ancora implementata').open()
        elif switch == 2:
            Snackbar(text= 'Rimozione o modifica abilitate dopo il riavvio').open()
        elif switch == 3:
            Snackbar(text= 'Non è possibile modificare orari nei mesi precedenti').open()

        #self.root.ids.nav_d.set_state(new_state='close')
Main().run()