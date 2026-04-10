function ChatHeader() {
  return (
    <header className="flex justify-between items-center w-full px-6 py-4 bg-white/80 dark:bg-slate-950/80 backdrop-blur-xl font-['Manrope'] font-semibold tracking-tight top-0 sticky shadow-[0px_12px_32px_rgba(42,52,57,0.06)] z-40 relative">
      <div className="flex items-center gap-4">
        <span className="text-xl font-extrabold text-slate-900 dark:text-slate-50">Faisal Abraham</span>
        <span className="px-2 py-0.5 bg-tertiary-container text-amber-800 text-[10px] rounded-full uppercase tracking-tighter">V1.0</span>
      </div>
      <div className="flex items-center gap-2">
        <button 
          className="p-2 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors" 
          onClick={() => document.documentElement.classList.toggle('dark')}
        >
          <span className="material-symbols-outlined dark:!hidden">dark_mode</span>
          <span className="material-symbols-outlined !hidden dark:!block">light_mode</span>
        </button>
        <button className="p-2 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors">
          <span className="material-symbols-outlined">tune</span>
        </button>
        <div className="h-8 w-[1px] bg-slate-200 dark:bg-slate-800 mx-2"></div>
        <button className="flex items-center gap-2 pl-2 pr-1 py-1 rounded-full border border-slate-300 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
          <div className="w-8 h-8 rounded-full overflow-hidden">
            <img className="w-full h-full object-cover" alt="Profile" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDLGOF7K-iiq2msTW7K79Hm4lMb5uyrvr1W8tFGrdptlu3r73hMGYNTl1S0EUU8k4CaXgIn5iZYmu8LgJfsPB7hDQJo_Et5mdpY0pTlhPkbEe7ivkNj1i5BWZKaPcnN4v7RMl8r7F5beAN1epVw225xC4620q6ODP2vlEBDmmy1ldHNquXvYNXaid_VyJIpHbsak7jrH4utbbjgLwY0kJzTxcru70GGU4-zLmle7VIZlLohS7qnv1m3egmsN29uoZHOoNYVVYME4tvV" />
          </div>
          <span className="material-symbols-outlined text-slate-600 dark:text-slate-400">expand_more</span>
        </button>
      </div>
    </header>
  );
}

export default ChatHeader;
