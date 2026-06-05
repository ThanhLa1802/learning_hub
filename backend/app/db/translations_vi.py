"""
Vietnamese translations for all seeded content.
Structure: { "vi": { translatable_fields } }
Used by seed_translations() to UPDATE existing DB records.
"""

DOMAIN_TRANSLATIONS_VI: dict[str, dict] = {
    "english-it": {
        "name": "Tiếng Anh cho Lập trình viên IT",
        "description": "Thành thạo giao tiếp tiếng Anh chuyên nghiệp cho lập trình viên — standup, họp khách hàng, code review và phỏng vấn kỹ thuật.",
    },
    "system-design": {
        "name": "Thiết kế Hệ thống",
        "description": "Học cách thiết kế hệ thống phân tán có khả năng mở rộng và đáng tin cậy. Cần thiết cho phỏng vấn senior và quyết định kiến trúc thực tế.",
    },
}

COURSE_TRANSLATIONS_VI: dict[str, dict] = {
    "english-it-essentials": {
        "name": "Tiếng Anh IT Cơ bản",
        "description": "Kỹ năng giao tiếp tiếng Anh cốt lõi dành cho lập trình viên phần mềm.",
    },
    "system-design-fundamentals": {
        "name": "Nền tảng Thiết kế Hệ thống",
        "description": "Nắm vững các khái niệm cốt lõi của hệ thống phân tán có khả năng mở rộng.",
    },
}

CATEGORY_TRANSLATIONS_VI: dict[str, dict] = {
    "daily_standup": {
        "title": "Daily Standup",
        "description": "Thực hành cập nhật công việc, blockers và kế hoạch hàng ngày một cách rõ ràng và chuyên nghiệp.",
    },
    "client_meeting": {
        "title": "Họp với Khách hàng",
        "description": "Xử lý kỳ vọng khách hàng, giải thích chậm trễ và truyền đạt khái niệm kỹ thuật cho người không chuyên.",
    },
    "bug_explanation": {
        "title": "Giải thích Lỗi & Sự cố",
        "description": "Báo cáo lỗi rõ ràng, leo thang sự cố production chuyên nghiệp và viết post-mortem.",
    },
    "technical_solution": {
        "title": "Đề xuất Giải pháp Kỹ thuật",
        "description": "Đề xuất phương án kỹ thuật, biện hộ cho lựa chọn công nghệ và giải thích quyết định kiến trúc.",
    },
    "python_interview": {
        "title": "Phỏng vấn Python Developer",
        "description": "Thực hành tiếng Anh cho phỏng vấn kỹ thuật Python — từ vòng screening junior đến senior architect.",
    },
    "aws_system_design": {
        "title": "AWS & Thiết kế Hệ thống",
        "description": "Thảo luận kiến trúc AWS, các đánh đổi trong thiết kế hệ thống và tối ưu chi phí cloud.",
    },
    "code_review": {
        "title": "Giao tiếp Code Review",
        "description": "Yêu cầu review chuyên nghiệp, phản hồi feedback và đưa ra nhận xét mang tính xây dựng.",
    },
    # SD categories
    "load_balancing": {
        "title": "Cân bằng Tải",
        "description": "Phân phối lưu lượng giữa các server để đạt hiệu suất cao và tính sẵn sàng cao.",
    },
    "caching": {
        "title": "Các Chiến lược Caching",
        "description": "Tăng tốc hệ thống và giảm tải database với các pattern caching hiệu quả.",
    },
    "microservices_sd": {
        "title": "Kiến trúc Microservices",
        "description": "Chia nhỏ monolith thành các service độc lập và quản lý sự phức tạp phát sinh.",
    },
    "database_scaling_sd": {
        "title": "Scale Database",
        "description": "Scale cơ sở dữ liệu quan hệ và NoSQL để phục vụ hàng triệu người dùng.",
    },
    "cap_theorem_sd": {
        "title": "Định lý CAP",
        "description": "Hiểu các đánh đổi cơ bản trong hệ thống phân tán.",
    },
    "message_queue_sd": {
        "title": "Message Queue",
        "description": "Tách rời các service và xử lý khối lượng công việc bất đồng bộ với hệ thống hàng đợi.",
    },
    "api_gateway_sd": {
        "title": "API Gateway",
        "description": "Thiết kế điểm vào cho microservices với routing, auth và rate limiting.",
    },
    "cdn_sd": {
        "title": "Mạng phân phối nội dung (CDN)",
        "description": "Phục vụ tài nguyên tĩnh và giảm latency toàn cầu với CDN.",
    },
    "sql_vs_nosql_sd": {
        "title": "SQL vs NoSQL",
        "description": "Chọn loại database phù hợp cho từng use case.",
    },
    "rate_limiting_sd": {
        "title": "Rate Limiting",
        "description": "Bảo vệ API khỏi lạm dụng và đảm bảo sử dụng công bằng.",
    },
    "distributed_transactions_sd": {
        "title": "Giao dịch Phân tán",
        "description": "Duy trì nhất quán dữ liệu qua nhiều service và database.",
    },
    "event_driven_sd": {
        "title": "Kiến trúc Hướng Sự kiện",
        "description": "Xây dựng hệ thống phản ứng, loose coupling với các pattern hướng sự kiện.",
    },
    "websocket_sd": {
        "title": "WebSockets & Thời gian thực",
        "description": "Xây dựng tính năng real-time với WebSockets và Server-Sent Events.",
    },
    "monolith_vs_microservices_sd": {
        "title": "Monolith vs Microservices",
        "description": "Khi nào nên tách monolith và cách thực hiện an toàn.",
    },
}

# ── English IT Lesson translations ────────────────────────────────────────────

