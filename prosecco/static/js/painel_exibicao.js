function atualizarRelogio() {
  const agora = new Date();
  const horas = String(agora.getHours()).padStart(2, '0');
  const minutos = String(agora.getMinutes()).padStart(2, '0');
  const segundos = String(agora.getSeconds()).padStart(2, '0');
  const horaFormatada = `${horas}:${minutos}:${segundos}`;
  document.getElementById('clock').textContent = horaFormatada;
}

setInterval(atualizarRelogio, 1000);
atualizarRelogio();

document.addEventListener("DOMContentLoaded", () => {
  const API_KEY = "b37d4e6ea6d62ad6c108007b65655186";
  const cidade = "Tres Lagoas,BR";

  fetch(`https://api.openweathermap.org/data/2.5/weather?q=${cidade}&appid=${API_KEY}&units=metric&lang=pt_br`)
    .then(response => response.json())
    .then(data => {
      const temperatura = Math.round(data.main.temp);
      const descricao = data.weather[0].description;

      const iconeClima = document.getElementById("icone-clima");
      const codigoIcone = data.weather[0].icon;

      switch (codigoIcone) {
        case "01d":
          iconeClima.className = "fas fa-sun fa-lg"; // ☀️
          break;
        case "01n":
          iconeClima.className = "fas fa-moon fa-lg"; // 🌙
          break;
        case "02d":
          iconeClima.className = "fas fa-cloud-sun fa-lg"; // 🌤️
          break;
        case "02n":
          iconeClima.className = "fas fa-cloud-moon fa-lg"; // 🌥️ (noite)
          break;
        case "03d":
        case "03n":
        case "04d":
        case "04n":
          iconeClima.className = "fas fa-cloud fa-lg"; // ☁️
          break;
        case "09d":
        case "09n":
        case "10d":
        case "10n":
          iconeClima.className = "fas fa-cloud-showers-heavy fa-lg"; // 🌧️
          break;
        case "11d":
        case "11n":
          iconeClima.className = "fas fa-bolt fa-lg"; // 🌩️
          break;
        case "13d":
        case "13n":
          iconeClima.className = "fas fa-snowflake fa-lg"; // ❄️
          break;
        case "50d":
        case "50n":
          iconeClima.className = "fas fa-smog fa-lg"; // 🌫️
          break;
        default:
          iconeClima.className = "fas fa-cloud-sun fa-lg"; // fallback
      }

      document.getElementById("temperatura").textContent = `${temperatura}°C`;
      document.getElementById("descricao").textContent = descricao.charAt(0).toUpperCase() + descricao.slice(1);
    })
    .catch(() => {
      document.getElementById("descricao").textContent = "Não foi possível carregar o clima";
    });
});

document.addEventListener("DOMContentLoaded", () => {
  const diasContainer = document.getElementById("dias");
  const mesAno = document.getElementById("mesAno");

  const hoje = new Date();
  const ano = hoje.getFullYear();
  const mes = hoje.getMonth(); 
  const diaHoje = hoje.getDate();

  const nomesMeses = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
  ];

  mesAno.textContent = `${nomesMeses[mes]} ${ano}`;

  const primeiroDia = new Date(ano, mes, 1).getDay(); 
  const totalDias = new Date(ano, mes + 1, 0).getDate();

  let html = "<tr>";
  for (let i = 0; i < primeiroDia; i++) {
    html += "<td></td>";
  }

  for (let dia = 1; dia <= totalDias; dia++) {
    const classe = dia === diaHoje ? "dia-hoje" : "";
    html += `<td class="${classe}">${dia}</td>`;
    if ((dia + primeiroDia) % 7 === 0) html += "</tr><tr>";
  }
  html += "</tr>";

  diasContainer.innerHTML = html;
});
