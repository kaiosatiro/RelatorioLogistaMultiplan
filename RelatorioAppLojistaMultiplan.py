from datetime import datetime
from time import strftime
from tkinter import TclError
import PySimpleGUI as sg
import psycopg2


def limpar_entrada():
    for key in values:
        if key == 'Escolher': continue
        window[key]('')
    return None


def validadadosA(I, F):
    inicial = I
    final = F
    try:  
        if I[-1] not in ('0123456789/'): inicial = I[:-1]
        if len(I) == 2: inicial = I[-2:] + '/'
        elif len(I) == 3: inicial = I[:-1]
        elif len(I) == 5: inicial = I + '/'
        elif len(I) == 6: inicial = I[:-1]
        elif len(I) > 10: inicial = I[:-1]
    except IndexError:
        pass
    try:
        if F[-1] not in ('0123456789/'): final = F[:-1]
        if len(F) == 2: final = F + '/'
        elif len(F) == 3: final = F[:-1]
        elif len(F) == 5: final = F + '/'
        elif len(F) == 6: final = F[:-1]
        elif len(F) > 10: final = F[:-1]  
    except IndexError:
        pass
    return inicial, final


def validadadosB(I, F):
    formato = "%d/%m/%Y"
    try: I = bool(datetime.strptime(I, formato))
    except ValueError:
        I = False
    try: F = bool(datetime.strptime(F, formato))
    except ValueError:
        F = False
    return I, F


def gerarelatorio(datainicial, datafinal, path):
    dataini = datetime.strptime(datainicial, '%d/%m/%Y').strftime('%Y-%m-%d 00:00:00')
    datafim = datetime.strptime(datafinal, '%d/%m/%Y').strftime('%Y-%m-%d 23:59:59') 
    try:
        conn = psycopg2.connect("user=multiplan host=localhost dbname=parkingplus password=multiplan")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM abonolojistamultiplan WHERE datahorasaida BETWEEN '{dataini}' AND '{datafim}';")
        query = cursor.fetchall()
        with open(f'{path}/AppLojista_{strftime("%d-%m-%Y")}.csv', 'w') as csv:
            csv.writelines('Ticket;Valor;DATA;Hora\n')
            soma = 0
            for index, row in enumerate(query):
                ticket = row[0]
                valor = str(row[1])
                data = row[2].strftime('%d-%m-%Y')
                hora = row[2].strftime('%H:%M:%S')
                linha = [ticket, ';', valor, ';', data, ';', hora,'\n']
                csv.writelines(linha)
                soma += row[1]
            csv.writelines(f"TOTAL:  {index+1};  {soma:0.2f}R$")
    except psycopg2.OperationalError:
        sg.popup_error('Erro na conculta ou no Banco de dados')
    except psycopg2.DatabaseError:
        sg.popup_error('Erro no Banco de dados')
    except IndexError:
        sg.popup_error('Index error')
    except OSError:
        sg.popup_error('Erro de sistema operacional')
    else:
        sg.popup('Pronto!')
    finally:
        return None

sg.theme('Default1')
layout = [
    [sg.Text('Escolha o intervalo de datas: ', enable_events=True)],
    [sg.Text('Data Inicial', size=(10,1)), sg.InputText(key='inicial', size=15, enable_events=True), 
        sg.Text('Data Final:',  size=(10,1)), sg.InputText(key='final', size=15, enable_events=True)],
    [sg.Text('Salvar na Pasta: '), sg.FolderBrowse('Escolher')],
    [sg.Submit('Gerar', disabled=True), sg.Button('Limpar'), sg.Exit()]
]

window = sg.Window('Relatório Abono App Logista', layout, icon='wps.ico')
while True:
    try:
        event, values = window.read()
        inicial, final = validadadosA(values['inicial'], values['final'])
        window['inicial'].update(inicial, text_color='black')
        window['final'].update(final, text_color='black')
        if event == sg.WIN_CLOSED or event == 'Exit': break
        if event == 'Limpar': limpar_entrada()
        if values['Escolher'] != '': window['Gerar'].update(disabled=False)
        if event == 'Gerar':
            inicio, fim = validadadosB(inicial, final)
            if not inicio or not fim: sg.popup('Data Inválida')
            if not inicio: window['inicial'].update(text_color='red')
            if not fim: window['final'].update(text_color='red')
            if inicio and fim:
                caminho = values['Escolher']
                gerarelatorio(inicial, final, caminho)
    except TclError:
        pass
    except TypeError:
        break
window.close()




