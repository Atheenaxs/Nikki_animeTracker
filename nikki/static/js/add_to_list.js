function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.add-to-list-btn').forEach(button => {
    const isAuthenticated = button.dataset.authenticated === "true";

    if (!isAuthenticated) {
      button.addEventListener('click', () => {
        window.location.href = "/login";
      });
      return; // ne met pas d'autres événements si non connecté
    }

    // Si connecté, gérer l'ouverture du menu au survol
    const menu = button.nextElementSibling;

    button.addEventListener('mouseenter', () => {
      menu.classList.remove('hidden');
    });

    button.addEventListener('mouseleave', () => {
      setTimeout(() => {
        if (!menu.matches(':hover')) {
          menu.classList.add('hidden');
        }
      }, 150);
    });

    menu.addEventListener('mouseleave', () => {
      menu.classList.add('hidden');
    });
  });

  document.querySelectorAll('.list-option').forEach(option => {
    option.addEventListener('click', () => {
      const animeCard = option.closest('.poster-card');
      const animeId = animeCard.dataset.animeId;
      const title = animeCard.querySelector('h3').innerText;
      const imageUrl = animeCard.querySelector('img').src;
      const status = option.dataset.status;

      fetch('/add-to-list/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
          anime_id: animeId,
          title: title,
          image_url: imageUrl,
          status: status
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert("Ajouté à votre liste !");
        } else {
          alert("Erreur : " + (data.error || "inconnue"));
        }
      });
    });
  });
});
