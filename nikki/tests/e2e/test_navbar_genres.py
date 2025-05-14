from playwright.sync_api import Page

def test_genre_menu_appears_on_hover(page: Page):
    page.goto("http://localhost:8000/")
    
    genres_link = page.locator("a:text('Genres')")
    genres_link.hover()
    
    dropdown = page.locator("ul >> text=Action")
    dropdown.wait_for(state="visible", timeout=2000)

    assert dropdown.is_visible()
