import Link from 'next/link'
import { RegisterForm } from '@/components/auth/RegisterForm'
import { BookOpen } from 'lucide-react'
import { ButtonLink } from '@/components/ui/button-link'

export default function RegisterPage() {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center gap-6 p-4">
            <Link href="/" className="flex items-center gap-2 text-xl font-semibold">
                <BookOpen className="h-6 w-6 text-primary" />
                DevEnglish
            </Link>
            <RegisterForm />
            <p className="text-sm text-muted-foreground">
                Already have an account?{' '}
                <Link href="/login" className="text-primary underline underline-offset-4">
                    Sign in
                </Link>
            </p>
        </div>
    )
}
