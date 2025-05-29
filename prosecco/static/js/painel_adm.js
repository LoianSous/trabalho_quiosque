document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("adminSidebar");
  const toggle = document.getElementById("menuToggle");
  const closeSidebar = document.getElementById("closeSidebar");

  const welcomeSection = document.querySelector("main .section");
  const welcomeTitle = welcomeSection.querySelector("h2.title");
  const welcomeSubtitle = welcomeSection.querySelector("p.subtitle");

  const sections = {
    upload: document.getElementById("uploadSection"),
    selecionar: document.getElementById("selecionarTelasSection"),
    identificar: document.getElementById("identificarTelasSection"),
    gerenciar: document.getElementById("gerenciarContasSection"),
  };

  // Obter o nome do usuário do atributo data-username
  const username = document.body.getAttribute("data-username");

  if (username) {
    if (welcomeTitle) {
      welcomeTitle.innerText = `Bem-vindo, ${username}`;
    }
    if (welcomeSubtitle) {
      welcomeSubtitle.innerText = "Selecione uma opção no menu à esquerda para começar.";
    }
  }

  if (toggle) {
    toggle.addEventListener("click", () => {
      sidebar.classList.toggle("active");
    });
  }

  if (closeSidebar) {
    closeSidebar.addEventListener("click", () => {
      sidebar.classList.remove("active");
    });
  }

  const links = document.querySelectorAll(".menu-list li");

  if (links.length >= 5) {
    links[0].addEventListener("click", (e) => {
      e.preventDefault();

      if (welcomeSection) welcomeSection.style.display = "block";

      for (const key in sections) {
        sections[key].style.display = "none";
      }

      sidebar.classList.remove("active");
    });

    links[1].addEventListener("click", (e) => {
      e.preventDefault();
      toggleSections("upload");
    });

    links[2].addEventListener("click", (e) => {
      e.preventDefault();
      toggleSections("selecionar");
    });

    links[3].addEventListener("click", (e) => {
      e.preventDefault();
      toggleSections("identificar");
    });

    links[4].addEventListener("click", (e) => {
      e.preventDefault();
      toggleSections("gerenciar");
    });
  }

  function toggleSections(show) {
    if (welcomeSection) welcomeSection.style.display = "none";

    for (const key in sections) {
      sections[key].style.display = key === show ? "block" : "none";
    }

    sidebar.classList.remove("active");
  }
});