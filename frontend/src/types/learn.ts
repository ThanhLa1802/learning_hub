export interface Domain {
    id: string
    slug: string
    name: string
    description: string
    icon_name: string
    color: string
    order_index: number
    is_active: boolean
}

export interface Course {
    id: string
    domain_id: string
    slug: string
    name: string
    description: string
    order_index: number
    is_active: boolean
}

export interface DomainWithCourses extends Domain {
    courses: Course[]
}

export interface LessonSummary {
    id: string
    title: string
    content_type: 'explanation' | 'example' | 'exercise'
    order_index: number
    estimated_minutes: number
    category_id?: string
    is_completed?: boolean
}

export interface Lesson extends LessonSummary {
    content: string
    course_id: string
    quiz_id?: string
    is_completed?: boolean
    quiz_passed?: boolean
    next_lesson_id?: string
}

export interface QuizQuestion {
    id: string
    question: string
    options: string[]
    order_index: number
    // correct_answer_index is NOT included until after submission
}

export interface Quiz {
    id: string
    title: string
    description?: string
    order_index: number
    questions: QuizQuestion[]
}

export interface QuizQuestionResult {
    question_id: string
    is_correct: boolean
    correct_answer_index: number
    explanation: string
    your_answer_index: number
}

export interface QuizAttemptResult {
    score: number
    feedback: string
    results: QuizQuestionResult[]
}

export interface UserDomainProgress {
    domain_id: string
    domain_name: string
    sessions_completed: number
    lessons_completed: number
    total_lessons: number
    quizzes_taken: number
    avg_quiz_score: number
    last_activity_at?: string
}

export interface UserProgress {
    domains: UserDomainProgress[]
}

export interface AIExplainRequest {
    question: string
}

export interface AIExplainResponse {
    explanation: string
    key_points: string[]
    real_world_example: string
    interview_tip: string
}
