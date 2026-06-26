import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        genre = self._model.getAllGenres()
        for n in genre:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(data=n, key=str(n), on_click=self._choiceGenre)
            )

        self._view.update_page()

    def _choiceGenre(self,e):
        self._genreValue = e.control.key

    def handleCreaGrafo(self, e):
        genre = self._view._ddGenre.value
        if genre is None:
            self._view.create_alert("Seleziona un genere musicale.")
            self._view.update_page()
            return

        self._model.buildGraph(genre)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato per il genere '{genre}'."))
        self._view.txt_result.controls.append(
            ft.Text(f"# vertici: {self._model.getNumNodes()}  -  # archi: {self._model.getNumEdges()}"))

        best, influ = self._model.getMostInfluential()
        if best is not None:
            self._view.txt_result.controls.append(
                ft.Text(f"Artista più influente: {self._model.getArtistName(best)} (influenza {influ})"))

        self._view.txt_result.controls.append(ft.Text("Top 5 archi per peso:"))
        for u, v, w in self._model.getTop5Edges():
            self._view.txt_result.controls.append(
                ft.Text(f"  {self._model.getArtistName(u)} -> {self._model.getArtistName(v)} : {w}"))

        self._view.update_page()

    def handleCammino(self,e):
        pass