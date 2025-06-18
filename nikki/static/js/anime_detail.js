document.addEventListener("DOMContentLoaded", () => {
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
  const animeId = window.location.pathname.split("/").filter(Boolean).pop();

  const addBtn = document.getElementById("add-to-list-button");
  const listMenu = document.getElementById("list-menu");
  const removeBtn = document.getElementById("remove-from-list");
  const loginModal = document.getElementById("loginModal");

  const isAuthenticated = window.isAuthenticated === true;


  // --- Gérer ajout à une liste
  if (addBtn && listMenu) {
    const menuWrapper = document.getElementById("menu-wrapper");

    addBtn.addEventListener("click", () => {
      if (!isAuthenticated) {
        if (loginModal) {
          loginModal.classList.remove("hidden");
        } else {
          alert("Erreur : modal de connexion introuvable.");
        }
        return;
      }
      listMenu.classList.remove("hidden");
    });

    menuWrapper.addEventListener("mouseleave", () => {
      listMenu.classList.add("hidden");
    });

    listMenu.querySelectorAll(".list-option").forEach(option => {
      option.addEventListener("click", () => {
        const status = option.dataset.status;
        const title = document.querySelector("h1").innerText;
        const imageUrl = document.querySelector(".anime-cover")?.src || "";

        fetch("/add-to-list/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
          },
          body: JSON.stringify({
            anime_id: animeId,
            title,
            image_url: imageUrl,
            status
          })
        })
          .then(res => res.json())
          .then(data => {
            if (data.success) {
              window.location.reload();
            } else {
              alert("Erreur : " + (data.error || "inconnue"));
            }
          });
      });
    });
  }

  // --- Gérer suppression de l’anime
  if (removeBtn) {
    removeBtn.addEventListener("click", () => {
      const userAnimeId = removeBtn.dataset.userAnimeId;
      fetch(`/remove-anime/${userAnimeId}/`, {
        method: "POST",
        headers: { "X-CSRFToken": csrftoken }
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            window.location.reload();
          } else {
            alert("Erreur lors de la suppression");
          }
        });
    });
  }

  // --- Gérer coche/décoche d’épisodes
  document.querySelectorAll(".episode-checkbox").forEach(cb => {
    cb.addEventListener("change", async () => {
      const episodeId = cb.dataset.episodeId;
      const response = await fetch(`/toggle-episode/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ episode_id: episodeId, watched: cb.checked })
      });

      response.ok ? window.location.reload() : alert("Erreur MAJ épisode");
    });
  });
});