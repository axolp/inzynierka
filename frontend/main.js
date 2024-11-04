const { app, BrowserWindow } = require("electron");
const url = require("url");
const path = require("path");
const isDev = process.env.NODE_ENV === "development";

function createMainWindow() {
  const mainWindow = new BrowserWindow({
    title: "zaczytuje z index.html",
    width: 1000,
    height: 1000,
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
