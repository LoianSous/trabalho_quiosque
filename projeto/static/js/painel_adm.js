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

  const params = new URLSearchParams(window.location.search);
  const secao = params.get("secao");

  const botoesMenu = document.querySelectorAll(".menu-list li a");
  const botoesPorSecao = {
    upload: 1,
    selecionar: 2,
    identificar: 3,
    gerenciar: 4
  };

  if (secao && botoesPorSecao[secao] !== undefined) {
    botoesMenu[botoesPorSecao[secao]].click();
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

const TEMPO_SESSAO_MINUTOS = 10;
const AVISO_MINUTOS = 5;  

let tempoRestante = TEMPO_SESSAO_MINUTOS * 60; 
let avisoEmitido = false;

const intervalo = setInterval(() => {
  tempoRestante--;

  if (tempoRestante === AVISO_MINUTOS * 60 && !avisoEmitido) {
    avisoEmitido = true;
    alert("Sua sessão irá expirar em 1 minuto. Salve seu progresso.");
  }

  if (tempoRestante <= 0) {
    clearInterval(intervalo);
    alert("Sua sessão expirou por inatividade. Você será redirecionado para o login.");
    window.location.href = "/logout";
  }
}, 1000); 

document.addEventListener("DOMContentLoaded", () => {
  const toasts = document.querySelectorAll(".toast");

  toasts.forEach((toast) => {
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(-10px)";
      toast.style.transition = "opacity 0.4s ease, transform 0.4s ease";
      setTimeout(() => toast.remove(), 400);
    }, 4000);
  });
});

function abrirModal(acao, url, mensagem, valorAtivo = null) {
    const form = document.getElementById("confirmForm");
    form.action = url;

    document.getElementById("modalTitle").textContent = acao;
    document.getElementById("modalMessage").textContent = mensagem;

    const campoAtivo = document.getElementById("campoAtivo");

    form.querySelectorAll('input[name="ids[]"]').forEach(el => el.remove());

    if (valorAtivo !== null && campoAtivo) {
        campoAtivo.name = "ativo";
        campoAtivo.value = valorAtivo;
    } else if (campoAtivo) {
        campoAtivo.removeAttribute("name");
        campoAtivo.removeAttribute("value");
    }

    if (acao.toLowerCase().includes("imagem")) {
        const selecionados = Array.from(document.querySelectorAll('input[name="ids[]"]:checked'));

        if (selecionados.length === 0) {
            alert("Nenhuma imagem selecionada.");
            return;
        }

        selecionados.forEach(cb => {
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "ids[]";
            input.value = cb.value;
            form.appendChild(input);
        });
    }

    document.getElementById("confirmacaoModal").classList.add("is-active");
}

function fecharModal() {
  document.getElementById("confirmacaoModal").classList.remove("is-active");
}

let todosSelecionados = false;

    function toggleSelecionarTodos() {
        const checkboxes = document.querySelectorAll('input[name="ids[]"]');
        todosSelecionados = !todosSelecionados;

        checkboxes.forEach(cb => cb.checked = todosSelecionados);

        const botao = document.querySelector('button[onclick="toggleSelecionarTodos()"]');
        botao.innerHTML = todosSelecionados
            ? '<i class="fas fa-times-circle mr-1"></i> Deselecionar tudo'
            : '<i class="fas fa-check-square mr-1"></i> Selecionar tudo';
    }

