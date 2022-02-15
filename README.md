# FastAPI-IoT

- User CRUD.
- CRUD of things.
- API with MySQL connection.
- Visualization, monitoring and control of processes. *(Coming soon)*
- Connection to MathLab and R, for results analysis and evaluation. *(Coming soon)*

## MySQL - Database structure
<p align="center"> <img src="https://user-images.githubusercontent.com/63327224/154146336-1e270c8b-ad39-4efc-9d98-754f3d6c7e64.jpg" width="350"> <img src="https://user-images.githubusercontent.com/63327224/154146638-07736fbb-5339-40c8-baa7-5d9fdc80ee1a.jpg" width="350"> </p>

### Clarifications
Los valores presentes en la tabla de *Things,* **modification_dates = SET[datatime]**, es un conjunto de todas las fechas en las que se ha usado la **Thing.**

Los valores presentes en la tabla de *Users,* **things = SET[thing_id]**, es un conjunto de todos los UUID que hacen referencia a las **Things** que un usuario tiene a disposición.

## In development
Se creara una base de datos adicional donde se guardara el conjunto de datos que una determinada **Thing** haya recolectado, posteriormente se analiza y dicho análisis también se guarda con el fin de comparar, y tener un seguimiento.
El análisis se hará por medio de MATLAB y/o de R, utilizando métodos como lo son el de Máxima Verosimilitud para el análisis de probabilidades en procesos estocásticos.
