"use client"

import { useState } from "react"
import { CodeEditor } from "@/components/code-editor"
import { ReviewResults } from "@/components/review-results"
import { Header } from "@/components/header"
import { toast } from "sonner"

export interface ReviewIssue {
  line: number
  severity: "Bug" | "Warning" | "Improvement" | "Security"
  explanation: string
  suggested_fix: string
}

interface AutoFixResponse {
  fixed_code: string
  summary: string
  changes: {
    line: number | null
    before: string
    after: string
    reason: string
  }[]
}

export default function Home() {
  const [code, setCode] = useState("")
  const [language, setLanguage] = useState("python")
  const [isReviewing, setIsReviewing] = useState(false)
  const [isFixing, setIsFixing] = useState(false)
  const [issues, setIssues] = useState<ReviewIssue[]>([])
  const [error, setError] = useState<string | null>(null)

  const handleReview = async () => {
    if (!code.trim()) {
      return
    }

    setIsReviewing(true)
    setError(null)

    try {
      const response = await fetch("/api/review", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code, language }),
      })

      if (!response.ok) {
        throw new Error("Failed to review code")
      }

      const data = await response.json()
      setIssues(data.issues || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
      setIssues([])
    } finally {
      setIsReviewing(false)
    }
  }

  const handleAutoFix = async () => {
    if (!code.trim()) return

    setIsFixing(true)
    try {
      const response = await fetch("/api/auto-fix", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code, language }),
      })

      if (!response.ok) {
        let errorMessage = "Failed to auto-fix code"
        try {
          const errorData = await response.json()
          if (errorData.detail) errorMessage = errorData.detail
        } catch (e) { }
        throw new Error(errorMessage)
      }

      const data: AutoFixResponse = await response.json()
      setCode(data.fixed_code)
      toast.success("Code fixed successfully!", {
        description: data.summary,
        duration: 5000,
      })
      // Clear previous issues as they might be resolved
      setIssues([])
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to auto-fix code")
    } finally {
      setIsFixing(false)
    }
  }

  const handleClear = () => {
    setCode("")
    setIssues([])
    setError(null)
  }

  return (
    <div className="flex flex-col h-screen bg-background">
      <Header />

      <div className="flex flex-1 overflow-hidden">
        <div className="flex-[7] flex flex-col border-r border-border">
          <CodeEditor
            code={code}
            language={language}
            onCodeChange={setCode}
            onLanguageChange={setLanguage}
            onReview={handleReview}
            onAutoFix={handleAutoFix}
            onClear={handleClear}
            isReviewing={isReviewing}
            isFixing={isFixing}
          />
        </div>

        <div className="flex-[3] flex flex-col">
          <ReviewResults issues={issues} isReviewing={isReviewing} error={error} />
        </div>
      </div>
    </div>
  )
}
