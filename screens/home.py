import flet as ft

def home_view(page: ft.Page):
    search = ft.TextField(label="Buscar libro", width=300)
    resultado = ft.Text()

    def on_search_click(e):
        # Aquí pondrás tu lógica para buscar libros (API o mock)
        resultado.value = f"Resultados para: {search.value}"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Bienvenido a la Biblioteca Digital", size=20),
            search,
            ft.ElevatedButton("Buscar", on_click=on_search_click),
            resultado
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
