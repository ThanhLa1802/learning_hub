'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

export type Lang = 'en' | 'vi'

const STORAGE_KEY = 'lang'

interface LangContextValue {
    lang: Lang
    toggle: () => void
}

const LangContext = createContext<LangContextValue>({
    lang: 'en',
    toggle: () => { },
})

export function LangProvider({ children }: { children: ReactNode }) {
    const [lang, setLang] = useState<Lang>('en')

    useEffect(() => {
        const stored = localStorage.getItem(STORAGE_KEY) as Lang | null
        if (stored === 'en' || stored === 'vi') {
            setLang(stored)
        }
    }, [])

    const toggle = () => {
        const next: Lang = lang === 'en' ? 'vi' : 'en'
        setLang(next)
        localStorage.setItem(STORAGE_KEY, next)
    }

    return <LangContext.Provider value={{ lang, toggle }}>{children}</LangContext.Provider>
}

export function useLang(): LangContextValue {
    return useContext(LangContext)
}
