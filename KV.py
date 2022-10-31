#                   LAYOUT DELL'APP
KV = '''
MDNavigationLayout:
    MDTopAppBar:
        pos_hint: {'center_x': .5, 'center_y':.95}
        id: data
        title: 'StraordinApp'
        right_action_items: [['dots-vertical', lambda x: nav_d.set_state('toggle')]] 
    ScreenManager: 
        id: S_M        
        Screen:
            name: 'M' 
            BoxLayout:
                orientation: 'vertical'
                pos_hint: {'center_x':.5, 'center_y':.4}
                RelativeLayout:
                    pos: self.parent.pos
                    MDTextField:
                        id: TXT
                        pos_hint: {'x':0.01, 'y':0.7}
                        size_hint_x: 0.35
                        input_filter: 'float'
                        required: True
                    MDRectangleFlatButton:
                        id: IN_B
                        pos_hint: {'x':0.4, 'y':0.75}
                        size_hint_x: 0.2
                        theme_text_color: 'Custom'
                        text:'INSERISCI'
                        on_release: app.writing()
                    MDLabel:
                        id: _ok
                        pos_hint: {'x':0.65, 'y':0.33}
                        font_style: 'H4'
                        theme_text_color: 'Custom'
                        text_color: 'limegreen'
                      
                    ScrollView:
                        id: s_w
                        do_scroll_x: False
                        pos_hint: {'x':0, 'y':-0.5}
                        size_hint_y: 1
                        size_hint_x: 0.5
                        MDList:
                            id: _oli   
                    ScrollView:
                        id: s_w_2
                        do_scroll_x: False
                        pos_hint: {'x':.6, 'y':.1}
                        size_hint_y: 0.5
                        size_hint_x: 0.5
                        MDList:
                            id: _oli_              
                MDLabel:
                    id: tot
                    pos_hint:{'x': 0.7, 'y':-0.35}
                    font_style: 'H5'
                    theme_text_color: 'Custom'
                    text_color: 'white'
        Screen:
            name: 'S'
            BoxLayout:
                orientation: 'vertical'
                pos_hint: {'center_x':.5, 'center_y':.4}
                RelativeLayout:
                    pos: self.parent.pos
                    MDRectangleFlatButton:
                        id: IN_B
                        pos_hint: {'x':0.1, 'y':0.85}
                        size_hint_x: 0.2
                        text:'CERCA'
                        on_press: 
                            #nav_d.set_state('close')
                            app.date_dialog()
                    MDLabel:
                        id: one_src_date 
                        pos_hint: {'x':.0, 'y':0.1}
                        font_style: 'H5'
                        theme_text_color: 'Custom'
                        text: ''
                    MDLabel:
                        id: src_tot 
                        pos_hint: {'x':.6, 'y':.4}
                        font_style: 'H5'
                        theme_text_color: 'Custom'
                        text: ''
                    ScrollView:
                        id: s_w_
                        do_scroll_x: False
                        pos_hint: {'x':.4, 'y':.2}
                        size_hint_y: 0.5
                        size_hint_x: 0.5
                        MDList:
                            id: _src_date    
                
                    
    MDNavigationDrawer: 
        anchor: 'right'
        size_hint_x: .5
        id: nav_d
        close_on_click: True
        BoxLayout:
            anchor: 'left'
            orientation: 'vertical'
            pos_hint: {'center_x': .5, 'center_y':.85}
            spacing: '10dp'
            Image:
                size_hint: 1, None
                size: '70dp', '70dp'
                source: 'SA+1.png'
            MDNavigationDrawerDivider:
                id: MDND_
            MDRectangleFlatIconButton:
                id: MDRFIB
                #size_hint_x: .5
                text: 'tema'
                font_style: 'H6'
                icon: 'theme-light-dark'
                line_color: 0,0,0,0
                on_press: app.theme_changer()
            MDRectangleFlatIconButton:
                id: src
                #size_hint_x: .5
                text: 'Cerca'
                font_style: 'H6'
                icon: 'magnify'
                line_color: 0,0,0,0
                #on_press: app.not_implemented()
                on_press: app.Pre_Nav_Change()
            MDRectangleFlatIconButton:
                id: add
                #size_hint_x: .5
                text: 'Aggiungi'
                font_style: 'H6'
                icon: 'plus'
                line_color: 0,0,0,0
                text_color: '#007f00'
                #on_press: app.not_implemented(1)
                on_press: app._add_()
            MDRectangleFlatIconButton:
                id: export
                #size_hint_x: .5
                text: 'Esporta'
                font_style: 'H6'
                icon: 'file-export-outline'
                line_color: 0,0,0,0
                text_color: '#007f00'
                on_press: app.date_dialog2()
            MDRectangleFlatIconButton:
                id: info
                #size_hint_x: .5
                text: 'Info'
                font_style: 'H6'
                icon: 'information'
                line_color: 0,0,0,0   
                on_press: app.dial(2)
            MDRectangleFlatIconButton:
                id: exit
                #size_hint_x: .5
                text: 'Esci'
                font_style: 'H6'
                theme_color: 'Custom'
                icon_color: '#f00000'
                text_color: '#f00000'
                icon: 'exit-to-app'
                line_color: 0,0,0,0   
                on_press: app.stop()
            MDNavigationDrawerDivider:
                id: MDND
            MDRectangleFlatIconButton:
                id: KV_ver
                pos_hint: {'center_x':.5, 'center_y':.9}
                size_hint_x: 1
                icon: 'information-outline'
                line_color: 0,0,0,0
                text: 'ver.'
                on_release: app.dial(3) 
                    #app.not_implemented()                            
                
<modifica>
    orientation: 'vertical'
    spacing: '12dp'
    size_hint_y: None
    height: '60dp'
    MDTextField:
        id: new_value
        hint_text: "Aggiungi il nuovo orario"   
<add>
    orientation: 'vertical'
    spacing: '12dp'
    size_hint_y: None
    height: '120dp'
    MDLabel:
        id: add_l
        pos_hint: {'x': .8, 'y':.5}
        theme_text_color: 'Custom'
        text_color: '#005f00'
        text: ''
    MDTextField:
        required: True
        input_filter: 'int'
        size_hint_x: .1
        id: day
        hint_text: 'Inserisci il numero del giorno'
    MDTextField:
        required: True
        input_filter: 'float'
        size_hint_x: .1
        id: ore
        hint_text: 'Inserisci il numero di ore'  
'''

#           STRINGHE CHE RIEMPIONO INUTILMENTE IL FILE MAIN.PY
dial='''
1.3.2rc 
- BugFix vari 

1.3 
-Creazione di un database (più pesante ma con meno errori)
-Possibilità di esportare la lista ore di un mese su un file di testo

1.2.6 
- Aggiunta la possibilità di aggiungere giorni ed ore al mese corrente
- Risolto qualche bug minore

1.1.0 - BETA
- Aggiunta la possibilità di aggiungere giorni ed ore al mese corrente

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