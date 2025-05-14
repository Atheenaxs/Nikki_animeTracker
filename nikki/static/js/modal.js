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

  if (switchToLogin) {
    switchToLogin.addEventListener("click", (e) => {
      e.preventDefault();
      signupModal.classList.add("hidden");
      loginModal.classList.remove("hidden");
    });
  }

  if (switchToSignup) {
    switchToSignup.addEventListener("click", (e) => {
      e.preventDefault();
      loginModal.classList.add("hidden");
      signupModal.classList.remove("hidden");
    });
  }

  if (startNow) {
    startNow.addEventListener("click", (e) => {
      e.preventDefault();
      signupModal.classList.remove("hidden");
      document.body.style.overflow = "hidden";
    });
  }

  loginBtn.onclick = () => loginModal.classList.remove("hidden");
  signupBtn.onclick = () => signupModal.classList.remove("hidden");
  closeLoginModal.onclick = () => loginModal.classList.add("hidden");
  closeSignupModal.onclick = () => signupModal.classList.add("hidden");
  loginOverlay.onclick = () => loginModal.classList.add("hidden");
  signupOverlay.onclick = () => signupModal.classList.add("hidden");
});

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
