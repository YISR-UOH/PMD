import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json

'''
created by Yerko Sepulveda Rojas
github=github.com/YISR-UOH
mail=yerko.sepulveda@pregrado.uoh.cl

programa para extraer datos del foro de U-campus
'''
def concatenar(i,j,lista):
    z=""
    for a in range(i,j):
        z=z+lista[a]+' '
    return z
  
def buscar(cadena):
    if '/' in cadena[-4]:
        cadena=cadena[0:-6]+[cadena[-6]+cadena[-5]]+cadena[-3:]
    autor=''
    for l in range(cadena.index('Por')+1,cadena.index(cadena[-4])):
        try:
            int(cadena[l])
            break
        except:
            autor=autor+cadena[l]+' '
    if 'Ayer' in cadena[-4]:
        
        return [False,autor]
    if 'Hoy' in cadena[-4]:
        return [False,autor]
    else:
        return [True,autor]


def buscar2(cadena):
    if '/' in cadena[-4]:
        cadena=cadena[0:-6]+[cadena[-6]+cadena[-5]]+cadena[-3:]
    autor=''
    for l in range(0,cadena.index(cadena[-4])):
        try:
            int(cadena[l])
            break
        except:
            autor=autor+cadena[l]+' '
    if 'Ayer' in cadena[-4]:
        return [False,autor]
    if 'Hoy' in cadena[-4]:
        return [False,autor]
    else:
        return [True,autor]

def myreplace(cadena):
    cadena=cadena.replace('respuestaPor','respuestas Por')
    cadena=cadena.replace('\tResponder','')
    cadena=cadena.replace('\tPadre','')
    cadena=cadena.replace('\t Compartir','')
    cadena=cadena.replace('\t',' ')
    cadena=cadena.replace('\n','')
    return cadena
# Conexion y validación de usuario del sistema 
option = webdriver.ChromeOptions()
option.add_argument("--headless")
browser = webdriver.Chrome()

browser.get(('https://ucampus.uoh.cl/m/foro_institucion/'))

# Usar identificadores validos con acceso al foro
usernameStr = "" 
passwordStr = ""

username = browser.find_element_by_name('username')
username.send_keys(usernameStr)
password = browser.find_element_by_name('password')
password.send_keys(passwordStr)
signInButton = browser.find_element_by_class_name('boton')
signInButton.click()
time.sleep(2)

siguiente = browser.find_element_by_class_name('paginar')
siguiente = siguiente.text
siguiente = siguiente.split("\n")
siguiente = siguiente[-2]
print("Paginas a leer --> ",siguiente)


body = browser.execute_script("return document.body")
source = body.get_attribute('innerHTML')
soup = BeautifulSoup(source,"html5lib")

data_final=[]
total=0
k=1

while(k<int(siguiente)):
    l=soup.find_all(class_="objetos")
    l=l[0].get_text()
    l=l.split('\tCerrar')
    data=[]
    i=0
    flag=0
    while(i<len(l)-1):
        try:
            while(i<len(l)-1):
                l[i]=myreplace(l[i])
                l[i]=l[i].split('hrs.',1)
                aux=l[i][0].split()
                x=0
                try:
                    if aux.index('respuesta'):
                        x=aux.index('respuesta')
                except:
                    if aux.index('respuestas'):
                        x=aux.index('respuestas')
                aux2=x-1
                titulo=concatenar(0,aux2,aux)
                num=int(aux[aux2])
                aux3=buscar(aux)
                autor= aux3[1]
                l[i][1]=l[i][1].split('hrs.',1)
                comentarios=[]
                aux_i=i
                for j in range(0,num):
                    aux=l[aux_i+1]
                    aux=myreplace(aux)
                    text=aux.split('hrs.')
                    aux=buscar2(text[0].split())
                    if aux[0]==True:
                        autor1=aux[1]
                    else:
                        autor1= aux[1]
                    comentarios.append([autor1,text[1]])
                    aux_i=aux_i+1
                    
                data.append([titulo,autor,num])
                data[flag]=[data[flag]]+[l[i][1][1]]
                data[flag]=data[flag]+[comentarios]
                flag=flag+1
                i=aux_i
                i=i+1
        except:
            print('error lectura pagina ',k,' elemento ',i)
            i=i+1
        
    data_final=data_final+data
    total=total+i
    k=k+1
    url='https://ucampus.uoh.cl/m/foro_institucion/?id_tema=&offset='+str(k)
    browser.get(url)
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    soup = BeautifulSoup(source,"html5lib")

indices=[]
titulo=[]
autor=[]
mensaje=[]
respuestas=[]
comentarios=[]

data_json = {}
data_json['Mensajes']=[]
ids=0
id_mens=0
for i in range(0,len(data_final)):
    try:
        aux0=i
        aux=data_final[i][0][0]
        aux1=data_final[i][0][1]
        aux2=data_final[i][1]
        aux3=data_final[i][0][2]
        aux4=data_final[i][2]
        indices.append(aux0)
        titulo.append(aux)
        autor.append(aux1)
        mensaje.append(aux2)
        respuestas.append(aux3)
        comentarios.append(aux4)
    except:
        continue
    comentarios_json={}
    comentarios_json['Mensajes']=[]
    id_aux=id_mens
    for i in aux4:
        try:
            id_mens=id_mens+1
            comentarios_json['Mensajes'].append({
                'id_mens':id_mens,
                'autor':i[0].split(),
                'mensaje':i[1]})
        except:
            continue
        
    data_json['Mensajes'].append({
        'id':ids,
        'id_mens':id_aux,
        'autor':aux1.split(),
        'titulo':aux,
        'respuestas':aux3,
        'mensaje':aux2,
        'comentarios':comentarios_json['Mensajes']})
    ids=ids+1
    id_mens=id_mens+1
with open('data.json', 'w') as file:
    json.dump(data_json['Mensajes'], file, indent=7)


print('Total de hilos leidos = ',indices[-1],'\nTotal de mensajes leidos = ',total)

