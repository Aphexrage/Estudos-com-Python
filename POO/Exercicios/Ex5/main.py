from Item import Item
from Carrinho import Carrinho

carrinho = Carrinho()

item1 = Item("Item1", 100)
item2 = Item("Item2", 200)
item3 = Item("Item3", 300)

carrinho.adicionar_item(item1)
carrinho.adicionar_item(item2)
carrinho.adicionar_item(item3)

print("Total:", carrinho.total())

carrinho.remover_item(item2)

print("Total após remover item2:", carrinho.total()) 
