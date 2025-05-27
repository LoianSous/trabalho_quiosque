  async function fetchDevices() {
    try {
      const response = await fetch('/adm/devices');

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const devices = await response.json();

      console.log('Dispositivos recebidos:', devices);

      devices.forEach(device => {
        console.log(`IP: ${device.ip}, Grupo: ${device.group}, Local: ${device.locale}`);
      });

    } catch (error) {
      console.error('Falha ao buscar os dispositivos:', error);
      const displayArea = document.querySelector('.box');
      const errorMessage = document.createElement('p');
      errorMessage.textContent = 'Não foi possível carregar os dispositivos. Tente novamente mais tarde.';
      errorMessage.style.color = 'red';
      if (displayArea) {
        displayArea.appendChild(errorMessage);
      }
    }
  }

  document.addEventListener('DOMContentLoaded', fetchDevices);