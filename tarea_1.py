#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1. Desarrolla un entorno similar al de los dos cuartos (el cual se
   encuentra en el módulo doscuartos_o.py), pero con tres cuartos en
   el primer piso, y tres cuartos en el segundo piso.
   
   El entorno se llamará `SeisCuartos`.

   Las acciones totales serán
   
   ```
   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   ``` 
    
   La acción de `"subir"` solo es legal en el piso de abajo, en los cuartos de los extremos, 
   mientras que la acción de `"bajar"` solo es legal en el piso de arriba y en el cuarto de el centro (dos
   escaleras para subir, una escalera para bajar).

   Las acciones de subir y bajar son mas costosas en término de
   energía que ir a la derecha y a la izquierda, por lo que la función
   de desempeño debe de ser de tener limpios todos los cuartos, con el
   menor numero de acciones posibles, y minimizando subir y bajar en
   relación a ir a los lados. El costo de limpiar es menor a los costos
   de cualquier acción.

2. Diseña un Agente reactivo basado en modelo para este entorno y
   compara su desempeño con un agente aleatorio despues de 100 pasos
   de simulación.

3. Al ejemplo original de los dos cuartos, modificalo de manera que el
   agente solo pueda saber en que cuarto se encuentra pero no sabe si
   está limpio o sucio.

   A este nuevo entorno llamalo `DosCuartosCiego`.

   Diseña un agente racional para este problema, pruebalo y comparalo
   con el agente aleatorio.

4. Reconsidera el problema original de los dos cuartos, pero ahora
   modificalo para que cuando el agente decida aspirar, el 80% de las
   veces limpie pero el 20% (aleatorio) deje sucio el cuarto. Igualmente, 
   cuando el agente decida cambiar de cuarto, se cambie correctamente de cuarto el 90% de la veces
   y el 10% se queda en su lugar. Diseña
   un agente racional para este problema, pruebalo y comparalo con el
   agente aleatorio.

   A este entorno llámalo `DosCuartosEstocástico`.

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = 'Rolando Velez'

from random import choice

class Environment:
    def __init__(self, x0=[]):
        self.x = x0[:]
        self.performance = 0

    def legal_action(self, action):
        return True

    def transition(self, action):
        pass
    
    def percepts(self):
        return self.x

class Agent(object):
    def program(self, percepts):
        pass
    
def simulator(env, agent, steps=10, verbose=True):
    performance_history = [env.performance]
    state_history = [env.x[:]]
    action_history = []

    for step in range(steps):
        p = env.percepts()
        a = agent.program(p)
        env.transition(a)

        performance_history.append(env.performance)
        state_history.append(env.x[:])
        action_history.append(a)

    action_history.append(None)

    if verbose:
        print(u"\n\nEnvironment Simulation of type " +
                str(type(env)) +
                " with an Agent of type " +
                str(type(agent)) + "\n")

        print('Step'.center(10) +
                'State'.center(40) +
                u'Action'.center(25) +
                u'Performance'.center(15))

        print('_' * (10 + 40 + 25 + 15))

        for i in range(steps):
            print(str(i).center(10) +
                    str(state_history[i]).center(40) +
                    str(action_history[i]).center(25) +
                    str(performance_history[i]).rjust(12))

        print('_' * (10 + 40 + 25 + 15) + '\n\n')

    return state_history, action_history, performance_history

class SixRooms(Environment):
    """
        Six Rooms.                                  _____________
        2 Floors, 3 rooms each floor.               | D | E | F |
        Can only go up on room "A" or "C".          | A | B | C |
        Can only go down on room "E".               -------------
        Actions to perform can only be ["go_right", "go_left", "go_up", "go_down", "suck", "noop"]
    """
    def __init__(self, x0=["A", "dirty", "dirty", "dirty", "dirty", "dirty", "dirty"]):
        
        self.x = x0[:]
        self.performance = 0

    def legal_action(self, action):
       """
            Check if the action the robot wants to perform is legal in the current state.
       """
       if self.x[0] == "A":
           return action in ("go_right", "go_up", "suck", "noop")
       elif self.x[0] == "B":
           return action in ("go_right", "go_left", "suck", "noop")
       elif self.x[0] == "C":
           return action in ("go_left", "go_up", "suck", "noop")
       elif self.x[0] == "D":
           return action in ("go_right", "suck", "noop")
       elif self.x[0] == "E":
           return action in ("go_right", "go_left", "go_down", "suck", "noop")
       else:
           return action in ("go_left", "suck", "noop")
    
    def transition(self, action):
        """
            First it checks if the action that we want to perform is legal in it's current state.
            Instructions say that the action of "suck" is the cheapest action there is, compared to all others.
            So following that rule, we set the performance value to 1 if the robot decides to clean.
            Since the action of going up/down is more costly than all the other actions we set it's performance value at 3.
            Finally I set the performance value of going right/left to 2. (Cheaper than going up/down but higher than cleaning).
            After that there's a lot of if's statements to check where the robot is going next after performing the given action.
        """
        
        if not self.legal_action(action):
            raise ValueError("Action is illegal in the current state.")
        
        robot, a, b, c, d, e, f = self.x
        if (action is not "noop" or a is "dirty" or b is "dirty" or c is "dirty" or
                d is "dirty" or e is "dirty" or f is "dirty"):
            if action is "go_up" or action is "go_down":
                self.performance -= 3
            elif action is "suck":
                self.performance -= 1
            else:
                self.performance -= 2
        if action is "suck":
            self.x[" ABCDEF".find(self.x[0])] = "clean"
        elif action is "go_right":
            if self.x[0] == "A":
                self.x[0] = "B"
            elif self.x[0] == "B":
                self.x[0] = "C"
            elif self.x[0] == "D":
                self.x[0] = "E"
            elif self.x[0] == "E":
                self.x[0] = "F"
        elif action is "go_left":
            if self.x[0] == "F":
                self.x[0] = "E"
            elif self.x[0] == "E":
                self.x[0] = "D"
            elif self.x[0] == "C":
                self.x[0] = "B"
            elif self.x[0] == "B":
                self.x[0] = "A"
        elif action == "go_up":
            if self.x[0] == "A":
                self.x[0] = "D"
            else:
                self.x[0] = "F"
        elif action == "go_down":
            self.x[0] = "B"
    
    def percepts(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]
