############################## STRAORDINAPP #########################################
## App per la gestione dei straordinari dove è possibile:                          ##
## - Aggiungere le ore                                                             ##
## - Aggiungere un giorno precedente (in caso di dimenticanza)                     ##
## - Modificare le ore di un giorno già inserito (Non dei mesi precedenti)         ##
## - Eliminare un determinato giorno (anche nei mesi passati)                      ##
## - Visualizzare le ore straordinarie nei mesi precedenti                         ##
## - Esportare un determinato mese come file di testo                              ##
## - Modificare il tema dell'app                                                   ##
##                                                                                 ##
##  andrewdm91@gmail.com                                                           ##
##  https://github.com/noxsilente/StraordinApp                                     ##
#####################################################################################
###                                 AGGIUNTA LIBRERIE                             ###
from kivymd.app import MDApp
from kivy.lang import Builder
import time
import shutil
import sqlite3
from os import mkdir
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.snackbar import Snackbar
from KV import KV, dial
from bs4 import BeautifulSoup

# DECOMMENTARE PRIMA DI CREARE L'APP
#   Altrimenti Android non troverà la path

#SAF = '/storage/emulated/0/StraordinApp/Straordinari.db'
#CFG = '/storage/emulated/0/StraordinApp/Config.xml'

# DECOMMENTARE PER I TEST
#   Con windows utilizzare le variabili qui sotto

SAF = 'Straordinari.db'
CFG = 'Config.xml'

##                                   DEFINISCO LE VARIABILI
month_list = [
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
        ] # lista dei mesi per effettuare la ricerca / esportazione
l = [] # lista per appendere i valori dei file di testo -- DA TENERE SOLO PER I TEST O PER CHI HA UTILIZZATO VERSIONI PRECEDENTI
_file_value_list = [] # lista per il contenuto del file -- DA TENERE SOLO PER I TEST O PER CHI HA UTILIZZATO VERSIONI PRECEDENTI
m = time.strftime('%m') # MESE ATTUALE
d = time.strftime('%d') # GIORNO ATTUALE
_data= f'{d}/{m}' # FORMATO DATA STANDARDIZZATO
Y = time.strftime('%Y') # ANNO ATTUALE
ico = 'SA+1.png' # ICONA PER L'APP
temp_ora = 0.0 # FLOAT TEMPORANEA PER L'ACQUISIZIONE DELL'ORA
tot = 0.0 # FLOAT PER IL CALCOLO DELLE ORE TOTALI
ver= '1.4.1' # MODIFICARE SOLO QUI, VERSIONE DELL'APP
##   CONTROLLO SE ESISTE IL FILE NELLA CARTELLA, ALTRIMENTI VERRA' CREATO
##   SE ESISTE GIA' LA CARTELLA, PASSA ALLA CREAZIONE ESCLUSIVA DEI FILE
try:
    f = open(CFG,'r')
    f.close()
except FileNotFoundError:                           ## DA COMMENTARE SOLO PER I TEST
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
    <y n="" y="{Y}">Anno</y>
    <txt n="" _txt="">TXT Color</txt>
    <bg n="" bg="">Background</bg> 
