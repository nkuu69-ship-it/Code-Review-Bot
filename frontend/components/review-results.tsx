import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, CheckCircle, Loader2 } from "lucide-react"
import type { ReviewIssue } from "@/app/page"

interface ReviewResultsProps {
  issues: ReviewIssue[]
  isReviewing: boolean
  error: string | null
}

const severityConfig = {
  Bug: { color: "bg-red-500/10 text-red-500 border-red-500/20", icon: AlertCircle },
  Warning: { color: "bg-yellow-500/10 text-yellow-500 border-yellow-500/20", icon: AlertCircle },
  Improvement: { color: "bg-blue-500/10 text-blue-500 border-blue-500/20", icon: AlertCircle },
  Security: { color: "bg-purple-500/10 text-purple-500 border-purple-500/20", icon: AlertCircle },
}

export function ReviewResults({ issues, isReviewing, error }: ReviewResultsProps) {
  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-3 border-b border-border bg-card/50">
        <h2 className="text-sm font-semibold text-foreground">Review Results</h2>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {isReviewing && (
          <div className="flex flex-col items-center justify-center h-full text-muted-foreground">
            <Loader2 className="w-8 h-8 animate-spin mb-2" />
            <p className="text-sm">Analyzing your code...</p>
          </div>
        )}

        {error && (
          <Card className="p-4 bg-destructive/10 border-destructive/20">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-destructive mt-0.5" />
              <div>
                <h3 className="font-semibold text-destructive mb-1">Error</h3>
                <p className="text-sm text-destructive/90">{error}</p>
              </div>
            </div>
          </Card>
        )}

        {!isReviewing && !error && issues.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-muted-foreground">
            <CheckCircle className="w-12 h-12 mb-3 text-green-500" />
            <p className="text-sm font-medium">No issues found</p>
            <p className="text-xs mt-1">Your code looks great!</p>
          </div>
        )}

        {!isReviewing && issues.length > 0 && (
          <>
            {issues.map((issue, index) => {
              const config = severityConfig[issue.severity]
              const Icon = config.icon

              return (
                <Card key={index} className="p-4 hover:bg-accent/5 transition-colors">
                  <div className="space-y-3">
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <Badge className={`${config.color} border`}>
                          <Icon className="w-3 h-3 mr-1" />
                          {issue.severity}
                        </Badge>
                        <span className="text-xs text-muted-foreground">Line {issue.line}</span>
                      </div>
                    </div>

                    <div>
                      <p className="text-sm text-foreground leading-relaxed">{issue.explanation}</p>
                    </div>

                    {issue.suggested_fix && (
                      <div>
                        <p className="text-xs font-medium text-muted-foreground mb-2">Suggested fix:</p>
                        <div className="bg-muted/50 rounded-md p-3 border border-border">
                          <code className="text-xs font-mono text-foreground whitespace-pre-wrap break-words">
                            {issue.suggested_fix}
                          </code>
                        </div>
                      </div>
                    )}
                  </div>
                </Card>
              )
            })}
          </>
        )}
      </div>
    </div>
  )
}
