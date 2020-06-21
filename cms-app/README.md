Autor: Lic. Manuel A. Camino - 2020

# Introducción
La presente aplicación web es un trabajo practico final para la materia "Desarrollo de Aplicaciones Web" de la especializacion en Internet de las Cosas (CEIoT) de la Facultad de Ingenieria de la Universidad de Buenos Aires.

# Descripción
La aplicación esta compuesta de un front-end (Typescript compilado a Javascript) y un back-end (Node.js + MySql). Su arquitectura es SPA (Single Page Application) con lo cual todos los requests se realizan mediante XMLHTTPRequest al back-end con la finalidad de no volver a cargar la pagina.

El back-end contiene queries SQL ya pre-definidos en caso de que pase 
<a href="https://imgs.xkcd.com/comics/exploits_of_a_mom.png">Roberto Tablas</a> y quiera generarnos un mal dia.

# Correr la aplicación
Previo a la ejecucion de la aplicacion, asegurarse de tener instalado docker y docker-compose. Caso contrario podran encontrar la documentacion para instalar estas dos herramientas en los siguientes enlaces:
- ![DOCKER](https://docs.docker.com/get-docker/)
- ![DOCKER COMPOSE](https://docs.docker.com/compose/install/)

Una vez realizado el clone del repositorio y haber descargado la aplicacion, nos ubicamos en el directorio raiz y ejecutamos el siguiente comando:
```sh
docker-compose up
```

NOTA: En caso de que al correr por primera vez no logre correr el container nodejs-container exitosamente, terminar el programa con CTRL-C, esperar a que se paren los containers y volver a correr docker-compose up.

Una vez que los contenedores esten corriendo exitosamente, podremos acceder a la aplicacion desde la siguiente direccion:
```
http://localhost:8000
```

# Agradecimientos
A los profesores:
- Ernesto Gigliotti
- Brian Ducca
- Agustin Bassi

A mis compañeros de cursada por haberse tomado el tiempo para ayudarme (Y mas por la paciencia)

# Contribuir
Para contribuir realizar un pull request con las sugerencias.

# Licencia
GPL