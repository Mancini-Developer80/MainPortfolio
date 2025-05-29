document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.querySelector(".navbar");
  const mobileToggle = document.querySelector(".mobile-menu-toggle");
  const mobileList = document.querySelector(".mobile-list-items");
  const mobileMenu = document.getElementById("mobile-menu");

  // Track mobile menu state
  let mobileMenuOpen = false;

  // Scroll event: toggle .active if mobile menu is NOT open, or keep if menu is open
  window.addEventListener("scroll", function () {
    if (!mobileMenuOpen) {
      if (window.scrollY > 50) {
        navbar.classList.add("active");
      } else {
        navbar.classList.remove("active");
      }
    }
  });

  if (mobileToggle && mobileList && mobileMenu) {
    mobileToggle.addEventListener("click", function (e) {
      e.stopPropagation();
      const isOpen = mobileList.classList.toggle("open");
      mobileMenuOpen = isOpen;

      // Accessibility improvements
      mobileToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      mobileMenu.setAttribute("aria-hidden", isOpen ? "false" : "true");

      // Add .active if menu is open or page is scrolled
      if (isOpen || window.scrollY > 50) {
        navbar.classList.add("active");
      } else {
        navbar.classList.remove("active");
      }
    });

    // Optional: close mobile menu when clicking outside
    document.addEventListener("click", function (e) {
      if (
        mobileMenuOpen &&
        !mobileList.contains(e.target) &&
        !mobileToggle.contains(e.target)
      ) {
        mobileList.classList.remove("open");
        mobileMenuOpen = false;
        mobileToggle.setAttribute("aria-expanded", "false");
        mobileMenu.setAttribute("aria-hidden", "true");
        // Add .active if scrolled, remove if not
        if (window.scrollY > 50) {
          navbar.classList.add("active");
        } else {
          navbar.classList.remove("active");
        }
      }
    });
  }
});
