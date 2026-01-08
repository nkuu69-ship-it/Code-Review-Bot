import { Sparkles } from "lucide-react"

export function Header() {
  return (
    <header className="h-14 border-b border-border bg-card flex items-center px-6">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center">
          <Sparkles className="w-5 h-5 text-accent-foreground" />
        </div>
        <h1 className="text-lg font-semibold text-foreground">AI Code Review Bot</h1>
      </div>
    </header>
  )
}