ENGLISH_IT_LESSON_TRANSLATIONS_VI: dict[str, dict] = {
    "daily_standup": {
        "lesson": {
            "title": "Daily Standup: Cấu trúc và Cụm từ Quan trọng",
            "content": """# Giao tiếp trong Daily Standup

Daily standup là buổi họp đồng bộ 15 phút của cả team. Mỗi lập trình viên đều phát biểu. Từng câu chữ đều quan trọng.

## Công thức 3 Câu hỏi
1. **Hôm qua** — Bạn đã hoàn thành gì?
2. **Hôm nay** — Bạn sẽ làm gì?
3. **Blockers** — Điều gì đang cản trở bạn?

## Từ vựng: Công việc đã hoàn thành
- ✅ "Hôm qua tôi đã **hoàn thành** login API và **merge** PR của mình."
- ✅ "Tôi đã **wrap up** phần database migration."
- ✅ "Tôi đã **resolve** cái bug xác thực từ sprint trước."
- ❌ Tránh: "Tôi đã làm vài thứ liên quan đến cái login."

## Từ vựng: Kế hoạch hôm nay
- ✅ "Hôm nay tôi sẽ **work on** phần tích hợp payment."
- ✅ "Tôi dự định **review** PR của John và **bắt đầu** làm caching layer."
- ✅ "Hôm nay tôi tập trung **hoàn thành** unit test cho user service."

## Từ vựng: Blockers
- ✅ "Tôi đang **blocked on** tài liệu API — cần có nó trước khi tiếp tục được."
- ✅ "Tôi có **dependency** vào team thiết kế. Đang đợi mockup mới."
- ✅ "Tôi đang **stuck on** một vấn đề phân quyền. Tôi sẽ post lên Slack sau standup."
- ❌ Tránh: "Tôi không biết phải làm gì." → Quá chung chung. Luôn nói rõ *bạn cần gì*.

## Mẹo chuyên nghiệp
- Giữ trong vòng 60 giây mỗi người
- Nói tên **task cụ thể**, không mô tả mơ hồ: "user authentication module" thay vì "cái login đó"
- Nếu bị block, hãy ngay lập tức nói **ai** bạn cần hoặc **cần gì**
- Đừng giải quyết vấn đề trong standup — đặt lịch theo dõi riêng

## Ví dụ: Standup Update hoàn chỉnh
> "Hôm qua tôi đã hoàn thành luồng đặt lại mật khẩu và sửa một critical bug trong logic hết hạn session. Hôm nay tôi sẽ bắt đầu tích hợp Stripe payment API và review 2 PR đang mở. Hiện tại không có blocker nào."

## Mẹo phỏng vấn
Trong phỏng vấn tiếng Anh, bạn có thể được yêu cầu thực hiện mock standup. Hãy luyện tập nói ngắn gọn và cụ thể. Interviewer đánh giá cao kỹ sư giao tiếp rõ ràng và nhận biết blocker sớm.""",
        },
        "quiz": {
            "title": "Quiz: Daily Standup",
            "description": "Kiểm tra kỹ năng giao tiếp standup của bạn.",
            "questions": [
                {
                    "question": "Câu nào giao tiếp blocker một cách chuyên nghiệp nhất?",
                    "options": [
                        "Tôi không biết phải làm gì tiếp theo.",
                        "Tôi đang bị blocked vì chờ tài liệu API từ team backend.",
                        "Có một vấn đề tôi không giải quyết được.",
                        "Công việc của tôi hôm nay chậm.",
                    ],
                    "explanation": "'Blocked on X — waiting for Y' nói rõ bạn cần gì và ai có thể giúp. Interviewer và đồng đội có thể hành động ngay.",
                },
                {
                    "question": "'Wrapped up' có nghĩa gì trong ngữ cảnh standup?",
                    "options": [
                        "Bắt đầu một task mới",
                        "Đặt lịch một cuộc họp",
                        "Hoàn thành một việc gì đó",
                        "Tạo một wrap component",
                    ],
                    "explanation": "'Wrapped up' có nghĩa là đã hoàn thành. 'I wrapped up the migration' = 'Tôi đã hoàn thành migration.'",
                },
                {
                    "question": "Standup nào chuyên nghiệp nhất?",
                    "options": [
                        "Tôi đã làm vài thứ trên user module.",
                        "Hôm qua tôi hoàn thành user auth API và merge PR. Hôm nay tôi sẽ bắt đầu payment service. Không có blocker.",
                        "Hôm qua đang làm login và hôm nay có thể làm payments.",
                        "Xong login rồi. Tiếp theo là payments. Ổn cả.",
                    ],
                    "explanation": "Lựa chọn thứ hai theo đúng công thức 3 câu hỏi, dùng tên task cụ thể và nói ngắn gọn.",
                },
                {
                    "question": "Update standup của một lập trình viên nên kéo dài bao lâu?",
                    "options": [
                        "5 phút",
                        "30 giây đến 1 phút",
                        "2 đến 3 phút",
                        "Bao lâu cũng được miễn là giải thích đầy đủ",
                    ],
                    "explanation": "Standup có giới hạn thời gian. Mỗi người nên nói dưới 60 giây. Thảo luận chi tiết diễn ra sau standup.",
                },
                {
                    "question": "Nên nói gì khi đang chờ input từ team khác?",
                    "options": [
                        "Tôi đang bị blocked.",
                        "Tôi có dependency vào team thiết kế — đang chờ mockup mới.",
                        "Ai đó cần giúp tôi.",
                        "Tôi sẽ tự xử lý.",
                    ],
                    "explanation": "Luôn nêu tên dependency và bạn đang chờ gì. 'Dependency on X — waiting for Y' giúp team có ngữ cảnh để hỗ trợ.",
                },
            ],
        },
    },
    "client_meeting": {
        "lesson": {
            "title": "Họp Khách hàng: Tính Chuyên nghiệp và Rõ ràng",
            "content": """# Tiếng Anh trong Cuộc họp Khách hàng

Cuộc họp khách hàng có mức độ rủi ro cao. Một câu nói sai có thể phá vỡ niềm tin. Hãy thành thạo các mẫu câu sau.

## Quản lý Sự chậm trễ
Đừng nói: ~~"Bị delay vì technical debt."~~ — khách hàng không hiểu thuật ngữ này.

✅ Thay bằng:
> "Chúng tôi phát hiện ra sự phức tạp trong codebase hiện tại đòi hỏi thêm thời gian để xử lý an toàn. Chúng tôi muốn bàn giao giải pháp đáng tin cậy, nên đang điều chỉnh timeline thêm hai tuần."

## Quản lý Kỳ vọng
- ✅ "Dựa trên ước tính hiện tại, chúng tôi dự kiến bàn giao vào **[ngày]**, nhưng tôi sẽ xác nhận sau khi hoàn thành giai đoạn thiết kế."
- ✅ "Tôi thà đưa ra timeline thực tế còn hơn hứa hẹn điều không thể đảm bảo."
- ❌ Tránh: "Tôi không chắc" mà không có câu tiếp theo — luôn thêm "Tôi sẽ kiểm tra và phản hồi trước [thời gian]."

## Giải thích Khái niệm Kỹ thuật Đơn giản

**Ví dụ về API:**
> "API giống như người phục vụ trong nhà hàng. App của bạn là khách, database là nhà bếp. Người phục vụ (API) nhận đơn, vào bếp, và mang ra đúng thứ bạn yêu cầu — mà không cần bạn vào bếp."

**Tại sao cần 3 tuần:**
> "Xây dựng API đúng chuẩn không chỉ là viết code — còn bao gồm bảo mật, xử lý lỗi, tài liệu và kiểm thử. Hãy nghĩ như xây cầu chứ không phải đường mòn. Làm đúng thì nó sẽ chịu được mọi thứ đặt lên trên."

## Xử lý Câu hỏi Khó
| Câu hỏi | Phản hồi Chuyên nghiệp |
|----------|---------|
| "Tại sao bị trễ?" | "Chúng tôi phát hiện sự phức tạp cần xử lý đúng. Ưu tiên của chúng tôi là chất lượng và liên tục kinh doanh của bạn." |
| "Có thể nhanh hơn không?" | "Chúng tôi có thể giảm phạm vi bản phát hành đầu tiên. Tính năng quan trọng nhất cho launch của bạn là gì?" |
| "Tại sao chi phí cao vậy?" | "Tôi có thể giải thích chi tiết. [giải thích]. Chúng ta cũng có thể thảo luận về phân chia công việc theo từng giai đoạn nếu phù hợp với ngân sách." |

## Cụm từ Chính
- "Để tôi làm rõ điều đó..."
- "Tóm tắt những gì tôi hiểu được..."
- "Tôi muốn đảm bảo chúng ta đồng thuận về..."
- "Tôi sẽ theo dõi bằng văn bản sau cuộc gọi này."

## Mẹo phỏng vấn
Interviewer thường test giao tiếp khách hàng với các tình huống như: "Bạn sẽ giải thích thế nào nếu trễ 2 tuần?" Luyện tập dùng ngôn ngữ kinh doanh, không phải lý do kỹ thuật.""",
        },
        "quiz": {
            "title": "Quiz: Giao tiếp Khách hàng",
            "description": "Kiểm tra kỹ năng giao tiếp khách hàng chuyên nghiệp của bạn.",
            "questions": [
                {
                    "question": "Khách hàng hỏi tại sao dự án bị trễ. Phản hồi nào chuyên nghiệp nhất?",
                    "options": [
                        "Vì technical debt trong code cũ.",
                        "Chúng tôi phát hiện sự phức tạp bất ngờ đòi hỏi thêm thời gian để xử lý đúng cách.",
                        "Khó giải thích lắm.",
                        "Developer trước đã làm sai.",
                    ],
                    "explanation": "Giải thích bằng ngôn ngữ kinh doanh, tập trung vào chất lượng, tránh đổ lỗi. Không dùng thuật ngữ chưa giải thích như 'technical debt' với khách hàng.",
                },
                {
                    "question": "'Scope down' có nghĩa gì trong giao tiếp với khách hàng?",
                    "options": [
                        "Tăng độ phức tạp của dự án",
                        "Thêm tính năng",
                        "Giảm tính năng để bàn giao nhanh hơn",
                        "Hủy dự án",
                    ],
                    "explanation": "Scoping down nghĩa là giảm phạm vi bản phát hành để có thể bàn giao chức năng cốt lõi nhanh hơn.",
                },
                {
                    "question": "Khách hàng hỏi ngày bàn giao cụ thể trong khi bạn chưa chắc chắn. Nên nói gì?",
                    "options": [
                        "Tôi không biết.",
                        "Chúng tôi sẽ cố gắng hết sức.",
                        "Dựa trên ước tính hiện tại, tôi dự kiến X, và sẽ xác nhận sau khi hoàn thành giai đoạn thiết kế.",
                        "Có thể tháng sau.",
                    ],
                    "explanation": "Đưa ra ước tính có điều kiện kèm cam kết cụ thể để follow up. 'Dựa trên X, tôi dự kiến Y, và sẽ xác nhận trước Z' là phong cách chuyên nghiệp.",
                },
                {
                    "question": "Phép so sánh nào tốt nhất khi giải thích API cho khách hàng không chuyên kỹ thuật?",
                    "options": [
                        "Đó là giao thức qua HTTP theo chuẩn REST.",
                        "Giống người phục vụ — nhận yêu cầu, vào bếp, mang ra kết quả.",
                        "Đó là code interface.",
                        "Đó là middleware giữa các layer.",
                    ],
                    "explanation": "Phép so sánh từ cuộc sống hàng ngày (người phục vụ, cây cầu...) giúp khái niệm kỹ thuật trở nên dễ hiểu ngay với người không chuyên.",
                },
                {
                    "question": "Sau cuộc họp khách hàng, bạn luôn nên làm gì?",
                    "options": [
                        "Gửi lời mời lịch họp.",
                        "Follow up bằng văn bản tóm tắt các quyết định và bước tiếp theo.",
                        "Chờ khách hàng liên hệ lại.",
                        "Cập nhật code ngay.",
                    ],
                    "explanation": "Follow up bằng văn bản sau cuộc họp xác nhận thỏa thuận, bảo vệ cả hai bên và thể hiện tính chuyên nghiệp.",
                },
            ],
        },
    },
    "bug_explanation": {
        "lesson": {
            "title": "Giải thích Lỗi & Sự cố một cách Chuyên nghiệp",
            "content": """# Tiếng Anh Báo cáo Lỗi và Leo thang Sự cố

Sự rõ ràng và chuyên nghiệp trong báo cáo lỗi và giao tiếp sự cố là điểm phân biệt kỹ sư tốt và kỹ sư xuất sắc.

## Cấu trúc Báo cáo Lỗi
1. **Điều gì đã xảy ra** (hành vi quan sát được)
2. **Điều gì nên xảy ra** (hành vi mong đợi)
3. **Các bước tái hiện**
4. **Tác động** (ai/cái gì bị ảnh hưởng)
5. **Nguyên nhân có thể** (giả thuyết)
6. **Những gì đã thử**

## Cụm từ Quan trọng: Báo cáo Lỗi
- ✅ "Tôi phát hiện bug trong luồng payment. Khi user submit với thẻ hết hạn, hệ thống **trả về** lỗi 500 thay vì thông báo validation."
- ✅ "Vấn đề **có vẻ nằm ở** logic hết hạn session — session đang hết hạn sớm hơn cấu hình."
- ✅ "Điều này **ảnh hưởng đến** khoảng 5% người dùng trên mobile Safari."

## Leo thang Sự cố Production
Khi production xảy ra sự cố, hãy giao tiếp nhanh và rõ ràng:

> **Subject: [KHẨN CẤP] Sự cố Production — Checkout Service Ngừng hoạt động**
> Xin chào team,
> Chúng tôi đang có sự cố production. Checkout service đang trả về lỗi 503 cho tất cả users.
> Tác động: Tất cả giao dịch mua bị chặn từ 14:22 UTC.
> Điều tra ban đầu: Connection pool database bị cạn kiệt.
> Hành động đã thực hiện: Đã restart service. Đang giám sát.
> ETA để sửa: 30 phút.
> Cập nhật tiếp theo lúc 15:00 UTC.

## Ngôn ngữ Post-Mortem
Post-mortem là blameless (không đổ lỗi). Cách dùng từ rất quan trọng:
- ✅ "Hệ thống không xử lý được edge case này."
- ✅ "Ngưỡng cảnh báo monitoring được cài quá cao."
- ❌ "John quên xử lý lỗi." → Không bao giờ đổ lỗi cho cá nhân

## Mô tả Nguyên nhân Gốc rễ
- "**Root cause** là một race condition trong queue processor."
- "Lỗi này được **triggered by** một deployment thay đổi giá trị timeout."
- "**Underlying issue** là thiếu validation trên input."

## Mẹo phỏng vấn
"Kể cho tôi nghe về một bug bạn đã sửa" là câu hỏi phỏng vấn kinh điển. Dùng cấu trúc: bug là gì → cách tìm ra → cách sửa → bài học rút ra.""",
        },
        "quiz": {
            "title": "Quiz: Giao tiếp Lỗi & Sự cố",
            "description": "Kiểm tra kỹ năng báo cáo lỗi và giao tiếp sự cố của bạn.",
            "questions": [
                {
                    "question": "Câu nào mô tả đúng hành vi quan sát được so với hành vi mong đợi?",
                    "options": [
                        "Bị hỏng rồi.",
                        "Khi X xảy ra, hệ thống làm Y, nhưng đáng lẽ phải làm Z.",
                        "Có lỗi ở đâu đó.",
                        "Code bị sai.",
                    ],
                    "explanation": "'Khi X, hệ thống làm Y, nhưng nên làm Z' mô tả bug rõ ràng theo 3 phần: trigger, thực tế, kỳ vọng.",
                },
                {
                    "question": "Trong post-mortem, câu nào phù hợp nhất?",
                    "options": [
                        "John quên thêm xử lý lỗi.",
                        "Hệ thống thiếu xử lý lỗi cho edge case này.",
                        "Đó là lỗi của người.",
                        "Ai đó trong team đã mắc lỗi.",
                    ],
                    "explanation": "Post-mortem là blameless. Tập trung vào hệ thống, quy trình hoặc biện pháp bảo vệ còn thiếu — không phải cá nhân.",
                },
                {
                    "question": "'Root cause' có nghĩa là gì?",
                    "options": [
                        "Bug đầu tiên trong code",
                        "Nguyên nhân cơ bản và cốt lõi gây ra sự cố",
                        "Thay đổi code gần nhất",
                        "Dòng code nơi lỗi được throw",
                    ],
                    "explanation": "Root cause là lý do cơ bản nhất khiến vấn đề xảy ra, không chỉ là triệu chứng bề mặt.",
                },
                {
                    "question": "Khi leo thang sự cố production, bạn phải bao gồm điều gì?",
                    "options": [
                        "Full stack trace",
                        "Phạm vi tác động, hành động đã thực hiện và ETA cập nhật tiếp theo",
                        "Output của git blame",
                        "Tất cả commit gần đây",
                    ],
                    "explanation": "Giao tiếp sự cố cần: cái gì bị down, ai bị ảnh hưởng, bạn đã làm gì và khi nào cập nhật tiếp.",
                },
                {
                    "question": "Câu nào tốt nhất để đưa ra giả thuyết về nguyên nhân bug?",
                    "options": [
                        "Tôi nghĩ có thể có lẽ là database.",
                        "Vấn đề có vẻ nằm ở logic hết hạn session.",
                        "Có gì đó hỏng ở đâu đó trong backend.",
                        "Tôi không chắc nhưng có thể là API.",
                    ],
                    "explanation": "'The issue appears to be in X' (Vấn đề có vẻ nằm ở X) chuyên nghiệp, cụ thể và được hedging phù hợp mà không nghe có vẻ không chắc chắn.",
                },
            ],
        },
    },
    "technical_solution": {
        "lesson": {
            "title": "Đề xuất Giải pháp Kỹ thuật bằng Tiếng Anh",
            "content": """# Đề xuất Giải pháp Kỹ thuật

Dù trong cuộc họp hay văn bản RFC, cách bạn trình bày ý tưởng kỹ thuật ảnh hưởng đến cách chúng được tiếp nhận.

## Cấu trúc Đề xuất Kỹ thuật
1. **Vấn đề** — Tình trạng hiện tại là gì?
2. **Giải pháp đề xuất** — Bạn đề nghị gì?
3. **Đánh đổi** — Ưu và nhược điểm
4. **Các lựa chọn đã cân nhắc** — Bạn đã xem xét gì khác?
5. **Khuyến nghị** — Nên làm gì?

## Cụm từ Quan trọng: Mô tả Vấn đề
- "Hiện tại, **bottleneck** của chúng ta là database monolithic. Mọi service đều truy vấn cùng một DB, gây ra **tranh chấp**."
- "Cách tiếp cận hiện tại **không thể mở rộng** quá X request/giây."
- "Chúng ta đang gặp **latency spike** vì các API call đồng bộ."

## Cụm từ Quan trọng: Đề xuất Giải pháp
- "Tôi **đề xuất** chuyển sang kiến trúc microservices với database riêng cho từng service."
- "**Khuyến nghị** của tôi là thêm message queue để tách rời các service."
- "Chúng ta **có thể** thêm Redis caching layer, giúp giảm tải DB khoảng ~70%."

## Thảo luận về Đánh đổi
- "**Ưu điểm** của cách này là..."
- "**Đánh đổi** là tăng độ phức tạp vận hành."
- "Cách này **đi kèm với** chi phí ban đầu cao hơn nhưng bảo trì dài hạn thấp hơn."
- "**Rủi ro** ở đây là..."

## Biện hộ cho Lựa chọn Công nghệ
- "Chúng tôi chọn PostgreSQL thay vì MongoDB **vì** dữ liệu có quan hệ và chúng tôi cần transaction ACID."
- "Chúng tôi chọn Kafka **vì** cần đảm bảo gửi tin và khả năng replay."
- "Redis **phù hợp với use case của chúng tôi** vì dữ liệu session tạm thời và hưởng lợi từ tốc độ in-memory."

## Ví dụ: Đề xuất Cache
> "Hiện tại, trang chi tiết sản phẩm thực hiện 12 DB query mỗi request, gây ra latency P95 là 800ms. Tôi đề xuất thêm Redis cache với chiến lược write-through và TTL 5 phút. Điều này sẽ giảm ~80% DB query và đưa latency P95 xuống dưới 100ms. Đánh đổi là tăng độ phức tạp infrastructure và khả năng cache không nhất quán trong cửa sổ TTL."

## Mẹo phỏng vấn
"Bạn sẽ cải thiện hiệu suất hệ thống này thế nào?" — Cấu trúc câu trả lời: vấn đề → giải pháp → đánh đổi. Interviewer đánh giá cao tư duy có cấu trúc hơn câu trả lời hoàn hảo.""",
        },
        "quiz": {
            "title": "Quiz: Đề xuất Giải pháp Kỹ thuật",
            "description": "Kiểm tra khả năng giao tiếp giải pháp kỹ thuật chuyên nghiệp của bạn.",
            "questions": [
                {
                    "question": "'Bottleneck' có nghĩa gì trong ngữ cảnh kỹ thuật?",
                    "options": [
                        "Một loại container nhỏ",
                        "Điểm trong hệ thống giới hạn hiệu suất tổng thể",
                        "Một loại database",
                        "Một lỗ hổng bảo mật",
                    ],
                    "explanation": "Bottleneck là điểm mà hiệu suất bị giới hạn, khiến toàn bộ hệ thống chậm lại — giống như giao thông tắc nghẽn tại một đoạn đường hẹp.",
                },
                {
                    "question": "Câu nào đề xuất giải pháp Redis caching tốt nhất?",
                    "options": [
                        "Hãy dùng Redis.",
                        "Tôi đề xuất Redis caching layer để giảm tải DB ~70%, với chiến lược write-through và TTL 5 phút.",
                        "Redis sẽ hay đấy.",
                        "Chúng ta nên thử caching xem sao.",
                    ],
                    "explanation": "Một đề xuất mạnh bao gồm công nghệ, tác động kỳ vọng và cách thực hiện.",
                },
                {
                    "question": "Khi biện hộ cho lựa chọn công nghệ, bạn nên bao gồm gì?",
                    "options": [
                        "Chỉ tên công nghệ",
                        "Công nghệ, lý do phù hợp và các lựa chọn thay thế đã cân nhắc",
                        "Bảng so sánh từ internet",
                        "Link tài liệu",
                    ],
                    "explanation": "Lý giải nên tham chiếu đến yêu cầu cụ thể của bạn và tại sao công nghệ này đáp ứng tốt hơn các lựa chọn khác.",
                },
                {
                    "question": "'Trade-off' có nghĩa là gì?",
                    "options": [
                        "Đổi một công nghệ sang công nghệ khác",
                        "Một lợi ích không có nhược điểm",
                        "Sự cân bằng giữa hai yếu tố cạnh tranh — đạt được một lợi thế nhưng hy sinh một thứ khác",
                        "Quyết định cuối cùng sau thảo luận",
                    ],
                    "explanation": "Mỗi quyết định kỹ thuật đều có trade-off. Thừa nhận chúng cho thấy bạn đã suy nghĩ phê phán về giải pháp.",
                },
                {
                    "question": "Câu nào xác định vấn đề hiệu suất một cách đúng đắn?",
                    "options": [
                        "Hệ thống chậm.",
                        "Chúng ta đang gặp latency spike P95 là 800ms trên API sản phẩm do DB query đồng bộ.",
                        "Mọi thứ không hoạt động tốt.",
                        "Hiệu suất kém.",
                    ],
                    "explanation": "Ngôn ngữ cụ thể, có thể đo lường (P95, 800ms, synchronous DB queries) là thiết yếu trong giao tiếp kỹ thuật chuyên nghiệp.",
                },
            ],
        },
    },
    "python_interview": {
        "lesson": {
            "title": "Tiếng Anh Phỏng vấn Python: Giải thích Code và Khái niệm",
            "content": """# Tiếng Anh Phỏng vấn Python Developer

Phỏng vấn kỹ thuật kiểm tra cả kiến thức Python lẫn khả năng truyền đạt rõ ràng bằng tiếng Anh.

## Giải thích Các Pattern Code

### Decorator
> "Decorator trong Python là một **higher-order function** (hàm bậc cao) **bọc** một hàm khác để thêm hành vi mà không sửa source code của nó. Ví dụ: decorator `@login_required` **chặn** mỗi request và kiểm tra xác thực trước khi cho hàm thực thi."

### Generator
> "Generator dùng `yield` thay vì `return`. Chúng **hiệu quả về bộ nhớ** vì tạo ra giá trị theo kiểu **lazy** — từng cái một — thay vì lưu toàn bộ chuỗi vào bộ nhớ. Lý tưởng cho **dataset lớn** hoặc streaming data."

### Context Manager
> "Context manager dùng `with` đảm bảo tài nguyên được **dọn sạch đúng cách** ngay cả khi có exception. `with open(file)` đảm bảo file được **đóng tự động** sau khi block kết thúc."

## Truyền đạt Độ phức tạp (Big O)
- "Giải pháp này là **O(n log n)** vì chúng ta sort input."
- "Cách tiếp cận của tôi **đánh đổi** không gian để lấy tốc độ — O(n) bộ nhớ nhưng O(1) lookup."
- "Chúng ta có thể **tối ưu** từ O(n²) xuống O(n) bằng cách dùng hash map."

## Trả lời Câu hỏi Behavioral
**"Kể cho tôi nghe về một bug khó bạn đã giải quyết."**
> "Trong một dự án trước, chúng tôi gặp **race condition** trong job queue gây ra email trùng lặp. Tôi **chẩn đoán** bằng cách thêm structured logging và phát hiện ra hai workers đang **claim** cùng một job đồng thời. Giải pháp là thêm database-level locking với `SELECT FOR UPDATE`. Sau khi sửa, chúng tôi **giám sát** trong 48 giờ và xác nhận vấn đề đã được giải quyết."

## Suy nghĩ Thành lời
- "Hãy để tôi **suy nghĩ qua** từng bước."
- "Cách tiếp cận ban đầu của tôi sẽ là... nhưng tôi thấy có vấn đề tiềm ẩn ở..."
- "Tôi sẽ bắt đầu với giải pháp **brute force** để thiết lập baseline, rồi tối ưu."

## Mẹo phỏng vấn
Nói "I'll think through this out loud" khi gặp câu hỏi khó. Interviewer muốn thấy quá trình suy luận của bạn, không chỉ kết quả cuối.""",
        },
        "quiz": {
            "title": "Quiz: Tiếng Anh Phỏng vấn Python",
            "description": "Kiểm tra khả năng giải thích khái niệm Python bằng tiếng Anh chuyên nghiệp.",
            "questions": [
                {
                    "question": "Cách giải thích decorator Python tốt nhất là gì?",
                    "options": [
                        "Nó giống như một wrapper.",
                        "Decorator là higher-order function bọc một hàm khác để thêm hành vi mà không sửa source code.",
                        "Nó trang trí code với tính năng bổ sung.",
                        "Đó là một design pattern.",
                    ],
                    "explanation": "Giải thích tốt dùng từ vựng chính xác: 'higher-order function', 'wraps', 'without modifying source code'. Điều này thể hiện độ sâu hiểu biết.",
                },
                {
                    "question": "Tại sao generator hiệu quả về bộ nhớ?",
                    "options": [
                        "Chúng dùng ít CPU hơn.",
                        "Chúng tạo giá trị lazily — từng cái một — thay vì lưu toàn bộ chuỗi vào bộ nhớ.",
                        "Chúng được compile, không phải interpret.",
                        "Chúng dùng NumPy bên dưới.",
                    ],
                    "explanation": "'Lazily' và 'one at a time' là khái niệm then chốt. Generator không giữ toàn bộ dataset trong bộ nhớ.",
                },
                {
                    "question": "Câu nào truyền đạt đúng một sự tối ưu Big O?",
                    "options": [
                        "Bây giờ nhanh hơn rồi.",
                        "Chúng ta có thể tối ưu từ O(n²) xuống O(n) bằng cách dùng hash map thay vì vòng lặp lồng nhau.",
                        "Thuật toán tốt hơn rồi.",
                        "Tôi làm nó hiệu quả hơn.",
                    ],
                    "explanation": "Truyền đạt điều gì đã thay đổi (cấu trúc dữ liệu), tại sao (tránh vòng lặp lồng nhau) và kết quả (O(n²) → O(n)).",
                },
                {
                    "question": "Cách bắt đầu trả lời câu hỏi algorithm khó trong phỏng vấn như thế nào?",
                    "options": [
                        "Nhảy thẳng vào giải pháp.",
                        "Không nói gì và bắt đầu code.",
                        "Nói 'I'll think through this out loud' và bắt đầu với brute force approach.",
                        "Hỏi interviewer lấy câu trả lời.",
                    ],
                    "explanation": "Suy nghĩ thành lời cho thấy quá trình lập luận. Interviewer đánh giá cao ứng viên giao tiếp được cách tiếp cận, không chỉ kết quả cuối.",
                },
                {
                    "question": "Câu nào mô tả đúng sự đánh đổi space-time?",
                    "options": [
                        "Nó dùng nhiều bộ nhớ hơn.",
                        "Cách tiếp cận này đánh đổi không gian để lấy tốc độ — O(n) bộ nhớ nhưng O(1) lookup.",
                        "Hơi chậm hơn nhưng dùng ít RAM hơn.",
                        "Giải pháp được tối ưu.",
                    ],
                    "explanation": "'Trades X for Y' là từ vựng kỹ thuật chuẩn để mô tả sự lựa chọn có chủ ý giữa hai loại tài nguyên.",
                },
            ],
        },
    },
    "aws_system_design": {
        "lesson": {
            "title": "Tiếng Anh Thảo luận AWS & Thiết kế Hệ thống",
            "content": """# Tiếng Anh Thảo luận AWS và System Design

Thảo luận system design đòi hỏi thành thạo cả khái niệm kiến trúc lẫn từ vựng để trao đổi về các trade-off một cách tự tin.

## Từ vựng Kiến trúc Cốt lõi
| Thuật ngữ | Ý nghĩa |
|------|---------| 
| Scalability | Khả năng xử lý tải tăng cao |
| Availability | Thời gian hoạt động của hệ thống (99.9% = ~9 giờ/năm downtime) |
| Latency | Thời gian hoàn thành một request |
| Throughput | Số request xử lý mỗi giây |
| Fault tolerance | Khả năng tiếp tục hoạt động khi có thành phần hỏng |

## Thảo luận về AWS Services

### Mô tả EC2 Choices
> "Cho workload này, tôi đề xuất **EC2 Auto Scaling** với **Application Load Balancer**. Tối thiểu 2 instance để đảm bảo HA, scale up dựa trên ngưỡng CPU 70%, và deploy trên **multi-AZ** để fault tolerance."

### Mô tả Storage
> "Cho file do user upload, **S3** là lựa chọn đúng — **vô hạn khả năng mở rộng**, **độ bền 11 nines**, và tích hợp với **CloudFront** để phân phối CDN toàn cầu."

### Thảo luận về RDS
> "Chúng tôi dùng **RDS PostgreSQL** với **Multi-AZ deployment** để failover tự động. Với workload đọc nhiều, chúng tôi thêm **read replica** để offload analytics query khỏi primary."

## Thảo luận Trade-offs
- "Trade-off của **Lambda** là cold start latency — chấp nhận được cho async workload nhưng problematic cho real-time API."
- "**SQS** tách rời producer khỏi consumer, nhưng tạo ra **eventual consistency** trong workflow."
- "**DynamoDB** cho latency single-digit millisecond ở quy mô lớn, nhưng mất khả năng **JOIN** và ad-hoc query."

## Cụm từ Thảo luận Design
- "Tôi sẽ bắt đầu với **monolith** để validate sản phẩm, rồi **extract** service khi xác định được bounded context."
- "**Bottleneck** ở đây sẽ là database — tôi sẽ giải quyết bằng **read replica** hoặc **cache layer**."
- "Cho global users, tôi sẽ đặt **CDN** phía trước để serve static assets và giảm tải **origin**."

## Mẹo phỏng vấn
Trong vòng design AWS, luôn đề cập: multi-AZ, auto-scaling, monitoring (CloudWatch) và tối ưu chi phí. Những điều này thể hiện hiểu biết thực tế về production.""",
        },
        "quiz": {
            "title": "Quiz: Tiếng Anh AWS & System Design",
            "description": "Kiểm tra từ vựng thảo luận kiến trúc AWS của bạn.",
            "questions": [
                {
                    "question": "'Multi-AZ' trong AWS có nghĩa là gì?",
                    "options": [
                        "Nhiều Amazon zone trên toàn cầu",
                        "Deploy trên nhiều Availability Zone trong một region để đảm bảo fault tolerance",
                        "Một loại load balancer",
                        "Nhiều tài khoản AWS",
                    ],
                    "explanation": "Multi-AZ deploy tài nguyên trên các trung tâm dữ liệu riêng biệt trong cùng region. Nếu một AZ hỏng, traffic tự động chuyển sang AZ khác.",
                },
                {
                    "question": "Trade-off khi dùng AWS Lambda cho real-time API là gì?",
                    "options": [
                        "Quá đắt",
                        "Cold start latency khiến nó không phù hợp cho request nhạy cảm về latency",
                        "Không hỗ trợ HTTP",
                        "Không thể kết nối database",
                    ],
                    "explanation": "Lambda function chưa được gọi gần đây có độ trễ 'cold start' hàng trăm millisecond — problematic cho real-time API.",
                },
                {
                    "question": "Tại sao bạn thêm read replica vào RDS instance?",
                    "options": [
                        "Để backup tự động",
                        "Để xử lý failover",
                        "Để offload read query và cải thiện scalability đọc",
                        "Để mã hóa database",
                    ],
                    "explanation": "Read replica xử lý SELECT query, giảm tải cho RDS primary instance vốn xử lý ghi.",
                },
                {
                    "question": "Câu nào mô tả đúng trade-off của DynamoDB?",
                    "options": [
                        "DynamoDB rẻ nhưng không đáng tin cậy.",
                        "DynamoDB cho latency single-digit millisecond ở quy mô lớn nhưng mất khả năng JOIN.",
                        "DynamoDB chỉ cho dự án nhỏ.",
                        "DynamoDB không hỗ trợ index.",
                    ],
                    "explanation": "DynamoDB xuất sắc cho key-value lookup ở quy mô lớn nhưng không hỗ trợ SQL JOIN hay ad-hoc query phức tạp.",
                },
                {
                    "question": "'Throughput' trong system design là gì?",
                    "options": [
                        "Thời gian hoàn thành một request",
                        "Số request hệ thống có thể xử lý mỗi giây",
                        "Dung lượng lưu trữ của database",
                        "Băng thông mạng tính bằng Mbps",
                    ],
                    "explanation": "Throughput đo số lượng operation (request, transaction) mà hệ thống xử lý mỗi đơn vị thời gian, thường là mỗi giây.",
                },
            ],
        },
    },
    "code_review": {
        "lesson": {
            "title": "Giao tiếp Code Review: Đưa và Nhận Feedback",
            "content": """# Tiếng Anh Code Review

Code review là nơi kỹ năng kỹ thuật gặp gỡ giao tiếp chuyên nghiệp. Giọng điệu của bạn định hình văn hóa team.

## Cho Feedback: Khung Mang tính Xây dựng

### Từ Phê bình sang Hợp tác
| Tránh | Tốt hơn |
|-------|--------|
| "Cái này sai." | "Điều này có thể gây ra X trong edge case Y. Bạn nghĩ sao về việc xử lý bằng Z?" |
| "Tại sao bạn làm thế này?" | "Tôi tò mò về lý do ở đây — bạn có thể giải thích cách tiếp cận không?" |
| "Cái này không hiệu quả." | "Tôi tự hỏi liệu chúng ta có thể tối ưu với hash map — sẽ giảm độ phức tạp từ O(n²) xuống O(n)." |

### Nit vs Blocking Comment
- **Nit**: nhỏ, không blocking — "Nit: chúng ta có thể đổi tên biến này thành `user_id` cho rõ hơn không?"
- **Blocking**: bắt buộc phải sửa trước khi merge — "SQL query này dễ bị injection. Phải dùng parameterized trước khi merge."
- **Suggestion**: cải thiện tùy chọn — "Suggestion: cân nhắc extract hàm này ra helper function để dễ test hơn."

## Nhận Feedback một cách Chuyên nghiệp
- ✅ "Nhận xét hay — tôi sẽ sửa ngay."
- ✅ "Cảm ơn feedback. Tôi dùng X vì Y — vui lòng thảo luận nếu bạn thấy cách tốt hơn."
- ✅ "Tôi thấy quan điểm của bạn. Để tôi refactor lại."
- ❌ Tránh: Bảo vệ mọi comment một cách phòng thủ. Chọn lọc trận chiến của bạn.

## Yêu cầu Code Review
> "Hi [Tên], khi bạn có thời gian, bạn có thể xem PR #142 không? Nó thêm tích hợp payment. Thay đổi chính ở `payment_service.py` và `checkout_api.py`. Tôi sẵn sàng hướng dẫn bạn qua nếu cần."

## Thảo luận Thay đổi trong Review
- "Tôi đã **refactor** logic validation để tách biệt concerns."
- "Cái này **thay thế** cách tiếp cận đồng bộ trước đó bằng xử lý async."
- "Tôi đã **extract** database query ra repository layer."
- "**Test coverage** cho module này hiện đạt 87%."

## Ví dụ: Để lại Comment Mang tính Xây dựng
> "Nhìn chung trông ổn! Một điều tôi nhận thấy: hàm `get_user` thực hiện DB call bên trong vòng lặp, có thể là O(n) query. Hãy cân nhắc batch bằng `get_users_by_ids(ids)` để chỉ cần một query. Cho tôi biết nếu bạn muốn cùng làm."

## Mẹo phỏng vấn
"Bạn xử lý code review feedback mà bạn không đồng ý như thế nào?" — nói rằng bạn thảo luận về lý do, cân nhắc quan điểm, và nếu thực sự xung đột, leo thang lên team. Đừng bao giờ nói bạn chỉ chấp nhận hoặc chỉ từ chối.""",
        },
        "quiz": {
            "title": "Quiz: Giao tiếp Code Review",
            "description": "Kiểm tra kỹ năng giao tiếp code review của bạn.",
            "questions": [
                {
                    "question": "Comment nào mang tính xây dựng nhất trong code review?",
                    "options": [
                        "Cái này sai.",
                        "Điều này có thể gây null pointer trong edge case khi user chưa đăng nhập. Hãy xem xét thêm guard clause.",
                        "Tôi không thích cái này.",
                        "Viết lại cái này.",
                    ],
                    "explanation": "Feedback tốt giải thích vấn đề, hậu quả và gợi ý giải pháp. Mang tính hợp tác, không phê phán.",
                },
                {
                    "question": "'Nit' trong code review có nghĩa là gì?",
                    "options": [
                        "Vấn đề blocking quan trọng",
                        "Gợi ý nhỏ không blocking, không ngăn merge PR",
                        "Lỗ hổng bảo mật",
                        "Lỗi cú pháp",
                    ],
                    "explanation": "'Nit' (viết tắt của nitpick) báo hiệu comment nhỏ về style hoặc preference không block PR khỏi việc merge.",
                },
                {
                    "question": "Nên phản hồi thế nào khi bạn không đồng ý với comment của reviewer?",
                    "options": [
                        "Từ chối ngay.",
                        "Bỏ qua nó.",
                        "Giải thích lý do một cách chuyên nghiệp: 'Tôi dùng X vì Y — vui lòng thảo luận.'",
                        "Chấp nhận mà không đặt câu hỏi.",
                    ],
                    "explanation": "Phản hồi chuyên nghiệp ghi nhận feedback, chia sẻ lý do của bạn và mời thảo luận. Điều này xây dựng niềm tin trong team.",
                },
                {
                    "question": "Câu nào xác định đúng vấn đề N+1 query?",
                    "options": [
                        "Database chậm.",
                        "Hàm get_user thực hiện DB call bên trong vòng lặp — có thể là O(n) query. Hãy cân nhắc batch với một query duy nhất.",
                        "Có quá nhiều query.",
                        "Tối ưu database.",
                    ],
                    "explanation": "Ngôn ngữ cụ thể (O(n) query, inside the loop, batching) cho thấy hiểu biết sâu và giúp tác giả sửa nhanh.",
                },
                {
                    "question": "Câu nào mô tả đúng một thay đổi cấu trúc code trong PR?",
                    "options": [
                        "Tôi di chuyển vài thứ.",
                        "Tôi đã extract database query ra repository layer để tách biệt concerns.",
                        "Đã thay đổi rồi.",
                        "Đã refactor.",
                    ],
                    "explanation": "Trong mô tả PR và review, hãy cụ thể: nêu rõ cái gì đã thay đổi, ở đâu và tại sao. 'Repository layer để tách biệt concerns' rõ ràng và chuyên nghiệp.",
                },
            ],
        },
    },
}

