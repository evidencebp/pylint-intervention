from cursesmenu import CursesMenu
from cursesmenu.items import SubmenuItem

menu = CursesMenu("Title", "Subtitle")
selection_menu = CursesMenu.make_selection_menu([f"item{i}" for i in range(20)])
submenu_item = SubmenuItem("Submenu item", selection_menu, menu)
menu.items.append(submenu_item)
menu.show()