</Config>
        ''')
## RIAPRO IL FILE XML PER PRENDERE I DATI DI CONFIGURAZIONE
with open(CFG,mode='r') as F:
    thm = F.read()
    data = BeautifulSoup(thm, 'xml')
    theme = data.find('theme')
    version = data.find('ver')
    ver_ = version.get('ver')
    cf = theme.get('theme')
    try:
        anno = data.find('y')
        Yy= anno.get('y')
    except:
        with open(CFG, mode='w') as F: # Scrivo il file di configurazione con le impostazioni aggiornate
            F.write(f'''
            <Config>
                <theme n="" theme="{cf}">Tema</theme>
                <ver n="" ver="{ver}">Ver</ver> 
                <y n="" y="{Y}">Anno</y>
                <txt n="" _txt="">TXT Color</txt>
                <bg n="" bg="">Background</bg> 
            </Config>
        ''')
        Yy = Y
_theme = cf # Variabile per il tema
## Configurazione del tema in app
if cf == 'Dark':
    _theme = 'Dark'
    if _data == '31/10': # Tema prestabilito per Halloween
        _palette = 'Orange'
    else:
        _palette = 'Gray'
    _text = 'white'
else:
    _theme = 'Light'
    if _data == '31/10': # Tema prestabilito per halloween
        _palette = 'Red'
    else:
        _palette = 'Blue'
    _text = 'black'
## CREO LA CONNESSIONE CON IL DATABASE
connect = sqlite3.connect(SAF)
cursor = connect.cursor()
# SE non esiste creo la tabella, aprendo il file TXT, inserendo i valori nella tabella (giorno,mese,ora) in formato stringa
## In assenza del file TXT la tabella sarà stata creata ma vuota
try:
    cursor.execute('create table straordinari (gg text, mm text, ora text)')         # <------
    #with open('/storage/emulated/0/StraordinApp/Straordinari.txt', 'r') as F:       # <------
    with open('straordinari.txt', 'r') as F:
        l=F.readlines()
        for i in l:
            data= (i[:2],i[3:5],i[7:9])
            _file_value_list.append(data)
        cursor.executemany('insert into straordinari values (?,?,?)', _file_value_list)
        connect.commit()
except sqlite3.OperationalError:
    pass
except FileNotFoundError:
    _file_value_list.append(('','',''))
    cursor.executemany('insert into straordinari values (?,?,?)', _file_value_list)
    connect.commit()
############### CREO UNA FUNZIONE PER IL CALCOLO DEL TOTALE DELLE ORE STRAORDINARIE
def tot_write(self,m, id, _text=_text):
    '''
    Restituisce il totale delle ore nel mese selezionato.
    Il parametro 'id' serve per scegliere quale label modificare (in base allo screen)
    :param self:
    :param m:
    :param id:
    :return:
    '''
    connect.commit() # assicuro il commit di eventuali modifiche
    tot = 0.0 # resetto il totale per calcolare il tot delle ore
    for row in cursor.execute('SELECT  gg,mm,ora FROM straordinari'):
        if row[1] == m: # se nella riga è presente il mese selezionato
            tot = tot + float(row[2]) # viene sommato il totale della colonna relativa alle ore
    self.root.ids.tot.text_color = _text
    self.root.ids.src_tot.text_color = _text
    ## CAMBIO IL COLORE IN BASE AL QUANTITATIVO DI ORE STRAORDINARIE TOTALI
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

actual_day = False # --------- Booleana utilizzata per controllare il giorno attuale
state = True   # ------------- Booleana utilizzata per l'icona ricerca/indietro
## CREAZIONE DELLE CLASSI COLLEGATE AL FILE KV
class modifica(BoxLayout):
    pass
class add(BoxLayout):
    pass
class Cerca(BoxLayout):
    pass

################################## CREAZIONE DELLA CLASSE PER L'APP ##################################################
class Main(MDApp):
    def build(self):
        '''
        Costruzione dell App.
        Nel primo statement controllo se l'app viene aperta l'anno dopo quello registrato nel file di configurazione.
        In tal caso, salvo il database dell'anno precedente, azzero il database attuale e parte la dialog di buon anno
        Infine setto l'icona (Per la versione desktop), il tema, la palette e carico il file KV
        :return:
        '''
        if int(Yy) < int(Y):
            self.nydialog = MDDialog(title=Y, text=f'BUON INIZIO ANNO NUOVO!!!')
            self.nydialog.open()
            shutil.copy(SAF, str(int(Y) - 1) + '.db')
            cursor.execute('DELETE FROM straordinari')
            connect.commit()
        self.icon = ico
        self.title = 'StraordinApp'
        self.theme_cls.theme_style = _theme
        self.theme_cls.primary_palette = _palette
        return Builder.load_string(KV)
    def dial(self, switch):
        '''
        Funzione a parte per la gestione delle dialogs
        :return:
        '''
        if switch == 1:
            self.dialog = MDDialog(
				title=f'VER. {ver}rc',
				type='simple',
				text='''
- Non verranno più esportati i file se i mesi sono privi di 
  ore straordinarie
''' )
            self.dialog.open()
        elif switch == 2:
            self.dialog = MDDialog(
				title='Info',
				type='simple',
				text=f'''
StraordinApp Versione {ver}rc

#Scritto in Python 3.10.6
    Librerie: 
     - Kivy 2.1.0
     - Kivymd 1.0.2
     - BeautifulSoup4 4.11.1
     
#Contatto: 
    andrewdm91@gmail.com
    
