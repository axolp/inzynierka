// electron.d.ts
export {};

declare global {
    interface Window {
        electronAPI: {
            startAnalysis: () => void;
            onAnalysisResult: (callback: (result: any) => void) => void;
        };
    }
}
