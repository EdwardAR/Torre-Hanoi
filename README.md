🏗️ Torre de Hanoi en Python (Tkinter)

Este proyecto implementa el clásico juego de la Torre de Hanoi utilizando la biblioteca Tkinter para crear una interfaz gráfica interactiva.

🎮 Descripción general

El programa permite al usuario jugar manualmente o ver una resolución automática del rompecabezas.
Incluye controles para seleccionar la cantidad de discos (de 3 a 8), reiniciar la partida y contar los movimientos realizados.

🧩 Características principales

Interfaz gráfica con canvas para visualizar las tres torres y los discos.

Control del número de discos mediante un Spinbox.

Contador dinámico de movimientos.

Posibilidad de auto-resolver el juego con animación paso a paso.

Validación de movimientos (no se permite colocar discos grandes sobre pequeños).

Mensajes informativos al ganar o realizar acciones inválidas.

⚙️ Componentes del código

Clase HanoiGame: Contiene toda la lógica del juego y la interfaz.

create_towers() y create_disks(): Dibujan las torres y los discos.

on_click(): Gestiona la selección y movimiento de discos.

move_disk(): Actualiza la posición del disco seleccionado.

start_autosolve(): Ejecuta y anima la solución automática.

reset_game(): Reinicia el tablero.

Método hanoi_moves(): Genera recursivamente la secuencia de movimientos para resolver el puzzle.

Ejecución principal: Crea la ventana principal y lanza el juego (root.mainloop()).

🖥️ Ejecución

Para ejecutar el programa:

python hanoi_game.py


Se abrirá una ventana donde podrás:

Seleccionar el número de discos.

Moverlos manualmente con clics.

Ver la solución automática.
