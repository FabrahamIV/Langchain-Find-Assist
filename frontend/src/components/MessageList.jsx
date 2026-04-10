function MessageList({ messages, messagesEndRef, isLoading }) {
  const hasMessages = (messages && messages.length > 0) || isLoading;

  return (
    <section className="flex-1 min-h-0 flex flex-col items-center justify-start px-6 max-w-5xl mx-auto w-full pt-8 pb-8 overflow-y-auto scroll-smooth no-scrollbar">
      {hasMessages ? (
        <div className="flex flex-col space-y-6 w-full mt-auto">
          {messages && messages.length > 0 && messages.map((message) => (
            <div key={message.id} className={`flex w-full ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`p-4 rounded-2xl max-w-[80%] shadow-sm ${
                message.role === 'user' 
                  ? 'bg-primary text-white rounded-br-sm' 
                  : 'bg-surface-container-highest dark:bg-slate-800 text-on-surface dark:text-slate-100 rounded-bl-sm border border-outline-variant/10 dark:border-slate-700'
              }`}>
                <div className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</div>
                {message.fileName && (
                  <div className="mt-2 text-xs flex items-center gap-2 opacity-90 bg-black/10 dark:bg-white/10 p-2 rounded-lg w-max">
                    <span className="material-symbols-outlined text-[16px]">attach_file</span>
                    <span>{message.fileName}</span>
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex w-full justify-start">
              <div className="p-4 rounded-2xl w-24 shadow-sm bg-surface-container-highest dark:bg-slate-800 rounded-bl-sm border border-outline-variant/10 dark:border-slate-700 flex items-center justify-center space-x-1 border opacity-80">
                <div className="w-2 h-2 bg-primary dark:bg-slate-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                <div className="w-2 h-2 bg-primary dark:bg-slate-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                <div className="w-2 h-2 bg-primary dark:bg-slate-400 rounded-full animate-bounce"></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center w-full my-auto">
          <div className="text-center mb-12 space-y-4">
            {/* <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-container/30 text-primary dark:bg-primary/20 mb-4">
              <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>bubbles</span>
              <span className="text-xs font-bold tracking-widest uppercase">System Ready</span>
            </div> */}
            <h2 className="text-5xl font-extrabold text-on-surface dark:text-slate-50 tracking-tight leading-[1.1]">
              Hi, this is my personal info page
            </h2>
            <p className="text-secondary dark:text-slate-400 body-lg max-w-lg mx-auto opacity-70">
              Ask me anything about my experience, skills, or projects.
            </p>
          </div>

          <div className="grid grid-cols-12 gap-4 w-full">
            <div className="col-span-7 bg-surface-container-low dark:bg-slate-900/50 p-6 rounded-3xl hover:bg-surface-container-high dark:hover:bg-slate-800 transition-all cursor-pointer group shadow-sm">
              <span className="material-symbols-outlined text-primary mb-3">auto_awesome</span>
              <h3 className="font-bold text-lg mb-2 dark:text-slate-100">Synthesize research</h3>
              <p className="text-sm text-secondary dark:text-slate-400 leading-relaxed">Create a comprehensive summary of the latest trends in sustainable architecture for 2024.</p>
            </div>
            <div className="col-span-5 bg-tertiary-container/20 dark:bg-slate-800/50 p-6 rounded-3xl hover:bg-tertiary-container/40 dark:hover:bg-slate-700 transition-all cursor-pointer group shadow-sm">
              <span className="material-symbols-outlined text-tertiary mb-3">code_blocks</span>
              <h3 className="font-bold text-lg mb-2 dark:text-slate-100">Review Code</h3>
              <p className="text-sm text-secondary dark:text-slate-400 leading-relaxed">Optimize my React component for performance.</p>
            </div>
            <div className="col-span-4 bg-surface-container-low dark:bg-slate-900/50 p-6 rounded-3xl hover:bg-surface-container-high dark:hover:bg-slate-800 transition-all cursor-pointer group shadow-sm">
              <span className="material-symbols-outlined text-primary mb-3">edit_note</span>
              <h3 className="font-bold text-lg mb-2 dark:text-slate-100">Draft Email</h3>
              <p className="text-sm text-secondary dark:text-slate-400 leading-relaxed">A polite follow-up for a project proposal.</p>
            </div>
            <div className="col-span-8 bg-surface-container-lowest dark:bg-slate-900 border border-outline-variant/10 dark:border-slate-800 p-6 rounded-3xl shadow-sm hover:shadow-md transition-all cursor-pointer group relative overflow-hidden">
              <div className="relative z-10">
                <span className="material-symbols-outlined text-primary mb-3">image</span>
                <h3 className="font-bold text-lg mb-2 dark:text-slate-100">Generate Visual Concept</h3>
                <p className="text-sm text-secondary dark:text-slate-400 leading-relaxed">Describe a futuristic minimalist workspace in a mountain cabin at dusk.</p>
              </div>
              <div className="absolute right-0 bottom-0 opacity-10 group-hover:opacity-20 transition-opacity">
                <span className="material-symbols-outlined text-9xl translate-x-8 translate-y-8">brush</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

export default MessageList;
