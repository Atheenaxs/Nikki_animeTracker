import pytest
from playwright.sync_api import Page

BASE_URL = "http://localhost:8000"

@pytest.mark.django_db
def test_genre_menu_appears_on_hover(live_server, page: Page):
    page.goto(live_server.url + "/")
    
    # Surligne le bouton "Genres"
    genres_trigger = page.locator("a:text('Genres')")
    genres_trigger.hover()

    # Attends que le menu apparaisse
    dropdown = page.locator("ul >> text=Action")  # ou autre genre que tu sais présent
    dropdown.wait_for(state="visible", timeout=2000)

    # Vérifie que le lien est visible
    assert dropdown.is_visible()
