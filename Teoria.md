# Teoría de Agentes y "Tool Calling" en LangChain

Este documento explica los conceptos fundamentales detrás del proyecto `AI Math Assistant`, basado en el uso de LangChain con modelos de lenguaje (LLMs) como Ollama (Llama 3.1).

## 1. ¿Qué es "Tool Calling"?

En inteligencia artificial, **"Tool Calling" (o llamada a herramientas)** es la capacidad de un modelo de lenguaje (LLM) para reconocer cuándo no puede responder a una pregunta basándose solo en su entrenamiento y, en su lugar, decide utilizar una "herramienta" externa.

*   **Sin Tool Calling**: Si preguntas "¿Cuánto es 34523 * 1.23?", el LLM adivina la respuesta basándose en predicciones estadísticas (a menudo incorrectas).
*   **Con Tool Calling**: El LLM reconoce que es un problema matemático, selecciona la herramienta `multiply_numbers`, le envía los datos, recibe el resultado exacto y te lo comunica.

### Principios clave
1.  **Propósito claro**: Cada herramienta debe tener una única función específica.
2.  **Input estandarizado**: Las herramientas deben aceptar datos en formatos predecibles (texto, listas, JSON).
3.  **Output consistente**: Los resultados deben ser fáciles de "leer" para el agente.
4.  **Documentación**: El LLM lee el `docstring` de la función (su manual) para saber cómo y cuándo usarla.

---

## 2. ¿Qué es un Agente?

Un **Agente** es el "cerebro" que orquesta la interacción entre el usuario, el LLM y las herramientas. No es solo un chatbot; es un sistema que toma decisiones.

### Relación Agente-LLM
*   **Agente**: Es el gestor. Decide qué pasos tomar.
*   **LLM**: Es el motor de razonamiento. Interpreta lo que dice el usuario y aconseja al agente qué herramienta usar.

### Ciclo ReAct (Reason + Act)
El framework utilizado en este proyecto (a través de `create_react_agent`) sigue el ciclo **ReAct**:
1.  **Pensar (Reason)**: El agente analiza la solicitud ("El usuario quiere sumar dos números").
2.  **Actuar (Act)**: Decide usar una herramienta (`add_numbers`) con argumentos específicos.
3.  **Observar (Observe)**: Ejecuta la herramienta y ve el resultado real (`30`).
4.  **Responder**: Formula la respuesta final al usuario basándose en la observación.

---

## 3. Implementación Técnica en LangChain

Este proyecto utiliza componentes modernos de LangChain (v0.2/v0.3):

### A. Definición de Herramientas (`@tool`)
Usamos el decorador `@tool` para convertir funciones de Python en herramientas.

```python
@tool
def add_numbers(inputs) -> dict:
    """Adds a list of numbers..."""
    # Lógica de la herramienta
```
El texto dentro de `"""..."""` es crucial: es lo que lee la IA para entender la herramienta.

### B. El problema de los Tipos de Datos (Parsing)
Uno de los mayores desafíos en Tool Calling es que los LLMs a veces envían los datos como texto (`"10, 20"`) y otras veces como estructuras (`[10, 20]`).
*   **Solución**: Implementamos una función `extract_numbers()` que normaliza cualquier entrada a una lista de números `float` antes de operar.

### C. LangGraph (`create_react_agent`)
En versiones antiguas se usaba `initialize_agent`. Ahora usamos **LangGraph**, que crea un grafo de decisiones más robusto.
*   **Agent Node**: Llama al LLM.
*   **Tools Node**: Ejecuta el código Python.
*   **Loop**: El agente puede llamar a varias herramientas en secuencia (ej: primero Wikipedia, luego multiplicar) hasta resolver el problema.
