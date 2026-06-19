# Sistema de Gestión Automatizada de Turnos (Consultorio Psicológico)

Este proyecto ha sido desarrollado para la cátedra **Organización Empresarial** de la Tecnicatura Universitaria en Programación (TUP) - UTN. Consiste en un chatbot conversacional interactivo diseñado bajo una Máquina de Estados Finitos que automatiza el proceso administrativo de asignación de turnos, integrando persistencia de datos y control de robustez ante errores de entrada.

## 🚀 Requisitos y Configuración del Entorno

El sistema está desarrollado íntegramente en **Python 3** y no requiere la instalación de librerías externas complejas, utilizando el módulo nativo `csv` para garantizar un despliegue ágil y portable.

### Pasos para el Despliegue Local:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/fdmuinos/UTN-TUPaD-OE-TPI.git
   cd UTN-TUPaD-OE-TPI
2. **Verificar la estructura del proyecto:**
Asegurarse de que el archivo de base de datos turnos.csv se encuentre en la raíz del proyecto.

3. **Ejecutar el simulador del Chatbot:**
Inicie el bucle interactivo ejecutando el archivo principal desde la terminal:
   ```bash
   python src/main.py

## Arquitectura implementada
- main.py: Interfaz de entrada por consola que simula el entorno de mensajería.

- bot.py: Motor conversacional y máquina de estados. 

- database.py: Implementa funciones de lectura y escritura sobre el archivo para guardar la información y validar la disponibilidad de la agenda.

- turnos.csv: Archivo de datos que funciona como base de datos del consultorio.
