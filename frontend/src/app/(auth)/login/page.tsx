import Link from 'next/link'
import { LoginForm } from '@/components/auth/LoginForm'
import { BookOpen } from 'lucide-react'
import { ButtonLink } from '@/components/ui/button-link'

export default function LoginPage() {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center gap-6 p-4">
            <Link href="/" className="flex items-center gap-2 text-xl font-semibold">
                <BookOpen className="h-6 w-6 text-primary" />
                DevEnglish
            </Link>
            <LoginForm />
            <p className="text-sm text-muted-foreground">
                Don&apos;t have an account?{' '}
                <Link href="/register" className="text-primary underline underline-offset-4">
                    Sign up
                </Link>
            </p>
        </div>
    )
}
