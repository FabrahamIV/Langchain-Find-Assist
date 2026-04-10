function ChatInput({
  input,
  onInputChange,
  onSubmit,
  attachedFile,
  onFileChange,
  onRemoveFile,
  supportsVoice,
  isRecording,
  onToggleRecording,
}) {
  return (
    <footer className="w-full p-6 pb-8 flex justify-center z-30 shrink-0">
      <div className="w-full max-w-4xl">
        {attachedFile && (
          <div className="mb-2 inline-flex items-center gap-2 bg-surface-container-highest dark:bg-slate-800 text-on-surface dark:text-slate-200 px-3 py-1.5 rounded-xl text-sm shadow-sm">
            <span className="material-symbols-outlined text-[18px]">attach_file</span>
            <span className="max-w-[200px] truncate">{attachedFile.name}</span>
            <button
              type="button"
              className="text-slate-400 hover:text-red-500 transition-colors ml-1"
              onClick={onRemoveFile}
            >
              <span className="material-symbols-outlined text-[18px]">close</span>
            </button>
          </div>
        )}

        <form 
          className="bg-surface-container-highest dark:bg-slate-900 rounded-[2rem] p-2 focus-within:bg-surface-container-lowest dark:focus-within:bg-slate-800/80 focus-within:shadow-[0px_12px_32px_rgba(42,52,57,0.06)] border border-transparent focus-within:border-outline-variant/20 transition-all duration-300 relative group"
          onSubmit={onSubmit}
        >
          <textarea
            className="w-full bg-transparent border-none focus:ring-0 resize-none px-6 pt-4 pb-14 text-on-surface dark:text-slate-100 placeholder:text-slate-500 font-['Inter'] outline-none"
            placeholder="Message Find-Assist..."
            rows={3}
            value={input}
            onChange={(e) => onInputChange(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                onSubmit(e);
              }
            }}
          />

          <div className="absolute bottom-3 left-4 right-4 flex items-center justify-between">
            <div className="flex items-center gap-1">
              <label 
                className="p-2 text-slate-500 hover:text-primary dark:hover:text-blue-400 hover:bg-primary-container/30 dark:hover:bg-slate-800 rounded-xl transition-all cursor-pointer" 
                title="Add File"
              >
                <span className="material-symbols-outlined">attach_file</span>
                <input
                  type="file"
                  className="hidden"
                  onChange={onFileChange}
                />
              </label>
            </div>
            
            <div className="flex items-center gap-2">
              {supportsVoice && (
                <button
                  type="button"
                  className={`p-2 rounded-xl transition-all ${
                    isRecording
                      ? 'bg-red-100 text-red-500 dark:bg-red-500/20 dark:text-red-400 animate-pulse'
                      : 'text-slate-500 hover:text-primary dark:hover:text-blue-400 hover:bg-primary-container/30 dark:hover:bg-slate-800'
                  }`}
                  onClick={onToggleRecording}
                  title={isRecording ? 'Stop recording' : 'Use microphone'}
                >
                  <span className="material-symbols-outlined">mic</span>
                </button>
              )}
              
              <button
                type="submit"
                disabled={!input.trim() && !attachedFile}
                className="flex items-center justify-center w-10 h-10 rounded-2xl bg-gradient-to-br from-primary to-primary-dim text-white shadow-lg shadow-primary/20 hover:scale-105 active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
              >
                <span className="material-symbols-outlined text-xl">arrow_upward</span>
              </button>
            </div>
          </div>

          <div className="absolute -top-10 left-1/2 -translate-x-1/2 flex items-center gap-4 text-[10px] font-bold tracking-widest text-slate-400 uppercase opacity-0 group-focus-within:opacity-100 transition-opacity">
            <span className="flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-green-500"></span> Find-Assist Model</span>
            <span className="flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-primary"></span> Memory Active</span>
          </div>
        </form>
        
        {/* <p className="text-[10px] text-center text-slate-400 mt-3 font-medium">Find-Assist may display inaccurate info, including about people, so double-check its responses.</p> */}
      </div>
    </footer>
  );
}

export default ChatInput;

