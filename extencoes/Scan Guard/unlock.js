document.getElementById("submitBtn").addEventListener("click", () => {
  const senhaInput = document.getElementById("senhaInput").value.trim();
  const message = document.getElementById("message");

  if (!senhaInput) {
    message.textContent = "Por favor, insira a senha.";
    return;
  }

  chrome.storage.local.get("senha", (data) => {
    const senhaSalva = data.senha || "";

    if (senhaInput === senhaSalva) {
      // Correct password, unlock downloads
      chrome.storage.local.set({ downloadUnlocked: true }, () => {
        message.style.color = "green";
        message.textContent = "Downloads desbloqueados com sucesso!";
        setTimeout(() => {
          window.close();
        }, 1000);
      });
    } else {
      message.style.color = "red";
      message.textContent = "Senha incorreta. Tente novamente.";
    }
  });
});
