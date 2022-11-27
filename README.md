

---


## Índice:
- [Descripcion y objetivos](#descripcion-y-objetivos)
- [Prerequisitos](#prerequisitos)
- [Detalles](#detalles)
- [Pasos](#pasos)
- [Exposicion final](#exposicion-final)
- [Entregables](#entregables)

## Descripcion y objetivos

Los objetivos de la práctica son los siguientes:

- Añadir por lo menos un nuevo endpoint a los existentes / y /health, un ejemplo sería /bye que devolvería {"msg": "Bye Bye"}, para ello será necesario añadirlo en el fichero src/application/app.py

- Creación de tests unitarios para el nuevo endpoint añadido, para ello será necesario modificar el fichero de tests

- (Opcional) Creación de helm chart para desplegar la aplicación en Kubernetes, se dispone de un ejemplo de ello en el laboratorio realizado en la clase 3

- Creación de pipelines de CI/CD en cualquier plataforma (Github Actions, Jenkins, etc) que cuenten por lo menos con las siguientes fases:

    - Testing: tests unitarios con cobertura. Se dispone de un ejemplo con Github Actions en el repositorio actual

    - Build & Push: creación de imagen docker y push de la misma a cualquier registry válido que utilice alguna estrategia de release para los tags de las vistas en clase, se recomienda GHCR ya incluido en los repositorios de Github. Se dispone de un ejemplo con Github Actions en el repositorio actual

- Configuración de monitorización y alertas:

    - Configurar monitorización mediante prometheus en los nuevos endpoints añadidos, por lo menos con la siguiente configuración:
        - Contador cada vez que se pasa por el/los nuevo/s endpoint/s, tal y como se ha realizado para los endpoints implementados inicialmente

    - Desplegar prometheus a través de Kubernetes mediante minikube y configurar alert-manager para por lo menos las siguientes alarmas, tal y como se ha realizado en el laboratorio del día 3 mediante el chart kube-prometheus-stack:
        - Uso de CPU de un contenedor mayor al del límite configurado, se puede utilizar como base el ejemplo utilizado en el laboratorio 3 para mandar alarmas cuando el contenedor de la aplicación fast-api consumía más del asignado mediante request

        Las alarmas configuradas deberán tener severity high o critical

    - Crear canal en slack <nombreAlumno>-prometheus-alarms y configurar webhook entrante para envío de alertas con alert manager

    - Alert manager estará configurado para lo siguiente:
        - Mandar un mensaje a Slack en el canal configurado en el paso anterior con las alertas con label "severity" y "critical"
        
        
        Deberán enviarse tanto alarmas como recuperación de las mismas
        Habrá una plantilla configurada para el envío de alarmas

        Para poder comprobar si esta parte funciona se recomienda realizar una prueba de estres, como la realizada en el laboratorio 3 a partir del paso 8.

        Creación de un dashboard de Grafana, con por lo menos lo siguiente:
        - Número de llamadas a los endpoints
        - Número de veces que la aplicación ha arrancado


## Prerequisitos

Es necesario disponer del siguiente software:

- Python 3.8.x o superior y pip3

- Docker 

- minikube (en caso de querer realizarlo en el equipo local)

- kubectl

- helm

## Detalles

1. En la aplicación he añadido dos endpoints:

- `/bye`
- `/riseload`

También he realizado sus correspondientes test.

El endpint `/riseload` incrementa el uso de CPU en el container de la aplicación.

Tras varias pruebas he visto que no es posible utilizarlo de manera adecuada para el propósito de la práctica. 

Sin embargo si es posible utilizarlo en la práctica y en los últimos pasos explico cómo y qué podemos conseguir con su uso.

2. El versionado es con semantic-release.

La generación de las nuevas imágenes se hace realizando el push con un tag que comience con `v`

Se utiliza Github para el CI

3. El deployment tiene *un único pod*. 

No incluye ningún pod con la base de datos

4. El deployment **no contempla ningún escenario de autoescalado**

5. Ante la posibilidad del problema de límites de github actions el desarrollo lo he realizado en un repositorio propio público y es de ahí de donde son las capturas de la parte CI:

https://github.com/roberto-asir/practica-liberando-producto


## Pasos

Para comprobar la práctica puedes seguir estos pasos:

- Clonar el repo

Los archivos necesarios para cumplimentar los requisitos y objetivos de la práctiva están en este repositorio: 
https://github.com/KeepCodingCloudDevops6/liberando-productos-roberto

Puedes clonarlo con el siguiente comando:

`git clone git@github.com:KeepCodingCloudDevops6/liberando-productos-roberto.git`

Luego para ejecutar los siguientes comandos debes situarte dentro del repositorio:

`cd liberando-productos-roberto`

```
    Quick setup — if you’ve done this kind of thing before
or

Get started by creating a new file or uploading an existing file. We recommend every repository include a README, LICENSE, and .gitignore.
…or create a new repository on the command line

echo "# liberndo-productos-roberto" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:KeepCodingCloudDevops6/liberndo-productos-roberto.git
git push -u origin main

…or push an existing repository from the command line

git remote add origin git@github.com:KeepCodingCloudDevops6/liberndo-productos-roberto.git
git branch -M main
git push -u origin main

…or import code from another repository

You can initialize this repository with code from a Subversion, Mercurial, or TFS project.
```


- Iniciar minikube (opcional)

Durante el desarrollo he utilizado `minikube` como entorno para el cluster de kubernetes.

Si deseas utilizar también *minikube* deberás lebantar un profilecon el siguiente comando:

```bash
minikube start --kubernetes-version='v1.21.1' \
    --memory=4096 \
    -p practica-roberto
```
También se puede activar el addon de minikube `metrics-server`:

`minikube addons enable metrics-server -p practica-roberto`

- Descargar los repos de helm

Para la realización de la práctica utilizaremos un chart de helm del operador de prometheus.

Para instalar el repo
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

```


- Instalar dos charts de helm

    - para instalar el chart del operador:

    `helm -n monitoring upgrade --install prometheus prometheus-community/kube-prometheus-stack -f monitoring/custom_values_prometheus.yaml --create-namespace --wait --version 34.1.1`

    - Para instalar la aplicación:

    `helm -n fast-api install fast-api-webapp --wait --create-namespace fast-api-webapp`

- Generar los port-forward para establecer comunicación desde el navegador local

Con esto tenemos las aplicaciones instaladas pero hay que proporcionar acceso a ellas a nuestro navegador.

Lo conseguimos con port-forwarding, este paso es conveniente realizarlo en una pestaña a parte para que el output de estos comandos no aparezca en la pestaña de trabajo:
```
kubectl -n fast-api port-forward svc/fast-api-webapp 8081:8081 & 
kubectl -n monitoring port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 &
kubectl -n monitoring port-forward svc/prometheus-grafana 3000:http-web &
```


> Estos pasos están pensados para un entorno local con *minikube*, si tu entorno emplea otro proveedor deberás tener en cuenta sus necesidades concretas para el acceso a las direcciones y puertos necesarios.

- instalar el dashboard

Ahora debemos instalar el dashboard.

Para ello accede al panel de grafana en https://0.0.0.0:3000

> El usuario es `admin` y la contraseña `prom-operator`

Una vez realizas el login deberás pinchar en el menú vertical de la izquierda: `+ >> Import`

CAPTURACAPTURACAPTURACAPTURA


Selecciona el archivo `dashboard-roberto.json` del directorio `monitoring` del repositorio clonado.



El dashboard tiene los siguientes paneles:

- 6 contadores
    1. Número de llamadas al servidor en la última hora
    2. Número de llamadas al endpoint `/` en la última hora
    3. Número de llamadas al endpoint `bye` en la última hora
    4. Número total de reinicios del pod
    5. Número de llamadas al endpoint `health` en la última hora
    6. Número de llamadas al endpoint `riseload` en la última hora

- 4 Graficos temporales
    1. POD CPU: Consumo Vs Limite
    2. POD CPU: % usado
    3. Uso de RAM vs Ram reservada
    4. Reinicios totales del pod (*)

CAPTURACAPTURACAPTURACAPTURA


> (*) Este último gráfico está puesto para poder tener referencia visual rápida de si se producen reinicios en momentos de load o de uso de RAM.


- preparar y ejecutar el entorno de estress

Antes de continuar debo explicar que en ninguna de mis pruebas he podido realizar los procesos de estrés con el comportamiento realmente deseado.

> El límite de CPU en ningún momento se ha rebasado en mi entorno. En el peor de los casos acababa reiniciandose el contenedor sin que las alertas salten.
>
Para las pruebas de estrés he utilizado **dos sistemas** que utilizan el mismo principio de generar load desde el propio servidor. 

Uno es la aplicación en go incluida en la práctica, el otro es una librería de python que es la que utilizo en el código para el endpoint `/riseload` aunque como mejor funciona es desde la linea de comandos.

**Tampoco se supera siempre el límite de memoria con la aplicación.**

Esto me ha hecho dar muchas vueltas, realizar muchas pruebas y estar estancado hasta el punto de consultarte directamente.

> He generado imágenes con distinta base (con distinto sistema operativo) para descartar que fuera algo relacionado con la imagen base

Igual depende de mi entorno de ejecución o igual de mi código. 
 
A otros compañeros *les han funcionado expresiones de prometheus que en mi entorno no han funcinando*, por ejemplo.
 
Por ese motivo, porque no superaba el límite de CPU en ningún caso, no he podido comprobar el funcionamiento deseado en la alarma que avisa al superar el límite de CPU que está programada e incluida en la práctica entregada.
 
Por lo tanto he duplicado la alarma que debía de avisar en ese caso para que con el mismo comando pero cambiando el límite de la alarma avise al 80% de uso de CPU en el pod y poder así comprobar que la alarma está correctamente planteada y funciona.
 
En mis pruebas las alarmas de CPU al 80% y la de memoria si que se disparan.


Ahora si, continúo

Lo primero es acceder al pod:

`kubectl exec  -it -n fast-api $(kubectl get pod -n fast-api --no-headers | cut -d' ' -f1)  -- bash`

Una vez dentro puedes utilizar dos sistemas para generar load:

1. Librería de python

Es la librería que se emplea en el endpoint `/riseload` 

La idea inicial era no tener que instalar la herramienta en GO y que se pudiera ejecutar desde el navegador pero desde el código no termina de funcionar igual de bien que desde la linea de comandos.

Para ejecutar la librería puedes utilizar este comando desde la consola del contenedor:

```
python -m cpu_load_generator -d 120 -c -1 -l 0.9
```

Este método sin embargo no termina de consumir RAM y no afecta a la alerta de memoria.

2. Aplicación en GO

Ejecuta los siguientes comandos para preparar la aplicación:
```
apt install -y git golang && 
git clone https://github.com/jaeg/NodeWrecker.git && 
cd NodeWrecker && go build -o extress main.go
```

Para ejecutar la prueba de estress:

`./extress -abuse-memory -threads=10 -max-duration 10000000`

Este método si que hace saltar la alerta de memoria.


- adicional/final 

Como comentaba en el punto anterior *la aplicación tiene incluido un endpoint que genera un incremento de load*.

Si bien esta herramienta no ha terminado de funcionar del modo deseado para realizar la práctica con ella únicamente, si que nos sirve para hacer una última prueba en el laboratorio a modo de cierre del mismo.


Una vez se ha revisado el funcionamiento del panel y que salta alguna de las alarmas se puede realizar el descenso de uso de recursos aprovechando el endpoint `/riseload`

Si se accede mientras el uso de los recursos es bastante alto además de mostrarse en el dashboard lo más probable es que se reinicie el pod.

Con esta acción desescala el consumo de recursos apareciendo las alarmas con el estado `RESOLVED` y se puede ver el incremento en el contador de reinicios y en el gráfico y cómo corresponde con un pico de actividad.



## Exposicion final

Detallo sobbre los puntos lo realizado en la práctica.


> *- Añadir por lo menos un nuevo endpoint a los existentes....*
>
>*- Creación de tests unitarios ...*

CAPTURAS

>*- Creación de helm chart para desplegar la aplicación en Kubernetes*

He utilizado la plantilla del laboratorio 3 y le he quitado todo lo relacionado con Mongo y HPA para dejarlo lo más ceñido posible a la aplicación realizada.

Se encuentra en la carpeta `fast-api-webapp/` del repositorio.

>*- Creación de pipelines de CI/CD en cualquier plataforma...*
>
>*- Testing: tests unitarios con cobertura*    

    CAPTURA TEST GITHUB

>*- Build & Push: creación de imagen docker y push de la misma...*

    CAPTURA BUILD Y PUSH DESDE GITHUB

>*- Configuración de monitorización y alertas:*
>
>- *Configurar monitorización mediante prometheus en los nuevos endpoints añadidos...*

Se ha añadido en el código de la aplicación un contador para cada endpoint y para que aumente el contador global ne cada acceso a los nuevos endpoints.

>*- Desplegar prometheus a través de Kubernetes mediante minikube y configurar alert-manager para por lo menos las siguientes alarmas, tal y como se ha realizado en el laboratorio del día 3 mediante el chart kube-prometheus-stack:*
>
>    *- Uso de CPU de un contenedor mayor al del límite configurado, se puede utilizar como base el ejemplo utilizado en el laboratorio 3 para mandar alarmas cuando el contenedor de la aplicación fast-api consumía más del asignado mediante request*
>
>   *Las alarmas configuradas deberán tener severity high o critical*





> *- Crear canal en slack <nombreAlumno>-prometheus-alarms y configurar webhook entrante para envío de alertas con alert manager*
>
> *- Alert manager estará configurado para lo siguiente:*
>    *- Mandar un mensaje a Slack en el canal configurado en el paso anterior con las alertas con label "severity" y "critical"*
        
        
>*Deberán enviarse tanto alarmas como recuperación de las mismas*
>*Habrá una plantilla configurada para el envío de alarmas*

> *Para poder comprobar si esta parte funciona se recomienda realizar una prueba de estres, como la realizada en el laboratorio 3 a partir del paso 8.*

> *Creación de un dashboard de Grafana, con por lo menos lo siguiente:*
> *- Número de llamadas a los endpoints*
> *- Número de veces que la aplicación ha arrancado*


## Entregables

Se deberá entregar mediante un repositorio realizado a partir del original lo siguiente:

- Código de la aplicación y los tests modificados
- Ficheros para CI/CD configurados y ejemplos de ejecución válidos
- Ficheros para despliegue y configuración de prometheus de todo lo relacionado con este, así como el dashboard creado exportado a `JSON` para poder reproducirlo
- `README.md` donde se explique como se ha abordado cada uno de los puntos requeridos en el apartado anterior, con ejemplos prácticos y guía para poder reproducir cada uno de ellos