// MessageList: renders either the list of messages or the "empty state".
// It does not know *how* messages are produced; it only knows how to display them.

function MessageList({ messages, messagesEndRef }) {
  const hasMessages = messages && messages.length > 0

  return (
    <section className="chat-messages">
      {hasMessages ? (
        messages.map((message) => (
          <div
            key={message.id}
            className={
              message.role === 'user'
                ? 'message message-user'
                : 'message message-assistant'
            }
          >
            <div className="message-avatar">
              {message.role === 'user' ? 'You' : 'AI'}
            </div>
            <div className="message-body">
              <div className="message-text">{message.content}</div>
              {message.fileName ? (
                <div className="message-file-pill">
                  <span className="message-file-icon">📎</span>
                  <span className="message-file-name">{message.fileName}</span>
                </div>
              ) : null}
            </div>
          </div>
        ))
      ) : (
        <div className="chat-empty-state">
          <h1 className="chat-empty-title">
            Hello there,
            <br />
            what can I help you find?
          </h1>
          <p className="chat-empty-subtitle">
            Start with a question, attach a file, or hold the mic to speak.
          </p>
        </div>
      )}

      {/* This invisible div is where we scroll to when new messages arrive */}
      <div ref={messagesEndRef} />
    </section>
  )
}

export default MessageList

