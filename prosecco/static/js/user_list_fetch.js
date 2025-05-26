document.addEventListener("DOMContentLoaded", function () {
    const usersListContainer = document.getElementById("users_list");

    const titleElement = document.createElement("h3");
    titleElement.innerText = "Usuários";
    titleElement.style.position = "sticky";
    titleElement.style.top = "0";
    titleElement.style.backgroundColor = "#fff";
    titleElement.style.padding = "10px";
    titleElement.style.zIndex = "10";
    titleElement.style.borderBottom = "2px solid #ccc";

    usersListContainer.appendChild(titleElement);

    async function fetchUsers() {
        try {
            const response = await fetch("/adm/users");
            const users = await response.json();

            renderUserList(users);
        } catch (error) {
            console.error("Erro ao carregar usuários:", error);
        }
    }

    function renderUserList(users) {
        const listContainer = document.createElement("div");
        listContainer.style.maxHeight = "300px";
        listContainer.style.overflowY = "auto";
        listContainer.style.padding = "10px";

        users.forEach(user => {
            const userItem = document.createElement("div");
            userItem.classList.add("user-item");
            userItem.innerHTML = `
                <p><strong>ID:</strong> ${user.id}</p>
                <p><strong>Nome:</strong> ${user.name}</p>
                <p><strong>Email:</strong> ${user.email}</p>
                <label><strong>Status:</strong></label>
                <select class="status-select" data-user-id="${user.id}">
                    <option value="active" ${user.u_state === "active" ? "selected" : ""}>Active</option>
                    <option value="blocked" ${user.u_state === "blocked" ? "selected" : ""}>Blocked</option>
                    <option value="pending" ${user.u_state === "pending" ? "selected" : ""}>Pending</option>
                    <option value="inactive" ${user.u_state === "inactive" ? "selected" : ""}>Inactive</option>
                </select>
                <hr>
            `;

            listContainer.appendChild(userItem);
        });

        usersListContainer.appendChild(listContainer);

        document.querySelectorAll(".status-select").forEach(select => {
            select.addEventListener("change", function () {
                const userId = this.getAttribute("data-user-id");
                const newStatus = this.value;
                updateUserStatus(userId, newStatus);
            });
        });
    }

    async function updateUserStatus(userId, status) {
        try {
            const response = await fetch(`/adm/users/${userId}/update-status`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ u_state: status })
            });

            if (response.ok) {
                console.log(`Status do usuário ${userId} atualizado para ${status}`);
            } else {
                console.error("Erro ao atualizar status");
            }
        } catch (error) {
            console.error("Erro ao comunicar com o servidor:", error);
        }
    }

    fetchUsers();
});