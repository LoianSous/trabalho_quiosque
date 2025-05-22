document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("adminSidebar");
  const toggle = document.getElementById("menuToggle");
  const closeSidebar = document.getElementById("closeSidebar");

  const welcomeSection = document.querySelector("main .section");
  const sections = {
    upload: document.getElementById("uploadSection"),
    selecionar: document.getElementById("selecionarTelasSection"),
    identificar: document.getElementById("identificarTelasSection"),
    gerenciar: document.getElementById("gerenciarContasSection"),
  };

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

  const fileInput = document.getElementById('fileInput');
  const fileName = document.getElementById('fileName');
  const placeholder = document.getElementById('uploadPlaceholder');

  if (fileInput && fileName && placeholder) {
    fileInput.addEventListener('change', () => {
      if (fileInput.files.length > 0) {
        const nome = fileInput.files[0].name;
        placeholder.style.display = "none";
        fileName.style.display = "block";
        fileName.textContent = `Imagem selecionada: ${nome}`;
      }
    });
  }
});
