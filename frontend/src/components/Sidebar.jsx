// Sidebar: shows the list of conversations and the "New chat" button.
// It is a *presentational* component: it does not own state itself,
// it just receives data + callbacks from App via props.

function Sidebar({
  isOpen,
  onToggle,
  conversations,
  activeConversationId,
  onNewChat,
  onSelectConversation,
}) {
  return (
    <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      <div className="sidebar-header">
        <button className="sidebar-toggle" type="button" onClick={onToggle}>
          ☰
        </button>
      </div>

      <div className="sidebar-menu">
        <button className="new-chat-button" type="button" onClick={onNewChat}>
          <span className="new-chat-icon">＋</span>
          <span>New Chat</span>
        </button>
      </div>

      <div className="sidebar-section-label">Your Conversations</div>

      <nav className="sidebar-list">
        {conversations.map((conversation) => {
          const isActive = conversation.id === activeConversationId

          return (
            <button
              key={conversation.id}
              type="button"
              className={
                isActive
                  ? 'sidebar-item sidebar-item-active'
                  : 'sidebar-item'
              }
              // Let App know which conversation should become active.
              onClick={() => onSelectConversation(conversation.id)}
            >
              <span className="sidebar-item-title">
                {conversation.title || 'New Chat'}
              </span>
            </button>
          )
        })}
      </nav>
    </aside>
  )
}

export default Sidebar

