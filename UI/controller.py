import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        genre = self._model.getAllGenres()
        genresDDOptions = list(
            map(lambda x: ft.dropdown.Option(data=x, key=x.genre_name, on_click=self._choiceGenre), genre))

        self._view._ddGenre.options = categoriesDDGenre

        self._view.update_page()

    def _choiceGenre(self,e):
        self._genreValue = e.get_attribute('value')

    def handleCreaGrafo(self, e):
        pass

    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass