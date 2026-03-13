// ChatHeader: static branding + short description at the top of the chat.
// Keeping this in its own component keeps App.jsx focused on data flow.

function ChatHeader() {
  return (
    <header className="chat-header">
      <div className="chat-header-title">
        <span className="chat-brand-dot" />
        <span className="chat-brand-name">Faisal Abraham Project</span>
      </div>
    </header>
  )
}

export default ChatHeader

