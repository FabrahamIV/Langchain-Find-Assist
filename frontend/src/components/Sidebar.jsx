function Sidebar({
  isOpen,
  onToggle,
  conversations,
  activeConversationId,
  onNewChat,
  onSelectConversation,
  onDeleteConversation,
}) {
  return (
    <aside className={`fixed left-0 top-0 h-full flex flex-col p-4 space-y-2 bg-slate-100 dark:bg-slate-900 rounded-none tonal-shift no-border font-['Inter'] text-sm tracking-wide font-medium z-50 transition-all duration-300 overflow-hidden ${isOpen ? 'w-80' : 'w-20'}`}>
      <div className={`flex ${isOpen ? 'items-center justify-between px-2' : 'flex-col items-center gap-6 mt-2'} mb-8`}>
        <div className={`flex items-center gap-3 ${!isOpen && 'justify-center'}`}>
          <div className="w-10 h-10 bg-primary min-w-[40px] rounded-xl flex items-center justify-center shadow-lg shadow-primary/20 shrink-0">
            <span className="material-symbols-outlined text-white" style={{ fontVariationSettings: "'FILL' 1" }}>dataset</span>
          </div>
          {/* {isOpen && (
            <div className="whitespace-nowrap">
              <h1 className="font-['Manrope'] font-bold text-slate-900 dark:text-slate-50 text-base leading-none">Find-Assist</h1>
              <p className="text-[10px] text-slate-500 dark:text-slate-400 uppercase tracking-widest mt-1">Intelligence Suite</p>
            </div>
          )} */}
        </div>
        <button onClick={onToggle} className="p-2 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-lg transition-colors shrink-0">
          <span className="material-symbols-outlined text-slate-500">{isOpen ? 'menu_open' : 'menu'}</span>
        </button>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto overflow-x-hidden no-scrollbar">
        <button onClick={onNewChat} className={`w-full flex items-center bg-white dark:bg-slate-800 text-blue-600 dark:text-blue-400 rounded-xl py-3 shadow-sm scale-95 active:scale-100 duration-150 transition-all group ${isOpen ? 'gap-3 px-4' : 'justify-center px-0'}`} title={!isOpen ? "New Chat" : undefined}>
          <span className="material-symbols-outlined shrink-0">add_circle</span>
          {isOpen && <span className="font-semibold whitespace-nowrap">New Chat</span>}
        </button>

        {isOpen && (
          <div className="pt-4 pb-2 px-2 text-[10px] text-slate-500 dark:text-slate-400 uppercase tracking-widest">
              History
          </div>
        )}
        
        {conversations.map((conversation) => {
          const isActive = conversation.id === activeConversationId;
          return (
            <div
              key={conversation.id}
              className={`w-full flex items-center rounded-xl transition-all group ${isOpen ? 'gap-3 px-4 py-3' : 'justify-center py-3 px-0'} ${
                isActive
                  ? 'bg-slate-200 dark:bg-slate-800 text-blue-600 dark:text-blue-400'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800'
              }`}
              title={!isOpen ? conversation.title || 'New Chat' : undefined}
            >
              <button
                onClick={() => onSelectConversation(conversation.id)}
                className={`flex items-center flex-1 min-w-0 text-left ${isOpen ? 'gap-3' : 'justify-center'}`}
              >
                <span className="material-symbols-outlined shrink-0">history</span>
                {isOpen && <span className="truncate">{conversation.title || 'New Chat'}</span>}
              </button>
              {isOpen && onDeleteConversation && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteConversation(conversation.id);
                  }}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-500 transition-all rounded-lg hover:bg-red-50 dark:hover:bg-red-500/10 shrink-0"
                  title="Delete conversation"
                >
                  <span className="material-symbols-outlined text-[18px]">delete</span>
                </button>
              )}
            </div>
          );
        })}
      </nav>

      {/* <div className="px-2 py-4">
        <div className="bg-gradient-to-br from-primary to-primary-dim p-4 rounded-2xl text-white shadow-xl shadow-primary/10">
          <p className="text-xs opacity-80 mb-2">Access advanced models</p>
          <button className="w-full py-2 bg-white/20 hover:bg-white/30 backdrop-blur-md rounded-lg text-sm font-bold transition-colors">
            Upgrade to Pro
          </button>
        </div>
      </div> */}

      <div className="pt-4 border-t border-slate-200 dark:border-slate-800 space-y-1">
        <button onClick={() => document.documentElement.classList.toggle('dark')} className={`w-full flex items-center text-slate-600 dark:text-slate-400 py-3 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-xl transition-all group ${isOpen ? 'gap-3 px-4' : 'justify-center px-0'}`} title={!isOpen ? "Toggle Theme" : undefined}>
          <span className="material-symbols-outlined dark:!hidden shrink-0">dark_mode</span>
          <span className="material-symbols-outlined !hidden dark:!block shrink-0">light_mode</span>
          {isOpen && (
            <>
              <span className="dark:hidden whitespace-nowrap">Dark Mode</span>
              <span className="hidden dark:block whitespace-nowrap">Light Mode</span>
            </>
          )}
        </button>
        <button className={`w-full flex items-center text-slate-600 dark:text-slate-400 py-3 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-xl transition-all group ${isOpen ? 'gap-3 px-4' : 'justify-center px-0'}`} title={!isOpen ? "Settings" : undefined}>
          <span className="material-symbols-outlined shrink-0">settings</span>
          {isOpen && <span className="whitespace-nowrap">Settings</span>}
        </button>
        <button className={`w-full flex items-center text-slate-600 dark:text-slate-400 py-3 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-xl transition-all group ${isOpen ? 'gap-3 px-4' : 'justify-center px-0'}`} title={!isOpen ? "Help" : undefined}>
          <span className="material-symbols-outlined shrink-0">help_outline</span>
          {isOpen && <span className="whitespace-nowrap">Help</span>}
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;
