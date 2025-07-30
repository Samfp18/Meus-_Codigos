document.addEventListener("DOMContentLoaded", () => {
  const campoSenhaAtual = document.getElementById("campoSenhaAtual");
  const campoNovaSenha = document.getElementById("campoNovaSenha");
  const salvarBtn = document.getElementById("salvarBtn");
  const mensagem = document.getElementById("mensagem");

  // Load current password status
  chrome.storage.local.get("senha", (data) => {
    if (!data.senha) {
      mensagem.textContent = "Nenhuma senha configurada. Defina uma nova senha.";
    } else {
      // Password is set, disable new password input and save button
      campoNovaSenha.style.display = "none";
      salvarBtn.style.display = "none";
      mensagem.textContent = "Senha configurada. Insira a senha atual para desbloquear downloads.";
    }
  });

  salvarBtn.addEventListener("click", () => {
    const senhaAtual = campoSenhaAtual.value.trim();
    const novaSenha = campoNovaSenha.value.trim();

    if (!novaSenha) {
      mensagem.style.color = "red";
      mensagem.textContent = "Por favor, insira a nova senha.";
      return;
    }

    chrome.storage.local.get("senha", (data) => {
      const senhaSalva = data.senha || "";

      if (senhaSalva && senhaAtual !== senhaSalva) {
        mensagem.style.color = "red";
        mensagem.textContent = "Senha atual incorreta.";
        return;
      }

      chrome.storage.local.set({ senha: novaSenha }, () => {
        mensagem.style.color = "green";
        mensagem.textContent = "Senha salva com sucesso!";
        campoSenhaAtual.value = "";
        campoNovaSenha.value = "";
        // After saving password, hide new password input and save button
        campoNovaSenha.style.display = "none";
        salvarBtn.style.display = "none";
      });
    });
  });
});
