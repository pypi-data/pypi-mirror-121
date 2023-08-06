from setuptools import setup, find_packages, version

setup(
    name= 'PYPIPPACKAGEEXAMPLE',
    version= '1.1',
    license= 'MIT',
    description= 'Paquete de prueba para una clase de Udemy',
    author= 'Stefano Berro',
    packages= find_packages(), #sirve para poder encontrar los paquetes internos
    #install_requires= ['math','numpy'], #Se usa para cuando se deben instalar librerías adicionales
    url= 'https://github.com/Stefanoberro/pypipackageexample'
)