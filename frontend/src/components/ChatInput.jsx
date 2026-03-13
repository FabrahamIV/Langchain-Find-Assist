// ChatInput: handles the message composer UI (text, file, voice, submit button).
// App stays in control of the actual values and logic; this component only
// raises events via the callbacks passed in props.

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
    <form className="chat-input-container" onSubmit={onSubmit}>
      {attachedFile ? (
        <div className="attached-file-pill">
          <span className="attached-file-icon">📎</span>
          <span className="attached-file-name">{attachedFile.name}</span>
          <button
            type="button"
            className="attached-file-remove"
            onClick={onRemoveFile}
          >
            ✕
          </button>
        </div>
      ) : null}

      <div className="chat-input-row gemini-style">
        <label className="icon-button" htmlFor="file-upload" title="Upload file">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          <input
            id="file-upload"
            type="file"
            className="file-input-hidden"
            onChange={onFileChange}
          />
        </label>

        <div className="chat-input-wrapper">
          <input
            className="chat-input gemini-input"
            placeholder="Ask Find-Assist"
            value={input}
            onChange={(event) => onInputChange(event.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                onSubmit(e);
              }
            }}
          />
        </div>

        {supportsVoice && (
          <button
            type="button"
            className={`icon-button voice-btn ${isRecording ? 'recording' : ''}`}
            onClick={onToggleRecording}
            disabled={!supportsVoice}
            title={
              supportsVoice
                ? isRecording
                  ? 'Stop recording'
                  : 'Use microphone'
                : 'Microphone not supported'
            }
          >
            {isRecording ? (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="2" ry="2"></rect></svg>
            ) : (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="22"></line></svg>
            )}
          </button>
        )}

        {input.trim() || attachedFile ? (
          <button
            type="submit"
            className="send-button-gemini"
            title="Send message"
          >
             <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
          </button>
        ) : null}
      </div>
    </form>
  )
}

export default ChatInput


