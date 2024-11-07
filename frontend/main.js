const { app, BrowserWindow, ipcMain } = require("electron");
const { spawn } = require('child_process');
const url = require("url");
const path = require("path");
const isDev = process.env.NODE_ENV === "development";

function createMainWindow() {
  const mainWindow = new BrowserWindow({
    title: "zaczytuje z index.html",
    width: 1000,
    height: 1000,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"), // Upewnij się, że ścieżka jest prawidłowa
      contextIsolation: true,
      enableRemoteModule: false,
      nodeIntegration: false,
    },
  });

  mainWindow.webContents.openDevTools();

  const startUrl = url.format({
    pathname: path.join(__dirname, "./my-app/build/index.html"),
    protocol: "file",
  });

  //"http://localhost:3000"
  mainWindow.loadURL("http://localhost:3000");
}

app.whenReady().then(createMainWindow);

ipcMain.on('start-analysis', (event) => {
  // Uruchom skrypt Pythona w tle
  console.log("Spawning Python process...");
  const pythonProcess = spawn('python', ['test.py']);

  pythonProcess.stdout.on('data', (data) => {
      const result = data.toString();
      try {
          const parsedResult = JSON.parse(result);
          console.log(parsedResult);
          event.reply('analysis-result', parsedResult);  // Przekazanie wyniku do renderer process (React)
      } catch (err) {
          console.error('Error parsing JSON:', err);
      }
  });

  pythonProcess.stderr.on('data', (data) => {
      console.error(`Python error: ${data}`);
  });

  pythonProcess.on('close', (code) => {
      console.log(`Python script ended with code ${code}`);
  });
});