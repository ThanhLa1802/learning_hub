export type PracticeMode = 'text_response' | 'ai_chat'
export type Difficulty = 'beginner' | 'intermediate' | 'advanced'
export type SessionStatus = 'in_progress' | 'completed'
export type MessageRole = 'user' | 'assistant'

export interface User {
    id: string
    email: string
    full_name: string
    is_active: boolean
    is_admin: boolean
    created_at: string
}

export interface ScenarioCategory {
    id: string
    name: string
    title: string
    description: string
    icon_name: string
    order_index: number
    course_id?: string | null
}

export interface Scenario {
    id: string
    category_id: string
    title: string
    description: string
    mode: PracticeMode
    difficulty: Difficulty
    tags: string[]
    order_index: number
    is_active: boolean
    category?: ScenarioCategory
}

export interface AIFeedback {
    overall_score: number
    grammar_score: number
    vocabulary_score: number
    professionalism_score: number
    it_appropriateness_score: number
    strengths: string[]
    improvements: string[]
    corrected_example: string
    natural_version: string
}

export interface SessionMessage {
    id: string
    session_id: string
    role: MessageRole
    content: string
    created_at: string
}

export interface PracticeSession {
    id: string
    scenario_id: string
    mode: PracticeMode
    status: SessionStatus
    started_at: string
    completed_at?: string
    overall_score?: number
    ai_feedback?: AIFeedback
    scenario?: Scenario
    messages: SessionMessage[]
}

export interface PaginatedResponse<T> {
    items: T[]
    total: number
    skip: number
    limit: number
}

export interface RegisterRequest {
    email: string
    password: string
    full_name: string
}

export interface LoginRequest {
    email: string
    password: string
}

export interface CreateSessionRequest {
    scenario_id: string
}

export interface AddMessageRequest {
    content: string
}

export interface CompleteSessionRequest {
    user_response?: string
    lang?: string
}
