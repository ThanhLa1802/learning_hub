'use client'

import { useState, useEffect } from 'react'

export type Lang = 'en' | 'vi'

const STORAGE_KEY = 'lang'

export function useLang() {
    const [lang, setLangState] = useState<Lang>('en')

    useEffect(() => {
        const stored = localStorage.getItem(STORAGE_KEY) as Lang | null
        if (stored === 'en' || stored === 'vi') {
            setLangState(stored)
        }
    }, [])

    const setLang = (next: Lang) => {
        setLangState(next)
        localStorage.setItem(STORAGE_KEY, next)
    }

    const toggle = () => setLang(lang === 'en' ? 'vi' : 'en')

    return { lang, setLang, toggle }
}
