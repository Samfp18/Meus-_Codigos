chrome.runtime.onInstalled.addListener(() => {
  console.log("Scam Guard ativado com sucesso.");
});

let notifiedDownloads = new Set();

chrome.downloads.onCreated.addListener((downloadItem) => {
  chrome.storage.local.get(["senha", "downloadUnlocked"], (data) => {
    const senhaCorreta = data.senha || null;
    const downloadUnlocked = data.downloadUnlocked || false;

    if (!senhaCorreta || downloadUnlocked) {
      // No password set or downloads unlocked, allow download
      return;
    }

    // Cancel the download and notify user only once per download
    if (!notifiedDownloads.has(downloadItem.id)) {
      chrome.downloads.cancel(downloadItem.id);
      chrome.notifications.create({
        type: "basic",
        iconUrl: "icon_48.png",
        title: "Download Bloqueado",
        message: "Para permitir downloads, insira a senha para desbloquear."
      });
      notifiedDownloads.add(downloadItem.id);

      // Open unlock.html popup for password entry
      chrome.windows.create({
        url: chrome.runtime.getURL("unlock.html"),
        type: "popup",
        width: 360,
        height: 280,
        focused: true
      });
    }
  });
});
