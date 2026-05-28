import Link from 'next/link'
import { BookOpen, MessageSquare, TrendingUp, Code2, Users, Zap } from 'lucide-react'
import { ButtonLink } from '@/components/ui/button-link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const FEATURES = [
  { icon: MessageSquare, title: 'AI Roleplay Conversations', description: 'Chat with an AI playing a Python interviewer, demanding client, or engineering manager.' },
  { icon: TrendingUp, title: 'Scored Feedback', description: 'Receive scores for grammar, vocabulary, professionalism, and IT appropriateness.' },
  { icon: Code2, title: 'Real IT Scenarios', description: '7 categories covering daily standups, system design interviews, code reviews, and more.' },
]

const SCENARIOS = ['Daily Standup', 'Client Meetings', 'Explaining Bugs', 'Python Interview', 'AWS System Design', 'Code Review', 'Technical Solutions']

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-border bg-card/50 backdrop-blur sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2 font-semibold text-lg">
            <BookOpen className="h-5 w-5 text-primary" />
            DevEnglish
          </div>
          <div className="flex items-center gap-2">
            <ButtonLink href="/login" variant="ghost" size="sm">Sign in</ButtonLink>
            <ButtonLink href="/register" size="sm">Get started</ButtonLink>
          </div>
        </div>
      </header>

      <main className="flex-1">
        <section className="max-w-6xl mx-auto px-4 py-20 text-center space-y-6">
          <Badge variant="secondary" className="text-xs">
            <Zap className="h-3 w-3 mr-1" />
            AI-powered English practice for developers
          </Badge>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight max-w-3xl mx-auto leading-tight">
            Speak English confidently<br />
            <span className="text-primary">in every IT situation</span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-xl mx-auto">
            Practice real workplace scenarios - standups, client calls, interviews, code reviews - and get instant AI feedback on your professional English.
          </p>
          <div className="flex items-center justify-center gap-3 flex-wrap">
            <ButtonLink href="/register" size="lg">Start for free</ButtonLink>
            <ButtonLink href="/login" size="lg" variant="outline">Sign in</ButtonLink>
          </div>
          <div className="flex flex-wrap justify-center gap-2 pt-2">
            {SCENARIOS.map((s) => <Badge key={s} variant="outline" className="text-xs">{s}</Badge>)}
          </div>
        </section>

        <section className="max-w-6xl mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {FEATURES.map((f) => (
              <Card key={f.title} className="bg-card/50">
                <CardHeader>
                  <div className="p-2 rounded-md bg-primary/10 text-primary w-fit mb-2">
                    <f.icon className="h-5 w-5" />
                  </div>
                  <CardTitle className="text-base">{f.title}</CardTitle>
                </CardHeader>
                <CardContent><CardDescription>{f.description}</CardDescription></CardContent>
              </Card>
            ))}
          </div>
        </section>

        <section className="max-w-6xl mx-auto px-4 py-16 text-center space-y-4">
          <Users className="h-5 w-5 text-primary mx-auto" />
          <h2 className="text-2xl font-bold">Ready to level up your IT English?</h2>
          <p className="text-muted-foreground">Join developers practising professional communication every day.</p>
          <ButtonLink href="/register" size="lg">Create free account</ButtonLink>
        </section>
      </main>

      <footer className="border-t border-border py-6 text-center text-sm text-muted-foreground">
        {new Date().getFullYear()} DevEnglish - English practice for IT developers
      </footer>
    </div>
  )
}
