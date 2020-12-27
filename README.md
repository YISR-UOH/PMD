# PMD
Proyecto de Procesamiento Masivo de datos COM4002-1 - Segundo Semestre 2020

===================================================================================================================================================================================

Motor de busqueda para para el foro de U-campus, almacena todos los hilos creados con sus datos (titulo, autor, cantidad de mensajes y contenido del hilo) Proyecto para Procesamiento Masivo de Datos, COM4002-1 - Segundo Semestre 2020 Universidad de O'Higgins.

Extrae los datos del foro de U-campus y los almacena en json, para posteriormente procesarlos.

Se necesita tener los siguientes modulos de python:

-selenium -BeautifulSoup -pandas -numpy (1.19.3) -webdriver

Todos los datos se almacenaron en una plataforma virtual de mongobd (ATLAS mongodb), por lo que cualquiera puede acceder a los datos (solo lectura). Username: UOH Pass: UOHanon2020

Conectarse:

desde shell mongo "mongodb+srv://mensajes.dp9ov.mongodb.net/PMD" --username UOH les pedira una contrasenia, usar UOHanon2020.
desde alguna app como compass mongodb+srv://UOH:UOHanon2020@mensajes.dp9ov.mongodb.net/PMD
desde vs code mongodb+srv://UOH:UOHanon2020@mensajes.dp9ov.mongodb.net/PMD?retryWrites=true&w=majority
