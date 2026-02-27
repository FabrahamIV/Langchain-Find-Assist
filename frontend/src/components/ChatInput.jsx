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

      <div className="chat-input-row">
        <label className="icon-button" htmlFor="file-upload">
          <span className="icon">📎</span>
          <input
            id="file-upload"
            type="file"
            className="file-input-hidden"
            onChange={onFileChange}
          />
        </label>

        <div className="chat-input-wrapper">
          <input
            className="chat-input"
            placeholder="Ask a question about your code, data, or files..."
            value={input}
            onChange={(event) => onInputChange(event.target.value)}
          />
        </div>

        <button
          type="button"
          className={`icon-button ${isRecording ? 'icon-button-active' : ''}`}
          onClick={onToggleRecording}
          disabled={!supportsVoice}
          title={
            supportsVoice
              ? isRecording
                ? 'Stop voice input'
                : 'Start voice input'
              : 'Voice input is not available in this browser'
          }
        >
          <span className="icon">
            {isRecording ? '■' : '🎤'}
          </span>
        </button>

        <button
          type="submit"
          className="send-button"
          disabled={!input.trim() && !attachedFile}
        >
          Send
        </button>
      </div>
    </form>
  )
}

export default ChatInput