#GitHub:
    https://github.com/noxsilente/StraordinApp
                    '''
                 )
            self.dialog.open()
        elif switch == 3:
            self.dialog = MDDialog(
                title=f'Logs',
                type='simple',
                text=dial
            )
            self.dialog.open()
    def _modifica(self,x, i, G, M):
        '''
        Richiamo a una classe esterna nel file KV
        Grazie a questa funzione, è possibile modificare le ore di un determinato giorno
        (Valido solo per il mese attuale)
        :param x:
        :param index:
        :param f_v:
        :return:
        '''
        f_v = f'{G}/{M}' #standardizzo la data presa dalla funzione lambda
        value = self.mod_dialog.content_cls.ids.new_value.text # ricevo il valore dalla dialog
        i.theme_text_color = 'Custom' # modifico il colore e il testo dell Item
        i.text_color = 'magenta'
        i.text = f'* {f_v} +{value}\n'
        # Faccio l update nel database trovando la riga con l'esatto giorno e mese
        cursor.execute(f'UPDATE straordinari SET ora = \'{int(value)}\n\' WHERE gg=\'{G}\' AND mm=\'{M}\'')
        self.mod_dialog.dismiss()
        self.menu.dismiss()
        tot_write(self,M,1)
    def menu_(self, i,gg,mm,local):
        def _remove_():
            '''
            Rimuove l'item dalla lista e dal database
            :return:
            '''
            if local == 1:
                self.root.ids._oli.remove_widget(i)
            elif local == 2:
                self.root.ids._src_date.remove_widget(i)
            cursor.execute(f'DELETE FROM straordinari WHERE gg=\'{gg}\' AND mm=\'{mm}\'')
            self.conferma.dismiss() # chiudo il dialog di conferma
            tot_write(self,mm,local)
            ##### LA LOCAL SERVE AD ASSICURARE L'ELIMINAZIONE DEL WIDGET GIUSTO
            ####  CREO LA LISTA DEL MENU RICHIAMATA CON IL DROPMENU
            ###   LA FUNZIONE DI MODIFICA NON E' IMPLEMENTATA SE LO SCREEN NON E' QUELLO PRINCIPALE
        menu_items = [
            {
                'viewclass': 'OneLineListItem',
                'theme_text_color': 'Custom',
                'text_color': 'magenta',
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
                ), ])
        self.mod_dialog = MDDialog(
            title=f'Modifica ',
            type='custom',
            content_cls=modifica(),
            buttons=[
                MDFlatButton(
                    text='OK',
                    on_release=lambda x, i=i , G=gg, M=mm, local=local: self._modifica(x, i, G, M)
                ),
                MDFlatButton(
                    text='Cancella',
                    on_release=lambda x: self.mod_dialog.dismiss()
                )
            ]
        )
    def on_stop(self):
        '''
        Chiusura del collegamento con il database e aggiornamento del file di configurazione
        :return:
        '''
        with open(CFG, mode='w') as F: # Scrivo il file di configurazione con le impostazioni aggiornate
            F.write(f'''
            <Config>
                <theme n="" theme="{cf}">Tema</theme>
                <ver n="" ver="{ver}">Ver</ver>                            
                <y n="" y="{Y}">Anno</y>
                <txt n="" _txt="">TXT Color</txt>
                <bg n="" bg="">Background</bg> 
            </Config>
                    ''')
        try:
            cursor.close()
        except:
            pass
        connect.close()
    def on_start(self):
        '''
        Funzione che parte all'avvio dell'app
        :return:
        '''
        global actual_day
        if ver != ver_: # Dialog che appare quando con l'aggiornamento della versione
            self.dial(1)
        else:
            pass
        self.root.ids.IN_B.text_color = _text                     ####
        self.root.ids.MDRFIB.text = _theme                          ##
        self.root.ids.src.text_color = _text                        ##
        self.root.ids.export.text_color = _text                     ##
        self.root.ids.MDRFIB.text_color = _text                     ## COLORAZIONI IN BASE AL TEMA
        self.root.ids.MDND_.color = _text                           ##
        self.root.ids.MDND.color = _text                          ####
        self.root.ids.KV_ver.text = f'versione: {ver}'
        self.root.ids.data.title = f'StraordinApp - {_data}'
        for row in cursor.execute(f'SELECT * FROM straordinari WHERE mm ={m}'):
            self.root.ids._oli.add_widget(OneLineListItem(text=f'{row[0]}/{row[1]} +{row[2]}', on_release=lambda
                        x=enumerate(row), g=row[0], M=row[1]: self.menu_(x, g,M, 1)))
            if row[0] == d:
                actual_day = True
        tot_write(self, m, 1)
    def _add_(self):
        def adding():
            gg = self.add_dialog.content_cls.ids.day.text
            ora = self.add_dialog.content_cls.ids.ore.text
            if float(ora) == 0.0:
                self.add_dialog.content_cls.ids.ore.hint_text = 'Non valido!!'
            elif '.0' in ora:
                ora = int(ora)
            else:
                self.add_dialog.content_cls.ids.day.text = ''
                self.add_dialog.content_cls.ids.ore.text = ''
                self.add_dialog.content_cls.ids.ore.hint_text = 'Inserisci il numero di ore'
            for row in cursor.execute(f'SELECT gg FROM straordinari WHERE mm={m}'):
                if int(gg) != int(row[0]):
                    if int(gg) < 10:
                        gg= '0'+gg
                    self.add_dialog.content_cls.ids.add_l.text = f'{gg}/{m}  +{str(ora)}'
                    self.root.ids._oli_.add_widget(
                    OneLineListItem(text=f'{gg}/{m} +{ora}', theme_text_color='Custom',
                                        text_color='#0033cc', on_release=lambda x: self.not_implemented(2)))
                    cursor.execute(f'INSERT INTO straordinari (gg,mm,ora) VALUES (\'{gg}\',\'{m}\',\'{ora}\n\')')
                    connect.commit()
                    break
                else:
                    self.add_dialog.dismiss()
                    Snackbar(text='Modificare dall\'apposito menù' ).open()
        ################# PICCOLA PARTE PER ORDINARE IN MODO CRESCENTE IL DATABASE ###########
        ##   L'ORDINAMENTO E' IMMEDIATO NEL CASO SI VOGLIA FARE UN EXPORT SU FILE TXT       ##
        ##   SENZA AVERE PROBLEMI CON L'ORDINE CRONOLOGICO DELLE DATE                       ##
        ######################################################################################
            lista = [] ## CREO UNA LISTA TEMPORANEA
            ## INSERISCO I VALORI (GIORNO) DEL DATABASE ORDINATI IN MODO CRESCENTE ##
            for row in cursor.execute(f'SELECT * FROM straordinari WHERE mm={m} ORDER BY CAST(gg AS INTEGER)'):
                data = (row[0], row[1], row[2])
                lista.append(data)
            ## ELIMINO I VALORI DELLA LISTA RELATIVI AL MESE CORRENTE
            cursor.execute(f'DELETE FROM straordinari WHERE mm={m}')
            ## RISCRIVO I VALORI IN ORDINE CRESCENTE NELLA LISTA
            for i in lista:
                cursor.execute('INSERT INTO straordinari VALUES (?,?,?)', i)
            ## SALVO IL TUTTO E VADO A FARE IL TOTALE.
            connect.commit()
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
        global actual_day
        _temp_txt = str(self.root.ids.TXT.text)
        self.root.ids.TXT.text = ''
        if _temp_txt == '':
            return
        if actual_day :
            for row in cursor.execute(f'SELECT ora FROM straordinari WHERE gg={d} AND mm = {m}'):
                temp_tot= float(row[0]) + float(_temp_txt)
            if '.0' in str(temp_tot):
                cursor.execute(f'UPDATE straordinari SET ora=\'{int(temp_tot)}\n\' WHERE gg={d} AND mm = {m}')
                self.root.ids._oli.add_widget(OneLineListItem
                                              (text=f'\n{d}/{m} +{int(temp_tot)}', theme_text_color='Custom',
                                               text_color='green',on_release=lambda x: self.not_implemented(2)))
            else:
                cursor.execute(f'UPDATE straordinari SET ora=\'{float(temp_tot)}\n\' WHERE gg={d} AND mm = {m}')
                self.root.ids._oli.add_widget(OneLineListItem
                                              (text=f'\n{d}/{m} +{temp_tot}', theme_text_color='Custom',
                                               text_color='green', on_release=lambda x: self.not_implemented(2)))
        else:
            cursor.execute(f'INSERT INTO straordinari (gg,mm,ora) VALUES ({d},{m},{_temp_txt})')
            self.root.ids._oli.add_widget(OneLineListItem
                (text=f'\n{d}/{m} +{_temp_txt}', theme_text_color='Custom', text_color='green',
                on_release=lambda x: self.not_implemented(2)))
        actual_day=True
        self.root.ids._ok.text = f'+{_temp_txt}'
        tot_write(self,m,1)
    def theme_changer(self): ### TODO Creare una pagina di scelta del tema
        '''
        Cambia automaticamente il tema appena viene selezionato, senza dover riavviare l'applicazione
        Colori per le palette: ‘Red’, ‘Pink’, ‘Purple’, ‘DeepPurple’, ‘Indigo’, ‘Blue’, ‘LightBlue’,
        ‘Cyan’, ‘Teal’, ‘Green’, ‘LightGreen’, ‘Lime’, ‘Yellow’, ‘Amber’, ‘Orange’, ‘DeepOrange’,
        ‘Brown’, ‘Gray’, ‘BlueGray’.

        :return:
        '''
        global cf
        if cf == 'Dark':
            _theme = 'Light'
            if _data == '31/10':
                _palette = 'Red'
            else:
                _palette = 'Blue'
            _text = 'black'
            cf = 'Light'
        elif cf == 'Light':
            _theme = 'Dark'
            if _data == '31/10':
                _palette = 'Orange'
            else:
                _palette = 'Gray'
            _text = 'white'
            cf = 'Dark'
        self.theme_cls.theme_style = _theme
        self.theme_cls.primary_palette = _palette
        self.root.ids.IN_B.text_color = _text
        self.root.ids.src_tot.text_color = _text
        self.root.ids.tot.text_color = _text
        self.root.ids.src.text_color = _text
        self.root.ids.export.text_color= _text
        self.root.ids.info.text_color = _text
        self.root.ids.MDND_.color = _text
        self.root.ids.MDND.color = _text
        self.root.ids.MDRFIB.text_color = _text
        self.root.ids.MDRFIB.text = _theme
        self.root.ids.nav_d.set_state(new_state='close', animation=True)
        tot_write(self, m,1,_text)
    def Search_export(self,value,type):
        '''
        Trova nel database il mese in base al valore ricevuto
        :param value:
        Seleziono che cosa devo fare: se ricerca o esportazione su file
        :param type:
        :return:
        '''
        self.date_dial.dismiss()
        mm=value+1 # aggiungo 1 per compensare l'index il quale parte da 0
        if mm <10: # se il valore è inferiore a 10 devo aggiungere '0' alla stringa per fare la ricerca nel database
            mm='0'+str(mm)
        else:
            mm= str(mm)
    ##### RICERCA DEL MESE SU APPOSITO SCREEN
        if type==1:
            self.root.ids._src_date.clear_widgets()
            for row in cursor.execute(f'SELECT * FROM straordinari'):
                if row[1]==mm:
                    self.root.ids._src_date.add_widget(OneLineListItem
                                (text=f'{row[0]}/{row[1]} +{row[2]}', on_press=lambda x=enumerate(row): self.menu_(x, row[0], mm, 2)))
            tot_write(self, mm, 2)
    ##### ESPORTAZIONE DEL MESE SU FILE TXT
        elif type==2:
            temp_list = []
            for row in cursor.execute(f'SELECT gg,mm,ora FROM straordinari'):
                if row[1] == mm:
                    temp_list.append(f'{str(row[0])}/{str(row[1])} +{str(row[2])}')
            if len(temp_list)==0:
                self.d = MDDialog(title=f'{str(month_list[int(mm) - 1])}-{Y}',
                                  text='NON CI SONO STRAORDINARI IN QUESTO MESE')
                self.d.open()
            ### DECOMMENTARE PER L'APP
            else:
                # with open(f'/storage/emulated/0/StraordinApp/{str(month_list[int(mm) - 1])}-{Y}.txt', mode='w') as F:  # <------
                with open(f'{str(month_list[int(mm) - 1])}-{Y}.txt', mode='w') as F:             # <------
                    F.writelines(temp_list)
                self.d = MDDialog(title=f'{str(month_list[int(mm) - 1])}-{Y}.txt',
                                  text='FILE ESPORTATO SU MEMORIA INTERNA:\n\n/storage/emulated/0/StraordinApp/')
                self.d.open()
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
    def date_dialog(self,id):# Istanza per aprire il dialog relativo alla ricerca per mese
        self.date_dial= MDDialog(
            title= 'Seleziona il Mese: ',
            type= 'custom',
            content_cls=Cerca(), )
        for i in range(len(month_list)): # Aggiungo i widget con il nome del mese
            self.date_dial.content_cls.ids.Cerca_list.add_widget(OneLineListItem(text=month_list[i], on_release=lambda x, i=i, id=id: self.Search_export(i,id) ))
        self.date_dial.open()
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
        state = False # per il Pre_Nav_Change
    def Pre_Nav_Change(self):
        '''
        Funzione di switch tra i comandi per il cambio della pagina:
        Se lo stato è impostato su False, verrà chiamata la funzione per il ritorno nello screen principale.
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