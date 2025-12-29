document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.querySelector(".navbar");
  const mobileToggle = document.querySelector(".mobile-menu-toggle");
  const mobileList = document.querySelector(".mobile-list-items");
  const mobileMenu = document.getElementById("mobile-menu");
  const form = document.getElementById("contact-form");
  const messageDiv = document.getElementById("form-message");

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

  // IntersectionObserver for each project card animation (bidirectional)
  const projectCards = document.querySelectorAll(".projects .project");
  if (projectCards.length) {
    const projectObserver = new IntersectionObserver(
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
        threshold: 0.25, // Animate when 25% visible
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
});
