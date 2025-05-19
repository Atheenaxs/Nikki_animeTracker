document.addEventListener("DOMContentLoaded", () => {
  const loginModal = document.getElementById("loginModal");
  const signupModal = document.getElementById("signupModal");
  const loginBtn = document.getElementById("loginBtn");
  const signupBtn = document.getElementById("signupBtn");
  const closeLoginModal = document.getElementById("closeLoginModal");
  const closeSignupModal = document.getElementById("closeSignupModal");
  const loginOverlay = document.getElementById("loginModalOverlay");
  const signupOverlay = document.getElementById("signupModalOverlay");
  const switchToLogin = document.getElementById("switchToLogin");
  const switchToSignup = document.getElementById("switchToSignup");
  const startNow = document.getElementById("startNow");
  const ctaSignup = document.getElementById("ctaSignup");
  const signupForm = document.getElementById("signupForm");

  // Gestion de l'ouverture des modaux
  if (loginBtn) loginBtn.onclick = () => loginModal.classList.remove("hidden");
  if (signupBtn) signupBtn.onclick = () => signupModal.classList.remove("hidden");
  if (startNow) startNow.onclick = () => {
    signupModal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  };
  if (ctaSignup) ctaSignup.onclick = () => {
    signupModal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  };

  // Fermeture des modaux
  if (closeLoginModal) closeLoginModal.onclick = () => loginModal.classList.add("hidden");
  if (closeSignupModal) closeSignupModal.onclick = () => signupModal.classList.add("hidden");
  if (loginOverlay) loginOverlay.onclick = () => loginModal.classList.add("hidden");
  if (signupOverlay) signupOverlay.onclick = () => signupModal.classList.add("hidden");

  // Passage entre les modaux
  if (switchToLogin) {
    switchToLogin.onclick = (e) => {
      e.preventDefault();
      signupModal.classList.add("hidden");
      loginModal.classList.remove("hidden");
    };
  }

  if (switchToSignup) {
    switchToSignup.onclick = (e) => {
      e.preventDefault();
      loginModal.classList.add("hidden");
      signupModal.classList.remove("hidden");
    };
  }

  // Envoi AJAX formulaire signup
  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const username = document.getElementById("signupName").value.trim();
      const email = document.getElementById("signupEmail").value.trim();
      const password = document.getElementById("signupPassword").value;
      const confirm = document.getElementById("signupPasswordConfirm").value;
      const avatar = document.getElementById("signupAvatar").value.trim();

      if (password !== confirm) {
        alert("Les mots de passe ne correspondent pas.");
        return;
      }

      try {
        const response = await fetch("signup/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify({ username, email, password, avatar }),
        });

        const data = await response.json();

        if (response.ok) {
          alert("Inscription réussie !");
          signupForm.reset();
          signupModal.classList.add("hidden");
        } else {
          alert(data.error || "Erreur lors de l'inscription.");
        }
      } catch (err) {
        console.error("Erreur réseau :", err);
        alert("Une erreur est survenue. Réessayez plus tard.");
      }
    });
  }
});

// CSRF pour Django
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Modales légales
const termsModal = document.getElementById("termsModal");
const privacyModal = document.getElementById("privacyModal");
const showTermsModal = document.getElementById("showTermsModal");
const showPrivacyModal = document.getElementById("showPrivacyModal");
const closeTermsModal = document.getElementById("closeTermsModal");
const closePrivacyModal = document.getElementById("closePrivacyModal");
const termsOverlay = document.getElementById("termsModalOverlay");
const privacyOverlay = document.getElementById("privacyModalOverlay");

if (showTermsModal && termsModal) {
  showTermsModal.onclick = (e) => {
    e.preventDefault();
    termsModal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  };
  closeTermsModal.onclick = () => {
    termsModal.classList.add("hidden");
    document.body.style.overflow = "auto";
  };
  termsOverlay.onclick = () => {
    termsModal.classList.add("hidden");
    document.body.style.overflow = "auto";
  };
}

if (showPrivacyModal && privacyModal) {
  showPrivacyModal.onclick = (e) => {
    e.preventDefault();
    privacyModal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  };
  closePrivacyModal.onclick = () => {
    privacyModal.classList.add("hidden");
    document.body.style.overflow = "auto";
  };
  privacyOverlay.onclick = () => {
    privacyModal.classList.add("hidden");
    document.body.style.overflow = "auto";
  };
}