# ── System Design Lesson translations ─────────────────────────────────────────

SD_LESSON_TRANSLATIONS_VI: dict[str, dict] = {
    "load_balancing": {
        "lesson": {
            "title": "Cân bằng Tải: Nền tảng và Chiến lược",
            "content": """# Cân bằng Tải (Load Balancing)

Load balancer phân phối traffic đến từ các client vào nhiều backend server.

## Các Thuật toán
- **Round Robin** — request đến từng server theo thứ tự
- **Weighted Round Robin** — theo tỷ lệ năng lực server
- **Least Connections** — định tuyến đến server có ít kết nối active nhất
- **IP Hash** — sticky session dựa trên IP client

## Layer 4 vs Layer 7
- **L4**: Tầng TCP/UDP, nhanh, định tuyến theo IP/port
- **L7**: Tầng HTTP, định tuyến theo URL/header/cookie (AWS ALB)

## Health Check
Load balancer định kỳ ping `/health`. Server không khỏe mạnh tự động bị loại khỏi vòng xử lý.

## High Availability
Deploy load balancer theo cặp active-active hoặc active-passive để loại bỏ điểm lỗi đơn.

## Session Stickiness
Với app stateful, dùng IP Hash HOẶC (tốt hơn) externalize session state ra Redis.

## Thực tế: Netflix
Netflix dùng AWS ELB để phân phối streaming request qua hàng nghìn EC2 instance. Giờ cao điểm, load balancer xử lý hàng triệu kết nối đồng thời.

## Mẹo phỏng vấn
Bắt đầu với *tại sao* (horizontal scaling, HA), thảo luận *thuật toán* kèm trade-off, luôn đề cập *health check* và *tính dự phòng* của chính LB.""",
        },
        "quiz": {
            "title": "Quiz: Cân bằng Tải",
            "description": "Kiểm tra kiến thức cơ bản về cân bằng tải.",
            "questions": [
                {
                    "question": "Thuật toán nào định tuyến đến server có ít kết nối active nhất?",
                    "options": ["Round Robin", "IP Hash", "Least Connections", "Weighted Round Robin"],
                    "explanation": "Least Connections định tuyến mỗi request mới đến server ít kết nối active nhất — lý tưởng cho kết nối tồn tại lâu.",
                },
                {
                    "question": "Ưu điểm chính của Layer 7 load balancer là gì?",
                    "options": [
                        "Nhanh hơn vì hoạt động ở tầng TCP",
                        "Định tuyến dựa trên nội dung HTTP như URL path và header",
                        "Dùng ít bộ nhớ hơn Layer 4",
                        "Không cần chứng chỉ SSL",
                    ],
                    "explanation": "Layer 7 hiểu HTTP và có thể định tuyến dựa trên URL path, header và cookie — cho phép content-based routing.",
                },
                {
                    "question": "IP Hash (sticky sessions) giải quyết vấn đề gì?",
                    "options": [
                        "Giảm SSL overhead",
                        "Đảm bảo client luôn đến cùng một backend server",
                        "Cải thiện cache hit rate",
                        "Phát hiện server không khỏe mạnh",
                    ],
                    "explanation": "IP Hash định tuyến request từ cùng IP client đến cùng server, duy trì session affinity cần thiết khi session state được lưu cục bộ.",
                },
                {
                    "question": "Load balancer phát hiện backend server không khỏe mạnh như thế nào?",
                    "options": [
                        "Giám sát CPU qua CloudWatch",
                        "Định kỳ gửi health check request và kiểm tra response thành công",
                        "Đọc error log từ server",
                        "Kiểm tra uptime qua SSH",
                    ],
                    "explanation": "Load balancer gửi health check request định kỳ. Nếu server không phản hồi thành công, nó bị loại khỏi vòng xử lý.",
                },
                {
                    "question": "Cách tiếp cận được đề xuất cho session trong app scale ngang là gì?",
                    "options": [
                        "Dùng sticky sessions (IP Hash)",
                        "Lưu session data trong store ngoài chia sẻ như Redis",
                        "Tắt session và chỉ dùng JWT",
                        "Replicate session data qua tất cả server",
                    ],
                    "explanation": "Lưu session trong Redis cho phép bất kỳ backend server nào xử lý bất kỳ request nào — kiến trúc stateless được ưa chuộng cho hệ thống có thể mở rộng.",
                },
            ],
        },
    },
    "caching": {
        "lesson": {
            "title": "Chiến lược Caching: Từ Cơ bản đến Pattern",
            "content": """# Chiến lược Caching

Cache lưu trữ bản sao dữ liệu tốn kém trong bộ nhớ nhanh. Chỉ số quan trọng: **cache hit rate**.

## Các Pattern

### Cache-Aside (Lazy Loading)
App kiểm tra cache trước. Nếu miss, lấy từ DB và điền vào cache.
- Ưu: Chỉ cache những gì cần; cache hỏng không ảnh hưởng app
- Nhược: Request đầu tiên chậm (cold start); dữ liệu có thể cũ

### Write-Through
Mỗi lần ghi vào cả cache và DB cùng lúc.
- Ưu: Cache luôn mới
- Nhược: Tăng write latency

### Write-Behind (Write-Back)
Ghi vào cache ngay; DB được cập nhật bất đồng bộ.
- Ưu: Write latency thấp nhất
- Nhược: Nguy cơ mất dữ liệu nếu cache crash trước khi ghi DB

## Chính sách Eviction
- **LRU** (Least Recently Used) — mặc định của Redis
- **LFU** (Least Frequently Used)
- **TTL** (Time-To-Live)

## Cache Invalidation
1. TTL expiry — dữ liệu tự hết hạn
2. Event-driven — xóa/cập nhật key tường minh khi ghi
3. Cache busting — thêm version vào key (`user:123:v2`)

## Thực tế: Twitter
Twitter cache timeline trong Redis. Home timeline của bạn được tính trước theo từng user. Khi người bạn follow tweet, worker fan-out đẩy tweet vào cached timeline của mỗi follower.

## Mẹo phỏng vấn
Với bất kỳ vấn đề hiệu suất nào, hãy đề xuất caching. Đề cập cache-aside là mặc định, Redis là công cụ mặc định, và thảo luận về TTL và chiến lược invalidation.""",
        },
        "quiz": {
            "title": "Quiz: Chiến lược Caching",
            "description": "Kiểm tra kiến thức về các pattern caching và trade-off.",
            "questions": [
                {
                    "question": "Trong cache-aside, điều gì xảy ra khi cache miss?",
                    "options": [
                        "Request thất bại",
                        "App lấy từ DB và lưu kết quả vào cache",
                        "Load balancer định tuyến sang server khác",
                        "Cache tự động lấy từ DB",
                    ],
                    "explanation": "Trong cache-aside, ứng dụng lấy từ DB khi miss và điền vào cache. Đây là pattern phổ biến nhất.",
                },
                {
                    "question": "Pattern caching nào có write latency thấp nhất?",
                    "options": ["Cache-Aside", "Write-Through", "Write-Behind", "Read-Through"],
                    "explanation": "Write-behind xác nhận ghi ngay khi dữ liệu vào cache và cập nhật DB bất đồng bộ, cho perceived write latency thấp nhất.",
                },
                {
                    "question": "Redis dùng chính sách eviction nào mặc định?",
                    "options": ["FIFO", "LFU", "LRU", "Random"],
                    "explanation": "Redis dùng LRU (Least Recently Used) mặc định — evict item không được truy cập lâu nhất khi bộ nhớ đầy.",
                },
                {
                    "question": "Rủi ro chính của write-behind caching là gì?",
                    "options": [
                        "Tăng write latency",
                        "Cache không nhất quán",
                        "Mất dữ liệu nếu cache crash trước khi ghi DB bất đồng bộ",
                        "Database không thể theo kịp read",
                    ],
                    "explanation": "Write-behind xác nhận ghi trước khi persist vào DB. Nếu cache crash giữa lúc ghi và đồng bộ DB, dữ liệu đó bị mất.",
                },
                {
                    "question": "TTL của cache kiểm soát điều gì?",
                    "options": [
                        "Số item tối đa cache lưu trữ",
                        "Bao lâu một item được cache trước khi tự động hết hạn",
                        "Thời gian chờ trước khi fallback về DB",
                        "Độ trễ replication giữa các cache node",
                    ],
                    "explanation": "TTL đặt thời gian hết hạn cho cached item. Sau khi hết hạn, item bị xóa, buộc request tiếp theo lấy dữ liệu mới.",
                },
            ],
        },
    },
    "cap_theorem_sd": {
        "lesson": {
            "title": "Định lý CAP: Đánh đổi trong Hệ thống Phân tán",
            "content": """# Định lý CAP

Trong hệ thống phân tán, bạn chỉ có thể đảm bảo **hai trong ba** thuộc tính:
- **C — Consistency (Nhất quán)**: Mỗi lần đọc trả về dữ liệu mới nhất hoặc lỗi
- **A — Availability (Sẵn sàng)**: Mỗi request nhận phản hồi không lỗi
- **P — Partition Tolerance (Chịu lỗi phân vùng)**: Hệ thống hoạt động dù network bị phân vùng

## Điểm Mấu chốt
Network partition là điều không thể tránh trong hệ thống phân tán thực. Vì vậy lựa chọn thực sự là **CP vs AP**.

## Hệ thống CP
Trong khi partition, từ chối phục vụ dữ liệu cũ — trả về lỗi hoặc timeout.
- **Ví dụ**: HBase, Zookeeper, MongoDB (mặc định)
- **Dùng khi**: Giao dịch tài chính, tồn kho, đặt chỗ

## Hệ thống AP
Trong khi partition, tiếp tục phục vụ nhưng có thể trả dữ liệu cũ.
- **Ví dụ**: Cassandra, DynamoDB (mặc định), CouchDB
- **Dùng khi**: Feed mạng xã hội, danh mục sản phẩm, gợi ý

## Eventual Consistency
Hệ thống AP cung cấp *eventual consistency*: với đủ thời gian, tất cả node sẽ hội tụ về cùng giá trị. Cửa sổ thường là millisecond đến giây.

## PACELC
Mở rộng CAP: ngay cả khi không có partition, vẫn có đánh đổi giữa **Latency** và **Consistency**.

## Thực tế: Amazon DynamoDB
DynamoDB cung cấp cả strong và eventual consistency theo từng request. Mặc định là eventual (throughput cao hơn). Cho các thao tác tài chính, opt-in strongly consistent reads.

## Mẹo phỏng vấn
Khi thảo luận về lựa chọn DB nào, hãy đề cập CAP. Cho thấy đó là trade-off có chủ đích được dẫn dắt bởi yêu cầu nghiệp vụ, không phải khiếm khuyết.""",
        },
        "quiz": {
            "title": "Quiz: Định lý CAP",
            "description": "Kiểm tra hiểu biết về định lý CAP và trade-off hệ thống phân tán.",
            "questions": [
                {
                    "question": "Trong định lý CAP, 'Consistency' có nghĩa là gì?",
                    "options": [
                        "Hệ thống luôn sẵn sàng",
                        "Mỗi lần đọc nhận dữ liệu mới nhất hoặc lỗi",
                        "Hệ thống chịu được network partition",
                        "Dữ liệu được replicate qua các node",
                    ],
                    "explanation": "CAP Consistency nghĩa là mỗi lần đọc trả về bản ghi mới nhất — tất cả node có cùng dữ liệu. Đây không giống ACID consistency.",
                },
                {
                    "question": "Tại sao hệ thống phân tán thực phải luôn chọn Partition Tolerance?",
                    "options": [
                        "Cho hiệu suất tốt nhất",
                        "Network partition là điều không thể tránh trong hệ thống phân tán",
                        "Consistency và Availability không thể cùng tồn tại",
                        "Yêu cầu bởi cloud provider",
                    ],
                    "explanation": "Mạng bị lỗi. Trong bất kỳ hệ thống phân tán thực nào, bạn sẽ gặp network partition. Từ bỏ P có nghĩa là một network glitch nhỏ cũng đủ để sập toàn bộ hệ thống.",
                },
                {
                    "question": "Đâu là ví dụ về hệ thống CP?",
                    "options": ["Amazon DynamoDB (mặc định)", "Apache Cassandra", "Apache Zookeeper", "CouchDB"],
                    "explanation": "Zookeeper là CP — nó từ chối phục vụ request trong partition hơn là trả dữ liệu cũ. Dùng cho distributed coordination nơi consistency là quan trọng.",
                },
                {
                    "question": "'Eventual consistency' có nghĩa là gì?",
                    "options": [
                        "Hệ thống cuối cùng sẽ crash nếu không giải quyết inconsistency",
                        "Tất cả node cuối cùng sẽ có cùng dữ liệu nếu không có cập nhật mới",
                        "Consistency được đảm bảo sau một khoảng thời gian cố định",
                        "Ghi được batch theo chu kỳ",
                    ],
                    "explanation": "Eventual consistency đảm bảo rằng nếu không có cập nhật mới, tất cả replica sẽ hội tụ về cùng giá trị theo thời gian — thường là millisecond đến giây.",
                },
                {
                    "question": "Use case nào nên chọn hệ thống AP?",
                    "options": [
                        "Xử lý chuyển khoản ngân hàng",
                        "Đặt vé máy bay",
                        "Hiển thị feed mạng xã hội",
                        "Ghi đơn thuốc y tế",
                    ],
                    "explanation": "Feed mạng xã hội có thể chấp nhận nội dung hơi cũ — tính sẵn sàng quan trọng hơn độ mới. Hệ thống tài chính và y tế cần strong consistency.",
                },
            ],
        },
    },
    "microservices_sd": {
        "lesson": {
            "title": "Kiến trúc Microservices: Nguyên tắc và Pattern",
            "content": """# Kiến trúc Microservices

Microservices là phong cách kiến trúc xây dựng ứng dụng thành tập hợp các service nhỏ, độc lập, mỗi service sở hữu database riêng và giao tiếp qua mạng.

## Monolith vs Microservices

| Khía cạnh | Monolith | Microservices |
|-----------|----------|---------------|
| Triển khai | Một đơn vị | Độc lập mỗi service |
| Scale | Scale toàn bộ | Chỉ scale bottleneck |
| Cô lập lỗi | Một bug có thể crash tất cả | Lỗi được giới hạn |

## Các Pattern Quan trọng

### API Gateway
Điểm vào duy nhất cho mọi request từ client. Xử lý auth, rate limiting, logging.

### Circuit Breaker
Nếu Service B liên tục lỗi, Service A ngừng gọi và trả fallback. Ngăn cascading failure.

### Saga Pattern
Quản lý distributed transaction. Mỗi bước publish event; compensating transaction hoàn tác khi lỗi.

### Event-Driven Communication
Services giao tiếp qua event (Kafka, SQS). Loose coupling, bất đồng bộ.

## Khi Nào Dùng Microservices
- Team lớn, nhiều người xung đột trên cùng module
- Các phần cần scale rất khác nhau
- Cần chu kỳ triển khai độc lập
- Đã có CI/CD và monitoring trưởng thành

## Khi Nào KHÔNG Nên Dùng
- Đang xây dựng MVP
- Team nhỏ (< 5 kỹ sư)
- Ranh giới domain chưa rõ

## Thực tế: Amazon
Jeff Bezos bắt buộc tất cả team expose dữ liệu qua API. Amazon đã tách thành hàng nghìn microservices. Nút "checkout" gọi ~150 service.

## Mẹo phỏng vấn
Luôn đề cập: service boundary (DDD), communication (sync REST/gRPC vs async event), quản lý dữ liệu (mỗi service sở hữu DB riêng), và độ phức tạp vận hành.""",
        },
        "quiz": {
            "title": "Quiz: Kiến trúc Microservices",
            "description": "Kiểm tra hiểu biết về nguyên tắc và pattern microservices.",
            "questions": [
                {
                    "question": "Pattern 'database per service' có nghĩa là gì?",
                    "options": [
                        "Tất cả microservices dùng chung một database trung tâm",
                        "Mỗi microservice sở hữu và quản lý database riêng",
                        "Database được replicate qua tất cả service",
                        "Service dùng read replica của primary database",
                    ],
                    "explanation": "Mỗi microservice sở hữu database riêng, cho phép thay đổi schema độc lập, chọn công nghệ phù hợp và scale độc lập.",
                },
                {
                    "question": "Circuit Breaker pattern giải quyết vấn đề gì?",
                    "options": [
                        "Service discovery trong môi trường động",
                        "Nhất quán distributed transaction",
                        "Ngăn cascading failure khi downstream service không khả dụng",
                        "Cân bằng tải giữa các service instance",
                    ],
                    "explanation": "Circuit breaker phát hiện lỗi lặp đi lặp lại và 'mở' — ngừng gọi service lỗi và trả fallback response.",
                },
                {
                    "question": "Khi nào KHÔNG nên dùng microservices?",
                    "options": [
                        "Khi team có 100+ kỹ sư",
                        "Khi services cần scale độc lập",
                        "Khi xây dựng MVP với team nhỏ",
                        "Khi cần chu kỳ triển khai độc lập",
                    ],
                    "explanation": "Microservices thêm rất nhiều độ phức tạp vận hành. Với MVP hoặc team nhỏ, chi phí vượt quá lợi ích.",
                },
            ],
        },
    },
    "database_scaling_sd": {
        "lesson": {
            "title": "Scale Database: Sharding, Replication và Partitioning",
            "content": """# Scale Database

Một instance PostgreSQL đơn lẻ tối đa khoảng 100.000 query/giây. Vượt ngưỡng đó, phải scale.

## Read Replicas
Primary xử lý ghi; nhiều replica xử lý đọc.
- AWS: RDS Read Replicas, Aurora lên đến 15 replica
- Trade-off: Replica có thể hơi chậm hơn (replication lag)

## Sharding (Horizontal Partitioning)
Chia dữ liệu qua nhiều server. Mỗi shard chứa một tập con.

**Chiến lược:**
- **Range-based**: A-M → Shard 1, N-Z → Shard 2. Đơn giản nhưng tạo hotspot.
- **Hash-based**: `shard_id = hash(user_id) % num_shards`. Phân phối đều nhưng khó rebalance.
- **Directory-based**: Lookup table ánh xạ record đến shard.

**Thách thức:** Cross-shard query tốn kém, re-sharding phức tạp.

## Vertical Partitioning
Chia bảng thành nhiều bảng ít cột hơn. Hot path đọc từ bảng nhỏ hơn.

## Connection Pooling
Dùng PgBouncer hoặc HikariCP để tái sử dụng connection. Không có pooling: 10K user đồng thời = 10K DB connection mở → database crash.

## Thực tế: Instagram
Instagram shard dữ liệu user qua hàng nghìn PostgreSQL shard. `shard_id = user_id % num_shards`.

## Mẹo phỏng vấn
Đi qua các bước: 1) Tối ưu query + index, 2) Vertical scale, 3) Read replicas, 4) Caching (Redis), 5) Sharding là biện pháp cuối cùng.""",
        },
        "quiz": {
            "title": "Quiz: Scale Database",
            "description": "Kiểm tra kiến thức về kỹ thuật scale database.",
            "questions": [
                {
                    "question": "Mục đích của read replica là gì?",
                    "options": [
                        "Shard dữ liệu qua nhiều server",
                        "Cung cấp automatic failover",
                        "Giảm tải read từ primary database",
                        "Cache kết quả query",
                    ],
                    "explanation": "Read replica nhận bản sao toàn bộ dữ liệu từ primary. Query đọc đến replica, giảm tải cho primary.",
                },
                {
                    "question": "Nhược điểm lớn của hash-based sharding là gì?",
                    "options": [
                        "Tạo hotspot với phân phối không đều",
                        "Re-sharding khi thêm server đòi hỏi di chuyển lượng lớn dữ liệu",
                        "Cần bảng lookup trung tâm",
                        "Chỉ hoạt động với NoSQL",
                    ],
                    "explanation": "Khi thêm/bỏ shard, hash function thay đổi và hầu hết dữ liệu cần di chuyển. Consistent hashing giảm thiểu nhưng thêm độ phức tạp.",
                },
                {
                    "question": "Connection pooler như PgBouncer giải quyết vấn đề gì?",
                    "options": [
                        "Replicate dữ liệu qua server",
                        "Phân phối query tự động",
                        "Tái sử dụng DB connection để giảm overhead",
                        "Mã hóa connection",
                    ],
                    "explanation": "Connection pooler duy trì pool connection mở và tái sử dụng, cho phép hàng nghìn app thread dùng chung số lượng nhỏ hơn DB connection thực.",
                },
            ],
        },
    },
    "message_queue_sd": {
        "lesson": {
            "title": "Message Queue: Giao tiếp Bất đồng bộ trong Hệ thống Phân tán",
            "content": """# Message Queue

Message queue cho phép **giao tiếp bất đồng bộ giữa các service**. Producer gửi message; consumer đọc và xử lý độc lập.

## Khi Nào Dùng Queue
- Traffic spike cao: queue làm buffer
- Task lâu dài: không chặn HTTP response (email, resize ảnh)
- Loose coupling: service không cần biết về nhau
- Reliability: service consumer tắt, message vẫn chờ trong queue

## Queue vs Pub/Sub
- **Queue**: Mỗi message được consume bởi đúng một consumer (AWS SQS, RabbitMQ)
- **Pub/Sub**: Mỗi message được gửi đến tất cả subscriber (AWS SNS, Kafka)

## Apache Kafka
Nền tảng distributed log/streaming. Khái niệm chính:
- **Topic**: Danh mục message (persistent, replayable)
- **Partition**: Topic chia thành partition để song song hóa
- **Consumer Group**: Nhiều consumer chia sẻ công việc trên một topic
- **Retention**: Message tồn tại theo thời gian cấu hình (mặc định 7 ngày)

Throughput Kafka: hàng triệu message/giây. LinkedIn xử lý 7 nghìn tỷ message/ngày trên Kafka.

## Thực tế: Uber
Khi bạn đặt Uber, Kafka publish 'TripRequested'. Driver matching, payment, ETA, notification đều consume độc lập.

## Mẹo phỏng vấn
Với email, xử lý ảnh, payment, task lâu dài — đề xuất ngay message queue. Cho thấy bạn biết SQS (task queue) vs Kafka (event streaming).""",
        },
        "quiz": {
            "title": "Quiz: Message Queue",
            "description": "Kiểm tra hiểu biết về message queue và giao tiếp bất đồng bộ.",
            "questions": [
                {
                    "question": "Sự khác biệt chính giữa queue và pub/sub là gì?",
                    "options": [
                        "Queue nhanh hơn; pub/sub tin cậy hơn",
                        "Trong queue một consumer nhận mỗi message; trong pub/sub tất cả subscriber nhận",
                        "Queue cho real-time; pub/sub cho batch",
                        "Pub/sub yêu cầu acknowledgment; queue thì không",
                    ],
                    "explanation": "Queue phân phối message cho một consumer (phân công việc). Pub/sub broadcast mỗi message đến tất cả subscriber (thông báo sự kiện).",
                },
                {
                    "question": "Khi nào message queue là lựa chọn thiết kế đúng?",
                    "options": [
                        "Khi consumer phải phản hồi trong 100ms",
                        "Khi cần xử lý task async để không chặn user",
                        "Khi service cần dùng chung database",
                        "Khi cần latency thấp nhất",
                    ],
                    "explanation": "Message queue lý tưởng cho task async — gửi email, resize ảnh, xử lý payment. Ngăn HTTP request bị chặn bởi thao tác chậm.",
                },
                {
                    "question": "Điều gì xảy ra với message khi consumer tạm thời tắt?",
                    "options": [
                        "Message bị xóa để ngăn tràn",
                        "Gửi đến consumer dự phòng",
                        "Giữ lại trong queue đến khi consumer phục hồi",
                        "Producer tự động retry trực tiếp",
                    ],
                    "explanation": "Message tồn tại trong queue khi consumer offline. Khi phục hồi, consumer xử lý backlog. Không có message nào bị mất.",
                },
            ],
        },
    },
    "api_gateway_sd": {
        "lesson": {
            "title": "API Gateway: Cửa Ngõ cho Microservices",
            "content": """# API Gateway

API Gateway là server đóng vai trò **điểm vào duy nhất** cho tất cả request từ client.

## Trách nhiệm Chính
- **Routing**: Điều hướng request đến microservice đúng
- **Authentication & Authorization**: Xác thực JWT token hoặc API key
- **Rate Limiting**: Ngăn lạm dụng
- **SSL Termination**: Giải mã HTTPS tại gateway
- **Request/Response Transformation**: Chuyển đổi giữa các format
- **Logging & Monitoring**: Observability tập trung
- **Caching**: Cache response phổ biến

## Gateway vs Load Balancer

| Khía cạnh | Load Balancer | API Gateway |
|-----------|---------------|-------------|
| Layer | L4 hoặc L7 | L7 luôn luôn |
| Auth | Không | Có |
| Rate Limiting | Không | Có |
| Transformation | Không | Có |

## Chiến lược Rate Limiting
- **Token Bucket**: Cho phép burst. Mỗi user có N token, nạp lại theo tốc độ R.
- **Leaky Bucket**: Xử lý theo tốc độ cố định. Làm phẳng burst.
- **Fixed Window**: N request mỗi time window. Đơn giản nhưng có vấn đề ranh giới.
- **Sliding Window**: Tốc độ mượt mà, không có spike ranh giới.

## Thực tế: Netflix
Gateway Zuul của Netflix xử lý toàn bộ API traffic — authentication, routing đến 100+ microservice, circuit breaking, A/B testing và canary deployment.

## Mẹo phỏng vấn
Vẽ API Gateway là thành phần đầu tiên client tương tác. Cross-cutting concern (auth, rate limiting, logging) được xử lý một lần tại gateway, không phải trong mỗi service.""",
        },
        "quiz": {
            "title": "Quiz: API Gateway",
            "description": "Kiểm tra kiến thức về pattern API Gateway.",
            "questions": [
                {
                    "question": "Vai trò chính của API Gateway là gì?",
                    "options": [
                        "Lưu trữ dữ liệu dùng chung giữa microservices",
                        "Đóng vai điểm vào duy nhất xử lý routing và cross-cutting concern",
                        "Thay thế load balancer",
                        "Quản lý database connection",
                    ],
                    "explanation": "API Gateway là điểm vào duy nhất cho toàn bộ traffic bên ngoài. Nó route request và xử lý auth, rate limiting, logging tập trung.",
                },
                {
                    "question": "Chiến lược rate limiting nào cho phép burst traffic ngắn?",
                    "options": ["Fixed Window", "Leaky Bucket", "Token Bucket", "Sliding Window"],
                    "explanation": "Token bucket cho phép burst — nếu token đã tích lũy, user có thể thực hiện nhiều request nhanh đến khi bucket rỗng.",
                },
                {
                    "question": "Tại sao API Gateway giảm sự trùng lặp trong microservices?",
                    "options": [
                        "Dùng chung database",
                        "Cross-cutting concern như auth được implement một lần tại gateway",
                        "Tự tạo client SDK",
                        "Kết hợp nhiều service deployment",
                    ],
                    "explanation": "Không có gateway, mỗi microservice implement authentication, rate limiting và logging. Gateway tập trung những thứ này.",
                },
            ],
        },
    },
    "cdn_sd": {
        "lesson": {
            "title": "Mạng Phân phối Nội dung (CDN): Hiệu suất Toàn cầu",
            "content": """# Mạng Phân phối Nội dung (CDN)

CDN là mạng server phân tán địa lý (Points of Presence/PoP) cache và phục vụ nội dung gần người dùng hơn.

## CDN Hoạt Động Thế Nào
1. User request `cdn.example.com/logo.png`
2. DNS phân giải về PoP gần nhất
3. **Cache hit**: PoP phục vụ ngay lập tức
4. **Cache miss**: PoP lấy từ origin, cache lại, phục vụ user
5. User tiếp theo tại cùng PoP được cache hit

## CDN Cache Gì
- Static asset: hình ảnh, CSS, JS, font, video
- API response (với Cache-Control header phù hợp)
- CDN KHÔNG cache: trang có auth, POST request, nội dung cá nhân hóa

## Lợi Ích
- Cải thiện latency 50-300ms cho user toàn cầu
- 80-95% request được phục vụ từ cache
- Bảo vệ DDoS
- Giảm chi phí bandwidth origin

## Cache Invalidation
1. **URL versioning (tốt nhất)**: `main.a3f9b2.js` — nội dung mới = URL mới
2. **CDN invalidation API**: Purge URL thủ công
3. **TTL expiry**: Chờ TTL hết hạn. Stale cho đến đó.

## Thực tế
AWS CloudFront có 450+ PoP. Cloudflare tập trung bảo mật, có gói miễn phí.

## Mẹo phỏng vấn
Với bất kỳ hệ thống toàn cầu nào, đề cập CDN ngay. 'Chúng ta sẽ đặt CDN trước S3 cho static asset và trước API cho các response có thể cache — giảm latency và cắt tải origin ~90%.'""",
        },
        "quiz": {
            "title": "Quiz: CDN",
            "description": "Kiểm tra kiến thức về CDN và pattern sử dụng.",
            "questions": [
                {
                    "question": "Điều gì xảy ra khi CDN cache miss?",
                    "options": [
                        "CDN trả 404",
                        "CDN lấy từ origin, cache lại và phục vụ user",
                        "CDN redirect user đến origin",
                        "Request được xếp hàng",
                    ],
                    "explanation": "Khi cache miss, CDN PoP lấy từ origin, lưu vào cache cục bộ và phục vụ user. Request tiếp theo từ PoP đó là cache hit.",
                },
                {
                    "question": "Chiến lược cache invalidation tốt nhất cho JS bundle là gì?",
                    "options": [
                        "TTL rất ngắn (60s)",
                        "Dùng CDN invalidation API sau mỗi deploy",
                        "Thêm content hash vào URL file",
                        "Tắt cache cho JS",
                    ],
                    "explanation": "URL với content hash (main.a3f9b2.js) là tốt nhất — nội dung mới = URL mới = cache entry mới. Cho phép TTL rất dài với cập nhật tức thì.",
                },
                {
                    "question": "CDN giảm tải cho origin server như thế nào?",
                    "options": [
                        "Nén request trước khi chuyển tiếp",
                        "Batch nhiều request thành một",
                        "Phục vụ nội dung cache từ PoP để hầu hết request không đến origin",
                        "Chạy code ứng dụng tại edge",
                    ],
                    "explanation": "Với cache hit rate cao (80-95%), hầu hết request được phục vụ từ CDN PoP. Chỉ cache miss mới đến origin.",
                },
            ],
        },
    },
    "sql_vs_nosql_sd": {
        "lesson": {
            "title": "SQL vs NoSQL: Chọn Database Phù hợp",
            "content": """# SQL vs NoSQL

## SQL (Quan hệ)
Lưu dữ liệu trong bảng với schema cố định. Hỗ trợ ACID transaction.
**Ví dụ**: PostgreSQL, MySQL, AWS RDS
**Dùng khi**: Query phức tạp với JOIN, cần ACID, dữ liệu có cấu trúc, dữ liệu tài chính/y tế.

## Các Loại NoSQL

### Document Store (MongoDB, DynamoDB)
Document dạng JSON. Schema linh hoạt theo từng document.
**Dùng cho**: Profile user, danh mục sản phẩm, quản lý nội dung.

### Key-Value (Redis, DynamoDB)
Đơn giản: key → value. Cực kỳ nhanh.
**Dùng cho**: Caching, session, leaderboard.

### Column Family (Cassandra, HBase)
Tối ưu cho write-heavy workload, time-series.
**Dùng cho**: IoT, analytics, event log.

### Graph (Neo4j, Amazon Neptune)
Tối ưu cho dữ liệu kết nối chặt chẽ.
**Dùng cho**: Mạng xã hội, gợi ý, phát hiện gian lận.

## Khi Nào Chọn SQL
- Cần JOIN và query phức tạp
- Yêu cầu ACID transaction (thanh toán, đặt chỗ)
- Scale < 10TB, < 100K write/giây

## Khi Nào Chọn NoSQL
- Scale khổng lồ (triệu write/giây)
- Schema linh hoạt, đang phát triển
- Pattern truy cập đơn giản (lookup theo key)

## Thực tế: Netflix
Netflix dùng MySQL (billing), Cassandra (lịch sử xem), Redis (cache), Elasticsearch (tìm kiếm).

## Mẹo phỏng vấn
Đừng nói 'tùy' mà không giải thích. Mặc định PostgreSQL. Chọn Cassandra cho write throughput cực lớn, MongoDB cho schema linh hoạt, DynamoDB cho serverless scale-to-zero.""",
        },
        "quiz": {
            "title": "Quiz: SQL vs NoSQL",
            "description": "Kiểm tra hiểu biết về trade-off giữa các loại database.",
            "questions": [
                {
                    "question": "Ưu điểm chính của SQL so với hầu hết NoSQL là gì?",
                    "options": [
                        "Scale ngang dễ dàng hơn",
                        "Hỗ trợ ACID transaction cho strong consistency",
                        "Xử lý dữ liệu phi cấu trúc tốt hơn",
                        "Latency thấp hơn cho key-value lookup",
                    ],
                    "explanation": "Database SQL được xây dựng xung quanh ACID transaction. Điều này làm chúng lý tưởng cho hệ thống tài chính, y tế và đặt chỗ.",
                },
                {
                    "question": "Khi nào bạn chọn Cassandra thay vì PostgreSQL?",
                    "options": [
                        "Khi cần JOIN phức tạp",
                        "Khi cần ACID transaction cho payment",
                        "Khi cần hàng triệu write mỗi giây",
                        "Khi dữ liệu có schema cố định",
                    ],
                    "explanation": "Cassandra được thiết kế cho write throughput khổng lồ và scalability ngang tuyến tính, đánh đổi ACID và JOIN.",
                },
                {
                    "question": "Với ứng dụng fintech mới yêu cầu giao dịch tài chính, database tốt nhất là gì?",
                    "options": [
                        "MongoDB, vì linh hoạt",
                        "Cassandra, cho write throughput cao",
                        "Redis, vì nhanh",
                        "PostgreSQL, cho ACID transaction và strong consistency",
                    ],
                    "explanation": "Giao dịch tài chính yêu cầu đảm bảo ACID. PostgreSQL là mặc định công nghiệp cho dữ liệu tài chính với strong consistency và tooling trưởng thành.",
                },
            ],
        },
    },
    "rate_limiting_sd": {
        "lesson": {
            "title": "Rate Limiting: Bảo vệ API khỏi Lạm dụng",
            "content": """# Rate Limiting

Rate limiting kiểm soát **số request một client có thể thực hiện** trong khoảng thời gian nhất định.

## Tại Sao Cần Rate Limit
- Bảo vệ DDoS
- Đảm bảo sử dụng công bằng
- Kiểm soát chi phí
- Mô hình kinh doanh (gói miễn phí vs trả phí)
- Bảo vệ downstream

## Thuật Toán

### Fixed Window Counter
Đếm request theo time window (100 req/phút).
**Vấn đề**: Client có thể thực hiện 100 lúc 11:59 và 100 lúc 12:00 — 200 trong 2 giây.

### Token Bucket
Client có N token; mỗi request tốn 1 token; token nạp lại theo tốc độ R. Cho phép burst.
Twitter dùng cho API rate limiting.

### Leaky Bucket
Request xử lý theo tốc độ cố định. Làm phẳng burst. Tốt cho xử lý payment.

### Sliding Window
Xấp xỉ sliding window dùng fixed counter có trọng số. Chính xác không cần log đầy đủ.

## Triển Khai
**API Gateway ưu tiên** — tập trung, ngăn traffic trước khi đến service.

**Redis-based distributed**: Tất cả gateway instance dùng chung counter trong Redis.

## HTTP Response
```
HTTP 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
```

## Thực tế: GitHub API
5.000 request/giờ cho user đã xác thực, 60 cho ẩn danh. Trả X-RateLimit-* header trong mỗi response.

## Mẹo phỏng vấn
Đề cập: 1) Thuật toán (token bucket — cho phép burst), 2) Nơi đặt (API Gateway + Redis), 3) Giao tiếp với client (429 + Retry-After). Đặt giới hạn khác nhau theo user tier và endpoint.""",
        },
        "quiz": {
            "title": "Quiz: Rate Limiting",
            "description": "Kiểm tra kiến thức về thuật toán và triển khai rate limiting.",
            "questions": [
                {
                    "question": "HTTP status code nào request bị rate limit nhận?",
                    "options": ["400 Bad Request", "401 Unauthorized", "429 Too Many Requests", "503 Service Unavailable"],
                    "explanation": "HTTP 429 Too Many Requests là status code chuẩn cho rate limiting. Thêm Retry-After và X-RateLimit header.",
                },
                {
                    "question": "Tại sao dùng Redis cho distributed rate limiting?",
                    "options": [
                        "Redis cung cấp ACID mạnh cho counter",
                        "Tất cả API gateway instance có thể dùng chung counter trong Redis",
                        "Redis tự động implement token bucket",
                        "Redis rate limiting được tích hợp vào AWS API Gateway",
                    ],
                    "explanation": "Khi nhiều API gateway instance xử lý traffic, chúng cần dùng chung số request đếm cho mỗi user. Redis cung cấp atomic counter dùng chung.",
                },
                {
                    "question": "Nên triển khai rate limiting ở đâu trong microservices?",
                    "options": [
                        "Trong mỗi service độc lập",
                        "Ở tầng database",
                        "Tại API Gateway, tập trung",
                        "Trong ứng dụng client",
                    ],
                    "explanation": "Triển khai tại API Gateway tập trung logic — tránh trùng lặp trong mỗi service. Traffic lạm dụng bị chặn trước khi đến microservice.",
                },
            ],
        },
    },
    "distributed_transactions_sd": {
        "lesson": {
            "title": "Giao dịch Phân tán: Đảm bảo Nhất quán giữa các Service",
            "content": """# Giao dịch Phân tán

Trong microservices, mỗi service có database riêng. Làm thế nào để đảm bảo thao tác trải qua nhiều service là atomic?

## Two-Phase Commit (2PC)
Coordinator yêu cầu tất cả participant 'prepare' (lock resource). Nếu tất cả đồng ý → commit. Nếu bất kỳ từ chối → abort.

**Vấn đề**: Chậm (hai vòng RTT), blocking (nếu coordinator crash, participant giữ lock), khả dụng kém. **Hiếm khi dùng trong hệ thống hiện đại.**

## Saga Pattern
Chia transaction thành các local transaction. Mỗi bước publish event. Khi lỗi, **compensating transaction** hoàn tác bước trước.

### Choreography Saga
Service phản ứng với event độc lập — không có coordinator trung tâm.

### Orchestration Saga
Orchestrator trung tâm điều phối từng bước tường minh.

## Outbox Pattern
Vấn đề: Làm thế nào ghi vào DB VÀ publish event atomically?

Giải pháp: Ghi event vào **outbox table** trong cùng DB transaction. Process riêng đọc và publish.

## Idempotency
Retry không được gây effect trùng lặp. Thêm **idempotency key** với mỗi thao tác. Nếu thấy lần hai, trả kết quả trước mà không thực thi lại.

## Thực tế: Uber Eats
Saga: Reserve công suất nhà hàng → Charge payment → Thông báo tài xế. Khi lỗi, compensating transaction chạy. Choreography qua Kafka event.

## Mẹo phỏng vấn
'Tôi tránh 2PC vì tính blocking. Tôi dùng Saga pattern cho business transaction và Outbox pattern cho event publishing tin cậy. Tôi thiết kế thao tác idempotent để retry an toàn.'""",
        },
        "quiz": {
            "title": "Quiz: Giao dịch Phân tán",
            "description": "Kiểm tra hiểu biết về pattern giao dịch phân tán.",
            "questions": [
                {
                    "question": "Vấn đề chính của 2PC trong hệ thống phân tán là gì?",
                    "options": [
                        "Yêu cầu cùng database cho mỗi service",
                        "Blocking — nếu coordinator crash, participant giữ lock vô thời hạn",
                        "Không thể xử lý hơn hai service",
                        "Không hỗ trợ rollback",
                    ],
                    "explanation": "2PC là blocking. Sau khi vote 'yes', participant giữ resource lock và chờ coordinator. Nếu coordinator crash, chúng bị kẹt.",
                },
                {
                    "question": "Outbox Pattern giải quyết vấn đề gì?",
                    "options": [
                        "Cross-service JOIN",
                        "Ghi vào DB VÀ publish event atomically",
                        "Phối hợp distributed transaction không cần coordinator",
                        "Replay event thất bại",
                    ],
                    "explanation": "Outbox pattern giải quyết vấn đề dual-write. Ghi event vào outbox table trong cùng DB transaction đảm bảo cả hai xảy ra cùng nhau.",
                },
                {
                    "question": "'Idempotency' có nghĩa là gì?",
                    "options": [
                        "Thao tác hoàn thành trong thời gian đảm bảo",
                        "Thực hiện cùng thao tác nhiều lần tạo ra kết quả giống như thực hiện một lần",
                        "Thao tác phân phối đều giữa các instance",
                        "Mỗi service duy trì transaction log riêng",
                    ],
                    "explanation": "Idempotency nghĩa là có thể retry thao tác an toàn. Nếu 'charge customer $50' bị retry, nó kiểm tra đã charge chưa (qua idempotency key) và không charge lại.",
                },
            ],
        },
    },
    "event_driven_sd": {
        "lesson": {
            "title": "Kiến trúc Hướng Sự kiện: Xây dựng Hệ thống Phản ứng",
            "content": """# Kiến trúc Hướng Sự kiện (EDA)

Trong EDA, các thành phần giao tiếp bằng cách **produce và consume event** thay vì gọi trực tiếp nhau. Event là bản ghi bất biến về điều gì đó đã xảy ra: `OrderPlaced`, `UserRegistered`.

## Lợi Ích
- **Loose coupling**: Service không biết về nhau — chỉ biết về event schema
- **Scalability**: Thêm consumer mà không sửa producer
- **Resilience**: Event tích lũy nếu consumer tắt
- **Auditability**: Event log là lịch sử đầy đủ
- **Time travel**: Replay event để rebuild state

## Các Pattern

### Event Sourcing
Lưu trạng thái dưới dạng chuỗi event. Để lấy trạng thái hiện tại, replay tất cả event.

### CQRS (Command Query Responsibility Segregation)
Tách write model (command) khỏi read model (query). Event từ write side cập nhật read side async.

## Khi Nào Dùng EDA
- Nhiều service phản ứng với cùng event
- Service cần triển khai độc lập
- Cần audit trail
- Xử lý async throughput cao

## Khi Nào Tránh
- Cần phản hồi đồng bộ (user đang chờ)
- Request/response đơn giản là đủ

## Thực tế: Netflix
Khi bạn xem phim, `PlaybackStarted` kích hoạt: cập nhật lịch sử, model gợi ý, đếm lượt xem, billing, analytics — tất cả độc lập.

## Mẹo phỏng vấn
Đề xuất EDA khi 'nhiều service cần phản ứng với hành động user' hoặc 'cần audit log'. Thể hiện bạn hiểu trade-off: debugging khó hơn (cần distributed tracing) nhưng resilience và scalability cải thiện.""",
        },
        "quiz": {
            "title": "Quiz: Kiến trúc Hướng Sự kiện",
            "description": "Kiểm tra hiểu biết về pattern kiến trúc hướng sự kiện.",
            "questions": [
                {
                    "question": "Lợi ích chính của loose coupling trong EDA là gì?",
                    "options": [
                        "Service giao tiếp nhanh hơn với binary protocol",
                        "Service không biết về nhau — chỉ biết về event schema",
                        "Event loại bỏ API versioning",
                        "Consumer có thể gọi đồng bộ nhau",
                    ],
                    "explanation": "Trong EDA, producer publish event mà không biết ai consume. Service mới có thể được thêm mà không sửa service hiện có — loose coupling thực sự.",
                },
                {
                    "question": "Event Sourcing là gì?",
                    "options": [
                        "Lưu source code cho event handler",
                        "Lấy event từ external webhook",
                        "Lưu trạng thái dưới dạng chuỗi event bất biến và suy ra trạng thái hiện tại bằng cách replay",
                        "Cache event response để replay nhanh hơn",
                    ],
                    "explanation": "Event Sourcing không bao giờ ghi đè trạng thái — nó append event. Trạng thái hiện tại được tính bằng cách replay tất cả event, cung cấp lịch sử đầy đủ và time travel.",
                },
                {
                    "question": "Khi nào nên tránh kiến trúc hướng sự kiện?",
                    "options": [
                        "Nhiều service phản ứng với cùng hành động user",
                        "Cần phản hồi đồng bộ (user đang chờ kết quả)",
                        "Cần audit trail đầy đủ",
                        "Service cần triển khai độc lập",
                    ],
                    "explanation": "EDA là bất đồng bộ theo bản chất. Nếu user submit payment và cần xác nhận ngay, bạn không thể chờ event lan truyền.",
                },
            ],
        },
    },
    "websocket_sd": {
        "lesson": {
            "title": "WebSockets & Thời gian thực: Giao tiếp Hai chiều",
            "content": """# WebSockets & Giao tiếp Thời gian thực

HTTP truyền thống là request-response. Với tính năng real-time, bạn cần **server push dữ liệu đến client** mà không cần hỏi.

## Các Lựa Chọn

### WebSocket
Kết nối TCP hai chiều, persistent. Cả hai bên gửi bất kỳ lúc nào. Thiết lập qua HTTP upgrade.
**Dùng cho**: Chat, game multiplayer, collaboration trực tiếp, dashboard giao dịch.

### Server-Sent Events (SSE)
Một chiều: chỉ server push đến client. HTTP chuẩn. Tự kết nối lại.
**Dùng cho**: Feed tin tức trực tiếp, thông báo, cập nhật tiến độ.

### Long Polling
Client request; server giữ đến khi có dữ liệu. Overhead cao. Chỉ dùng làm fallback.

## Scale WebSocket
**Thách thức**: WebSocket stateful — gắn với một server cụ thể. User A trên Server 1 không thể đến User B trên Server 2.

**Giải pháp: Redis Pub/Sub**
1. Server 1 nhận message từ A
2. Server 1 publish lên Redis channel `chat:room:42`
3. Server 2 (subscribe channel đó) nhận
4. Server 2 push đến connection của B

## Thực tế: Slack
Slack dùng WebSocket cho messaging real-time. Message qua HTTP POST đến API, publish lên Redis Pub/Sub channel của workspace, rồi push đến tất cả client đang kết nối.

## Mẹo phỏng vấn
Khi 'real-time' được đề cập, đề xuất WebSocket + Redis Pub/Sub. Phân biệt: WebSocket (bidirectional), SSE (unidirectional feed), Long polling (fallback). Thể hiện bạn hiểu thách thức scale ngang.""",
        },
        "quiz": {
            "title": "Quiz: WebSockets & Real-time",
            "description": "Kiểm tra hiểu biết về pattern giao tiếp thời gian thực.",
            "questions": [
                {
                    "question": "Sự khác biệt chính giữa WebSocket và SSE là gì?",
                    "options": [
                        "WebSocket dùng HTTP; SSE dùng TCP",
                        "WebSocket hai chiều; SSE chỉ từ server đến client",
                        "SSE hỗ trợ binary; WebSocket chỉ text",
                        "WebSocket yêu cầu server chuyên dụng",
                    ],
                    "explanation": "WebSocket full-duplex — cả hai bên gửi message. SSE một chiều — chỉ server push. Dùng WebSocket cho chat, SSE cho notification feed.",
                },
                {
                    "question": "Redis Pub/Sub giải quyết vấn đề scale WebSocket như thế nào?",
                    "options": [
                        "Redis lưu connection state để bất kỳ server nào có thể tiếp tục",
                        "Tất cả WebSocket server subscribe Redis channel và fan out message đến client đang kết nối",
                        "Redis route connection đến server đúng",
                        "Redis đóng vai trò load balancer cho WebSocket traffic",
                    ],
                    "explanation": "Khi Server 1 nhận message, nó publish lên Redis channel. Tất cả WebSocket server subscribe channel đó push message đến user đang kết nối.",
                },
                {
                    "question": "Khi nào bạn ưu tiên SSE hơn WebSocket?",
                    "options": [
                        "Cho game multiplayer",
                        "Cho ứng dụng chat trực tiếp",
                        "Cho feed tin tức trực tiếp khi chỉ server gửi dữ liệu",
                        "Cho document editor cộng tác",
                    ],
                    "explanation": "SSE đơn giản hơn khi chỉ cần luồng dữ liệu từ server đến client. HTTP chuẩn, tự kết nối lại, dễ scale hơn. Không cần WebSocket nếu client không gửi dữ liệu.",
                },
            ],
        },
    },
    "monolith_vs_microservices_sd": {
        "lesson": {
            "title": "Monolith vs Microservices: Đưa ra Quyết định Đúng",
            "content": """# Monolith vs Microservices

## Monolith
Một đơn vị triển khai duy nhất. Cách Amazon, Netflix, Airbnb, Shopify bắt đầu.

**Ưu điểm**: Phát triển đơn giản, debug dễ, không có network overhead, deploy/rollback đơn giản.

**Nhược điểm**: Phải deploy toàn bộ để thay một dòng, không scale được từng component, bị khóa công nghệ.

## Thực tế Microservices
Độ phức tạp thêm: network failure, cần distributed tracing, nhiều CI/CD pipeline, service discovery, distributed transaction.

**Conway's Law**: Tổ chức thiết kế hệ thống phản chiếu cấu trúc giao tiếp của họ. Microservices phù hợp khi có team độc lập.

## Migration: Strangler Fig Pattern
Đừng viết lại monolith. Trích xuất service dần dần:
1. Xác định bounded context với ranh giới rõ
2. Trích xuất thành service với DB riêng
3. Route traffic đến service mới qua API Gateway
4. Xóa code khỏi monolith
5. Lặp lại

## Khi Nào Trích Xuất Service
- Module cần scale rất khác phần còn lại
- Nhiều team xung đột trên cùng module
- Muốn công nghệ khác cho component cụ thể
- Module có dữ liệu độc lập (không có cross-boundary JOIN)

## Thực tế: Amazon
Bắt đầu như monolith năm 1995. Jeff Bezos ban hành 'API Mandate' năm 2001. Hơn một thập kỷ sau, tách thành hàng nghìn microservice.

## Mẹo phỏng vấn
Đừng bao giờ nói 'microservices luôn tốt hơn.' Thể hiện sự tinh tế: 'Tôi bắt đầu với modular monolith. Khi team lớn lên hoặc xuất hiện nhu cầu scale cụ thể, tôi trích xuất service bằng Strangler Fig pattern. Microservices đến sau khi đạt product-market fit, không phải trước.'""",
        },
        "quiz": {
            "title": "Quiz: Monolith vs Microservices",
            "description": "Kiểm tra hiểu biết về trade-off quyết định kiến trúc.",
            "questions": [
                {
                    "question": "Strangler Fig pattern là gì?",
                    "options": [
                        "Loại bỏ microservice không dùng",
                        "Dần dần thay thế monolith bằng cách xây service mới xung quanh nó",
                        "Pattern cân bằng tải",
                        "Pattern migration database",
                    ],
                    "explanation": "Strangler Fig xây microservice xung quanh monolith và dần dần route traffic sang. Monolith thu nhỏ dần — tránh rủi ro rewrite toàn bộ.",
                },
                {
                    "question": "Conway's Law nói gì?",
                    "options": [
                        "Hệ thống phát triển lấp đầy tài nguyên sẵn có",
                        "Tổ chức thiết kế hệ thống phản chiếu cấu trúc giao tiếp của họ",
                        "Microservices phải có một trách nhiệm mỗi service",
                        "Hệ thống phân tán luôn có điểm lỗi",
                    ],
                    "explanation": "Conway's Law: tổ chức bị ràng buộc tạo ra thiết kế phản chiếu cấu trúc giao tiếp. Microservices phù hợp khi team được tổ chức theo ranh giới service.",
                },
                {
                    "question": "Khi nào trích xuất microservice rõ ràng là justified?",
                    "options": [
                        "Khi team đạt 5 developer",
                        "Khi module cần scale rất khác phần còn lại",
                        "Khi code vượt 10.000 dòng",
                        "Khi app hơn 2 năm tuổi",
                    ],
                    "explanation": "Nếu module xử lý ảnh cần CPU gấp 50x phần còn lại, trích xuất thành service và scale độc lập. Đây là driver kỹ thuật thực sự.",
                },
            ],
        },
    },
}
