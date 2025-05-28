document.addEventListener("DOMContentLoaded", function () {
    const devicesListContainer = document.getElementById("devices_list");

    const titleElement = document.createElement("h3");
    titleElement.innerText = "Dispositivos Conectados";
    titleElement.style.position = "sticky";
    titleElement.style.top = "0";
    titleElement.style.backgroundColor = "#fff";
    titleElement.style.padding = "10px";
    titleElement.style.zIndex = "10";
    titleElement.style.borderBottom = "2px solid #ccc";

    devicesListContainer.appendChild(titleElement);

    async function fetchDevices() {
        try {
            const response = await fetch("/adm/devices");

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const devices = await response.json();

            renderDeviceList(devices);
        } catch (error) {
            console.error("Erro ao carregar dispositivos:", error);

            const errorMessage = document.createElement("p");
            errorMessage.textContent = "Não foi possível carregar os dispositivos. Tente novamente mais tarde.";
            errorMessage.style.color = "red";

            devicesListContainer.appendChild(errorMessage);
        }
    }

    function renderDeviceList(devices) {
        const listContainer = document.createElement("div");
        listContainer.style.maxHeight = "300px";
        listContainer.style.overflowY = "auto";
        listContainer.style.padding = "10px";

        devices.forEach(device => {
            const deviceItem = document.createElement("div");
            deviceItem.classList.add("device-item");
            deviceItem.innerHTML = `
                <p><strong>IP:</strong> ${device.ip}</p>
                <p><strong>Grupo:</strong> ${device.group}</p>
                <p><strong>Local:</strong> ${device.locale}</p>
                <hr>
            `;

            listContainer.appendChild(deviceItem);
        });

        devicesListContainer.appendChild(listContainer);
    }

    fetchDevices();
});
