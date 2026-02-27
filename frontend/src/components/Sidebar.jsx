// Sidebar: shows the list of conversations and the "New chat" button.
// It is a *presentational* component: it does not own state itself,
// it just receives data + callbacks from App via props.

function Sidebar({
  conversations,
  activeConversationId,
  onNewChat,
  onSelectConversation,
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <button className="new-chat-button" type="button" onClick={onNewChat}>
          <span className="new-chat-icon">＋</span>
          <span>New chat</span>
        </button>
      </div>

      <div className="sidebar-section-label">History</div>

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
                {conversation.title || 'New chat'}
              </span>
            </button>
          )
        })}
      </nav>
    </aside>
  )
}

export default Sidebar

