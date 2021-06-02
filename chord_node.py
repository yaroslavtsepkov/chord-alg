from __future__ import annotations
from typing import *
from finger import Finger

import random


class ChordNode:
    _id: int # id узла
    finger_table: List[Finger] # таблица 
    predecessor: ChordNode # узел

    def __init__(self, m: int, n: int):
        """
        Функция инициализация узла в системе.
        """
        self._id = n
        self.finger_table = [Finger(m, n, i, self) for i in range(m)]
        self.predecessor = self

    def get_successor(self) -> ChordNode:
        """ Возвращает successor """
        return self.finger_table[0].node

    def set_successor(self, successor: ChordNode):
        """ Присваивает полю значение succesor в таблице finger """
        self.finger_table[0].node = successor

    def find_successor(self, _id: int) -> ChordNode:
        """ Возвращает succesor найденный по id """
        return self.find_predecessor(_id).get_successor()

    def find_predecessor(self, _id: int) -> ChordNode:
        """ Поиск приемника для узла по id """
        node = self
        while not (self.id_in_range(_id, node._id, node.get_successor()._id) or _id == node.get_successor()._id):
            node = node.closest_preceding_finger(_id)

        return node

    def closest_preceding_finger(self, j: int) -> ChordNode:
        """
        поиск в локальной таблице 
        самого высокого предшественника идентификатора
        """ 
        m: int = len(self.finger_table)
        for i in range(m - 1, -1, -1):
            node: ChordNode = self.finger_table[i].node
            if self.id_in_range(node._id, self._id, j):
                return node
        return self

    def join(self, node: ChordNode):
        if node is not None:
            self.init_finger_table(node)
            self.update_others()
        else:
            for finger in self.finger_table:
                finger.node = self
            self.predecessor = self

    def init_finger_table(self, node: ChordNode):
        """ Инициалиация локальной таблицы """
        successor: ChordNode = self.get_successor()
        self.finger_table[0].node = node.find_predecessor(self.finger_table[0].start)
        self.predecessor = successor.predecessor
        successor.predecessor = self

        m: int = len(self.finger_table)
        for i in range(m - 1):
            if self._id == self.finger_table[i + 1].start or self.id_in_range(self.finger_table[i + 1].start, self._id,
                                                                              self.finger_table[i].node._id):
                self.finger_table[i + 1].node = self.finger_table[i].node
            else:
                self.finger_table[i + 1].node = node.find_successor(self.finger_table[i + 1].start)

    def update_others(self):
        """ Обновление """
        m: int = len(self.finger_table)
        for i in range(m):
            # j = _id - 2^i
            j: int = self._id - (1 << i)
            if j < 0:
                j += 1 << m
            p: ChordNode = self.find_predecessor(j)
            p.update_fingertable(self, i)

    def update_fingertable(self, s: ChordNode, i: int):
        """
        Обновление локальной таблицы
        """
        if self._id == s._id or self.id_in_range(s._id, self._id, self.finger_table[i].node._id):
            self.finger_table[i].node = s
            p: ChordNode = self.predecessor
            p.update_fingertable(s, i)

    def join2(self, node: ChordNode):
        """ Добавление узла в систему """
        if node is not None: 
            self.predecessor = None
            self.set_successor(node.find_successor(self._id))
        else:
            for finger in self.finger_table: # поиск по таблице
                finger.node = self  # записывает текущее состояние 
            self.predecessor = self 

    def stabilize(self):
        """ Стабилизация системы """
        x: ChordNode = self.get_successor().predecessor
        if self.id_in_range(x._id, self._id, self.get_successor()._id):
            self.set_successor(x)
        self.get_successor().notify(self)

    def notify(self, node: ChordNode):
        """ Проверка существования узла и вхождения его в полузакртыый интервал """
        if self.predecessor is None or self.id_in_range(node._id, self.predecessor._id, self._id):
            self.predecessor = node

    def fix_fingers(self):
        """ Изменение данных в таблице """
        i: int = random.randrange(len(self.finger_table))
        self.finger_table[i].node = self.find_successor(self.finger_table[i].start)

    def find_by_id(self, i: int) -> Optional[ChordNode]:
        """
        Поиск по id в таблице finge
        """
        node: ChordNode = self
        visited: set = set()
        while node._id != i:
            visited.add(node)
            for finger in self.finger_table:
                if i == finger.node._id:
                    return finger.node
                if finger.interval_start == i or self.id_in_range(i, finger.start, finger.interval_end):
                    node = finger.node
            if node in visited:
                return None
        return node

    def _delete(self):
        self.predecessor.set_successor(self.get_successor())
        self.get_successor().predecessor = self.predecessor

        m: int = len(self.finger_table)
        for i in range(m):
            j: int = self._id - (1 << i)
            if j < 0:
                j += 1 << m
            p: ChordNode = self.find_predecessor(j)
            p.update_fingertable(self.get_successor(), i)

    def id_in_range(self, i: int, a: int, b: int) -> bool:
        """ 
        Вспомогательная функция для проверки вхождения узла 
        с id в полуинтервал  
        """
        end: int = b
        ii: int = i
        m: int = len(self.finger_table)

        if a >= b:
            end += 1 << m
            if a > i:
                ii += 1 << m

        return a < ii and ii < end

    def __repr__(self):
        """ 
        Визуализация таблицы для каждого из узла
        """ 
        res: str = ""
        res += f"id\t:\t{self._id}\n"
        res += f"|\tstart\t|\tinterval\t|\tnode\t|"
        res += "\n"
        res += "#####"*9
        res += "\n"
        for finger in self.finger_table:
            res += f"|\t{finger.start}\t|\t[{finger.interval_start}, {finger.interval_end})\t        |\t{finger.node._id}\t|\n"
        res += "#####"*9
        return res
