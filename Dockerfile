FROM jupyter/pyspark-notebook:spark-3.3.1

# Instalar Delta Lake usando pip
RUN pip install delta-spark==2.2.0

# Copiar el notebook al contenedor
COPY pipline.ipynb /home/jovyan/work/

# Establecer el directorio de trabajo
WORKDIR /home/jovyan/work

# Comando para ejecutar Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]