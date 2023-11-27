# 1. Napisać klasę Graph - wierzchołkami mogą być dowolne obiekty niemodyfikowalne(wszystko
# co może być kluczem słownika). Klasa  powinna umożliwiać dodanie wierzchołka, usunięcie
# wierzchołka(razem ze wszystkimi przyległymi krawędziami), dodanie krawędzi, usunięcie
# krawędzi, pobranie wszystkich sąsiadów wskazanego wierzchołka.
#
# 2. Napisać metody bfs i dfs, przyjmujące wierzchołek, z którego chcemy
# zacząć przeglą grafu i pozwalające na iterację wszerz i wgłąb.
# Przykładowe użycie: for vertex in graph.dfs(root):
#
# Uwaga: metody nie mają zwracać listy ani krotki, tylko iterator (metody _iter_ i _next_).

class Graph:
    def __init__(self):
        self.wierzcholki = {}

    def add_wierz(self, wierz):  # polglish
        self.wierzcholki[wierz] = set()  # czemu nie defaultdict?

    def remove_wierz(self, wierz):
        del self.wierzcholki[wierz]
        for w in self.wierzcholki:  # czy trzeba odwiedzać wszystkie wierzchołki w poszukiwaniu krawędzi do usuwanego?
            self.wierzcholki[w].discard(wierz)

    def add_kraw(self, w1, w2):
        self.wierzcholki[w1].add(w2)
        self.wierzcholki[w2].add(w1)

    def remove_kraw(self, w1, w2):
        self.wierzcholki[w1].discard(w2)
        self.wierzcholki[w2].discard(w1)

    def get_neighbors(self, wierz):
        return iter(self.wierzcholki[wierz])

    def BFS(self, start_wierz):
        visited = set()
        queue = [start_wierz]

        while queue:
            obecny_wierz = queue.pop(0)
            if obecny_wierz not in visited:
                yield obecny_wierz
                visited.add(obecny_wierz)
                queue.extend(self.wierzcholki[obecny_wierz] - visited)

    def DFS(self, start_wierz):
        visited = set()
        stack = [start_wierz]

        while stack:
            obecny_wierz = stack.pop()
            if obecny_wierz not in visited:
                yield obecny_wierz
                visited.add(obecny_wierz)
                stack.extend(self.wierzcholki[obecny_wierz] - visited)


# Budowanie grafu - dodanie wierzcholkow i relacji miedzy nimi jako krawedzi
graph = Graph()
graph.add_wierz("a")
graph.add_wierz("b")
graph.add_wierz("c")
graph.add_wierz("d")
graph.add_wierz("e")
graph.add_kraw("a", "b")
graph.add_kraw("a", "c")
graph.add_kraw("b", "e")
graph.add_kraw("c", "d")

# Sprawdzenie dzialania BFS i DFS

print("BFS:")
for wierzcholek in graph.BFS("a"):
    print(wierzcholek)
# zwraca a c b d e

print("\nDFS:")
for wierzcholek in graph.DFS("a"):
    print(wierzcholek)
# zwraca a b e c d