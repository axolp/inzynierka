const { app, BrowserWindow, ipcMain } = require("electron");
const url = require("url");
const path = require("path");
const { spawn } = require("child_process");
const isDev = process.env.NODE_ENV === "development";

let pythonProcess;

ipcMain.on("start-python", (event, args) => {
  const pythonPath =
    "C:\\Users\\PC\\Desktop\\PracaInzynierska\\python311\\env\\Scripts\\python.exe";
  // Ścieżka do skryptu Python
  //const scriptPath = path.join(__dirname, "path", "to", "program.py");

  // Uruchamianie programu Python
  pythonProcess = spawn(pythonPath, ["async.py"]);

  pythonProcess.stdout.on("data", (data) => {
    console.log(`Dane z programu Python: ${data}`);
    // Przekaż dane do renderer process
    event.sender.send("python-data", data.toString());
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`Błąd w Pythonie: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    console.log(`Program Python zakończył działanie z kodem ${code}`);
  });
});

ipcMain.on("stop-python", () => {
  if (pythonProcess) {
    pythonProcess.kill();
    pythonProcess = null;
  }
});
function createMainWindow() {
  const mainWindow = new BrowserWindow({
    title: "zaczytuje z index.html",
    width: 1000,
    height: 1000,
    webPreferences: {
      nodeIntegration: true, // Włączenie nodeIntegration
      contextIsolation: false, // Wyłączenie izolacji kontekstu
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
