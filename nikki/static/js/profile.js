document.getElementById("openSettings").onclick = () => {
    document.getElementById("settingsPanel").classList.remove("translate-x-full");
  };
  document.getElementById("closeSettings").onclick = () => {
    document.getElementById("settingsPanel").classList.add("translate-x-full");
  };

document.addEventListener("DOMContentLoaded", () => {
  const profileForm = document.getElementById("profileForm");
  const successMsg = document.getElementById("profileSuccess");
  const errorMsg = document.getElementById("profileError");

  // Update profile AJAX
  profileForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData(profileForm);

    const response = await fetch("{% url 'profil' %}", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    });

    if (response.ok) {
      successMsg.classList.remove("hidden");
      errorMsg.classList.add("hidden");
    } else {
      successMsg.classList.add("hidden");
      errorMsg.classList.remove("hidden");
    }
  });

  // Supprimer mes données (RGPD)
  document.getElementById("deleteDataBtn").addEventListener("click", async () => {
    const confirmed = confirm("Supprimer toutes vos données personnelles ?");
    if (!confirmed) return;

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const response = await fetch("{% url 'delete_data' %}", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
    });

    if (response.ok) {
      alert("Données supprimées.");
      location.reload();
    }
  });

  // Supprimer le compte
  document.getElementById("deleteAccountBtn").addEventListener("click", async () => {
    const confirmed = confirm("Êtes-vous sûr de vouloir supprimer votre compte ?");
    if (!confirmed) return;

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const response = await fetch("{% url 'delete_account' %}", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
    });

    if (response.ok) {
      alert("Compte supprimé. À bientôt...");
      location.href = "{% url 'home' %}";
    }
  });
});
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.anime-status-select').forEach(select => {
    select.addEventListener('change', () => {
      const userAnimeId = select.dataset.userAnimeId;
      const newStatus = select.value;

      fetch('/ajax/change-anime-status/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
          user_anime_id: userAnimeId,
          new_status: newStatus
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          location.reload();  // <-- Recharge la page automatiquement
        } else {
          alert("Erreur : " + (data.error || "inconnue"));
        }
      })
      .catch(error => {
        alert("Erreur réseau");
        console.error(error);
      });
    });
  });
});
