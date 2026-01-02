document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.querySelector(".navbar");
  const mobileToggle = document.querySelector(".mobile-menu-toggle");
  const mobileList = document.querySelector(".mobile-list-items");
  const mobileMenu = document.getElementById("mobile-menu");
  const form = document.getElementById("contact-form");
  const messageDiv = document.getElementById("form-message");
  const arrowUp = document.querySelector(".arrow-up-fixed");

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
    // Toggle back-to-top arrow visibility
    if (arrowUp) {
      if (window.scrollY > 300) {
        arrowUp.classList.add("show");
      } else {
        arrowUp.classList.remove("show");
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

  // Smooth scroll to top on arrow click
  if (arrowUp) {
    arrowUp.addEventListener("click", function (e) {
      // If href contains a hash, let default behavior handle focus shift; still animate scroll
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Navbar active link highlighting
  const currentPath = window.location.pathname.split("/").pop();
  const currentHash = window.location.hash;

  // Desktop nav links
  const desktopLinks = document.querySelectorAll(".navbar ul a");
  // Mobile nav links
  const mobileLinks = document.querySelectorAll(".mobile-menu a");

  // Highlight desktop nav links based on scroll/hash/path
  desktopLinks.forEach(function (link) {
    const linkHref = link.getAttribute("href");
    if (
      (currentPath === "" || currentPath === "index.html") &&
      linkHref.startsWith("#") &&
      linkHref === currentHash
    ) {
      link.classList.add("active");
    } else if (
      linkHref === currentPath ||
      (linkHref === "index.html" &&
        (currentPath === "" || currentPath === "index.html"))
    ) {
      link.classList.add("active");
    } else if (
      linkHref.includes("#") &&
      (window.location.pathname + window.location.hash).endsWith(linkHref)
    ) {
      link.classList.add("active");
    }
  });

  // Highlight mobile nav links ONLY by exact path match (no scroll/hash)
  mobileLinks.forEach(function (link) {
    const linkHref = link.getAttribute("href");
    if (
      linkHref === currentPath ||
      (linkHref === "index.html" &&
        (currentPath === "" || currentPath === "index.html"))
    ) {
      link.classList.add("active");
    }
  });

  // AJAX Formspree form submission with custom thank you message and auto-redirect
  if (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();

      const formData = new FormData(form);

      try {
        const response = await fetch(form.action, {
          method: "POST",
          body: formData,
          headers: {
            Accept: "application/json",
          },
        });

        if (response.ok) {
          form.style.display = "none";
          messageDiv.style.display = "block";
          messageDiv.innerHTML = `
            <h3>Thank you!</h3>
            <p>Your message has been sent. We will get back to you soon.</p>
            <a href="index.html" class="btn" style="margin-top:1.5rem;display:inline-block;">Return to Home</a>
          `;
          // Automatically redirect to home after 4 seconds
          setTimeout(function () {
            window.location.href = "index.html";
          }, 4000);
        } else {
          messageDiv.style.display = "block";
          messageDiv.innerHTML =
            "<p>There was an error sending your message. Please try again later.</p>";
        }
      } catch (error) {
        messageDiv.style.display = "block";
        messageDiv.innerHTML =
          "<p>There was an error sending your message. Please try again later.</p>";
      }
    });
  }

  // IntersectionObserver for about-intro animation (bidirectional)
  const left = document.querySelector(".about-intro .left-content");
  const right = document.querySelector(".about-intro .right-content");
  if (left && right) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
          } else {
            entry.target.classList.remove("visible");
          }
        });
      },
      {
        threshold: 0.3, // Trigger when 30% of the element is visible
      }
    );
    observer.observe(left);
    observer.observe(right);
  }

  // IntersectionObserver for about-overview animation (bidirectional)
  const secondLeft = document.querySelector(".about-overview .left-content");
  const secondRight = document.querySelector(".about-overview .right-content");
  const btnInfo = document.querySelector(".about-overview .btn-info a");
  if (secondLeft || secondRight || btnInfo) {
    const observer2 = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
          } else {
            entry.target.classList.remove("visible");
          }
        });
      },
      {
        threshold: 0.3,
      }
    );
    if (secondLeft) observer2.observe(secondLeft);
    if (secondRight) observer2.observe(secondRight);
    if (btnInfo) observer2.observe(btnInfo);
  }

  // IntersectionObserver for each project card animation (one-time reveal to prevent pulsing)
  const projectCards = document.querySelectorAll(".projects .project");
  if (projectCards.length) {
    const projectObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            // Unobserve after first reveal to avoid toggle flicker/pulsing
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.15, // Trigger a bit earlier for smoother entry
      }
    );
    projectCards.forEach((card) => projectObserver.observe(card));
  }

  // IntersectionObserver for skills heading and description (bidirectional)
  const skillsHeading = document.querySelector(".skills-heading");
  const skillsDescription = document.querySelector(".skills-description");
  if (skillsHeading || skillsDescription) {
    const skillsObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
          } else {
            entry.target.classList.remove("visible");
          }
        });
      },
      {
        threshold: 0.3,
      }
    );
    if (skillsHeading) skillsObserver.observe(skillsHeading);
    if (skillsDescription) skillsObserver.observe(skillsDescription);
  }

  // Portfolio filters: quick project subset by tech
  const filterBar =
    document.querySelector(".projects-filters") ||
    document.querySelector(".portfolio-filters");
  const filterButtons = filterBar
    ? filterBar.querySelectorAll("button[data-filter]")
    : [];
  const projectList =
    document.getElementById("projects-gallery") ||
    document.getElementById("projects-list");
  const projects = projectList ? projectList.querySelectorAll(".project") : [];
  const projectsCount = document.getElementById("projects-count");

  function updateProjectsCount() {
    if (!projectsCount) return;
    const total = projects.length;
    let visible = 0;
    projects.forEach((card) => {
      const isHidden = card.hidden || card.style.display === "none";
      if (!isHidden) visible += 1;
    });
    if (visible === total) {
      projectsCount.textContent = `Showing all ${total} projects`;
    } else {
      projectsCount.textContent = `Showing ${visible} of ${total} projects`;
    }
  }

  function applyFilter(filter) {
    projects.forEach((card) => {
      const tech = (card.getAttribute("data-tech") || "").toLowerCase();
      const match = filter === "all" || tech.split(/\s+/).includes(filter);
      // Hide via both hidden attribute and inline style for robustness
      card.hidden = !match;
      card.style.display = match ? "" : "none";
    });
    updateProjectsCount();
  }

  function setActiveButton(activeBtn) {
    filterButtons.forEach((btn) => {
      const isActive = btn === activeBtn;
      btn.setAttribute("aria-pressed", isActive ? "true" : "false");
      btn.classList.toggle("btn--primary", isActive);
      btn.classList.toggle("btn--secondary", !isActive);
    });
  }

  if (filterButtons.length && projects.length) {
    filterButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const filter = btn.getAttribute("data-filter");
        applyFilter(filter);
        setActiveButton(btn);
      });
    });
    // Initialize to 'all'
    applyFilter("all");
  } else {
    // Still initialize count if filters are missing
    updateProjectsCount();
  }
});
