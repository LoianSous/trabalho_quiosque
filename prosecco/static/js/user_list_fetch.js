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
        usersListContainer.innerHTML = "";
        usersListContainer.appendChild(titleElement);

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
            userItem.style.display = "flex";
            userItem.style.justifyContent = "space-between";
            userItem.style.alignItems = "center";
            userItem.style.padding = "5px 0";
            userItem.style.borderBottom = "1px solid #ddd";

            const userInfo = document.createElement("div");
            userInfo.innerHTML = `
                <p><strong>ID:</strong> ${user.id}</p>
                <p><strong>Nome:</strong> ${user.name}</p>
                <p><strong>Email:</strong> ${user.email}</p>
                <p><strong>Status:</strong> ${user.u_state}</p>
            `;

            const buttonsContainer = document.createElement("div");
            buttonsContainer.style.display = "grid";
            buttonsContainer.style.gridTemplateColumns = "1fr 1fr";
            buttonsContainer.style.gridGap = "5px";
            buttonsContainer.style.width = "150px";

            const btnChangePassword = document.createElement("button");
            btnChangePassword.textContent = "Alterar Senha";
            btnChangePassword.onclick = () => changePassword(user.id, user.u_state);

            const btnApprove = document.createElement("button");
            btnApprove.textContent = "Aprovar";
            btnApprove.onclick = () => approveUser(user.id, user.u_state);

            const btnInactivate = document.createElement("button");
            btnInactivate.textContent = "Desativar";
            btnInactivate.onclick = () => inactivateUser(user.id, user.u_state);

            const btnDelete = document.createElement("button");
            btnDelete.textContent = "Excluir";
            btnDelete.onclick = () => deleteUser(user.id);

            buttonsContainer.appendChild(btnChangePassword);
            buttonsContainer.appendChild(btnApprove);
            buttonsContainer.appendChild(btnInactivate);
            buttonsContainer.appendChild(btnDelete);

            userItem.appendChild(userInfo);
            userItem.appendChild(buttonsContainer);

            listContainer.appendChild(userItem);
        });

        usersListContainer.appendChild(listContainer);
    }

    async function changePassword(userId, currentStatus) {
        if (currentStatus === "DELETED") {
            alert("Não é possível alterar a senha de um usuário excluído.");
            return;
        }
        const newPassword = prompt("Digite a nova senha para o usuário:");
        if (!newPassword) {
            alert("Senha não informada, operação cancelada.");
            return;
        }

        try {
            const response = await fetch(`/adm/user/${userId}`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password: newPassword })
            });

            if (response.ok) {
                alert("Senha alterada com sucesso.");
                fetchUsers();
            } else {
                alert("Falha ao alterar a senha.");
            }
        } catch (error) {
            console.error("Erro ao comunicar com o servidor:", error);
            alert("Erro na comunicação com o servidor.");
        }
    }

    async function approveUser(userId, currentStatus) {
        if (currentStatus === "DELETED") {
            alert("Não é possível aprovar um usuário excluído.");
            return;
        }
        if (currentStatus === "ACTIVE") {
            alert("Usuário já está aprovado (ACTIVE).");
            return;
        }

        try {
            const response = await fetch(`/adm/user/${userId}`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ u_state: "ACTIVE" })
            });

            if (response.ok) {
                alert("Usuário aprovado com sucesso.");
                fetchUsers();
            } else {
                alert("Falha ao aprovar usuário.");
            }
        } catch (error) {
            console.error("Erro ao comunicar com o servidor:", error);
            alert("Erro na comunicação com o servidor.");
        }
    }

    async function inactivateUser(userId, currentStatus) {
        if (currentStatus === "DELETED") {
            alert("Não é possível inativar um usuário excluído.");
            return;
        }
        if (currentStatus === "INACTIVE") {
            alert("Usuário já está inativo.");
            return;
        }

        try {
            const response = await fetch(`/adm/user/${userId}`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ u_state: "INACTIVE" })
            });

            if (response.ok) {
                alert("Usuário inativado com sucesso.");
                fetchUsers();
            } else {
                alert("Falha ao inativar usuário.");
            }
        } catch (error) {
            console.error("Erro ao comunicar com o servidor:", error);
            alert("Erro na comunicação com o servidor.");
        }
    }

    async function deleteUser(userId) {
        try {
            const response = await fetch(`/adm/user/${userId}`, {
                method: "DELETE"
            });

            if (response.ok) {
                alert("Usuário excluído (soft delete) com sucesso.");
                fetchUsers();
            } else {
                alert("Falha ao excluir usuário.");
            }
        } catch (error) {
            console.error("Erro ao comunicar com o servidor:", error);
            alert("Erro na comunicação com o servidor.");
        }
    }

    fetchUsers();
});