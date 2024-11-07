const { contextBridge, ipcRenderer } = require('electron');
console.log("JESTEM PRELOAD DZIALAM")
contextBridge.exposeInMainWorld('electronAPI', {
    startAnalysis: () => ipcRenderer.send('start-analysis'),
    onAnalysisResult: (callback) => ipcRenderer.on('analysis-result', (event, result) => callback(result)),
});
