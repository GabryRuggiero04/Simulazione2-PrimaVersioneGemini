import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenere(self):
        allGenere = self._model.getAllGenere()
        for o in allGenere:
            self._view._ddGenere.options.append(
                ft.dropdown.Option(text=o)
            )


    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        if self._view._ddGenere.value is None:
            self._view.create_alert("Selezionare da menù a tendina")
            return
        genere =  self._view._ddGenere.value
        self._model.buildGraph(genere)
        grafo = self._model.getGraph()
        if len(grafo.nodes()) < 1:
            self._view.txt_result.controls.append(
                ft.Text(f"Grafo vuoto o creato in modo errato", color="red")
            )
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato correttamente", color="green")
        )
        numNodes, numEdges = self._model.detailGraph()
        self._view.txt_result.controls.append(
            ft.Text(f"Numero nodi: {numNodes}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero archi: {numEdges}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"I nodi isolati sono: ", color="green")
        )
        lista= self._model.edgesIsolati()
        for n in lista:
            self._view.txt_result.controls.append(
                ft.Text(n)
            )
        allNodes = list(grafo.nodes())
        for o in allNodes:
            self._view._ddAttore.options.append(
                ft.dropdown.Option(data=o,
                                   text=o.name,
                                   key=o.id,
                                   on_click=self.choiceObject)
            )
        self._view.update_page()

    def choiceObject(self, e):
        self._ObjectSelectedValue = e.control.data
        return self._ObjectSelectedValue



    def handleCammino(self, e):
        self._view.txt_result.controls.clear()
        nodoInizio = self._ObjectSelectedValue
        if self._view._ddAttore.value is None:
            self._view.create_alert("Scegliere partenza!!")
            return
        bestPath, bestLen = self._model.getPath(nodoInizio)
        if len(bestPath) == 0:
            self._view.txt_result.controls.append(
                ft.Text("nessun cammino esistente con questi input", color="red")
            )
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino trovato: ", color="green")
        )
        for n in bestPath:
            self._view.txt_result.controls.append(
                ft.Text(n)
            )
        self._view.update_page()