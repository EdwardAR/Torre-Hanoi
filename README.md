# 🏗️ Torre de Hanoi — Python + Tkinter

Una implementación gráfica del clásico juego **Torre de Hanoi**, desarrollada en **Python** utilizando la biblioteca **Tkinter**.  
Permite jugar manualmente o ver cómo el programa resuelve el puzzle automáticamente con animaciones.

---

## 🎮 Características principales

- 🎯 **Interfaz gráfica interactiva** con visualización de torres y discos.  
- 🔢 Selección de **número de discos** (de 3 a 8).  
- 🔁 **Reinicio rápido** del juego en cualquier momento.  
- 🧠 **Modo automático** que muestra la solución paso a paso.  
- ⚖️ **Validación de movimientos** (no se permite colocar discos grandes sobre pequeños).  
- 🧾 **Contador de movimientos** actualizado en tiempo real.  
- 🏆 **Mensaje de victoria** al completar correctamente el desafío.

<center>
    <img width="657" height="462" alt="image" src="https://github.com/user-attachments/assets/5f34a68e-b654-4562-8bfb-28ffb3e20365" />
</center>

---

## 🧩 Estructura del código

El código se organiza en una clase principal y varios métodos que gestionan tanto la lógica del juego como la interfaz gráfica:

### 📦 Clase `HanoiGame`
Contiene toda la lógica del juego y la gestión de la interfaz.

#### Métodos destacados:
- `create_towers()` → Dibuja las tres torres en el lienzo.  
- `create_disks()` → Genera los discos con colores y tamaños dinámicos.  
- `on_click(event)` → Gestiona la selección y movimiento de discos.  
- `move_disk()` → Actualiza la posición de los discos entre torres.  
- `check_win()` → Verifica si el jugador ha completado el juego.  
- `start_autosolve()` → Ejecuta la resolución automática mediante recursión.  
- `reset_game()` → Reinicia el tablero y el contador de movimientos.

---

## 🧠 Lógica de resolución

El método `start_autosolve()` utiliza un enfoque **recursivo** basado en el algoritmo clásico de la **Torre de Hanoi**:

```python
def hanoi_moves(k, src, dst, aux):
    if k == 0:
        return
    hanoi_moves(k - 1, src, aux, dst)
    moves.append((src, dst))
    hanoi_moves(k - 1, aux, dst, src)
