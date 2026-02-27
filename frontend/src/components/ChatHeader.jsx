// ChatHeader: static branding + short description at the top of the chat.
// Keeping this in its own component keeps App.jsx focused on data flow.

function ChatHeader() {
  return (
    <header className="chat-header">
      <div className="chat-header-title">
        <span className="chat-brand-dot" />
        <span className="chat-brand-name">Find Assist</span>
      </div>
      <div className="chat-header-subtitle">
        Ask anything about your project. Voice, files, and history are all in one place.
      </div>
    </header>
  )
}

export default ChatHeader

