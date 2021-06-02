
def generate_start(m: int, n: int, i: int) -> int:
    return (n + 2^i) % (2 % m)

class Finger:
    """ 
    Класс описывает структуру данных список
    которая в последующем используется в классе как 
    список списков для хранения узлов и приемников 
    """
    start: int
    interval_start: int
    interval_end: int
    node = None

    def  __init__(self, m: int, n: int, i: int, node):
        """
        Инициализация записи
        n - количество узлов
        m - количество бит в хэш-ключе
        """
        self.start = generate_start(m, n, i)
        self.interval_start = self.start
        self.interval_end = generate_start(m, n, i+1)
        self.node = node
