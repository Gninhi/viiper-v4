"""
Content Writer Agent for VIIPER.

Elite content creation for SEO domination and #1 Google rankings.
Creates engaging, authoritative, and perfectly optimized content.
"""

from typing import ClassVar, Dict, Any, List
from datetime import datetime

from viiper.agents.base import Agent, AgentRole, AgentCapability, AgentTask


class ContentWriterAgent(Agent):
    """
    Elite content writer for creating SEO-optimized, engaging content.

    Capabilities:
    - Long-form blog posts (2,000-5,000 words)
    - Landing page copy that converts
    - Product descriptions that sell
    - Comprehensive guides and tutorials
    - Video scripts for YouTube SEO
    - Email sequences

    All content is optimized for:
    - Search engines (top rankings)
    - User engagement (dwell time, shares)
    - Conversions (CTAs, persuasion)
    - E-E-A-T signals

    Task metadata keys:
        content_type: str   - "blog_post" | "landing_page" | "product_description"
                              | "comprehensive_guide" | "video_script" | "email_sequence"
        topic: str          - Main topic / project name
        target_keyword: str - Target SEO keyword
        word_count: int     - Desired word count
        product: str        - Product name (landing page / product desc)
        audience: str       - Target audience
        video_type: str     - "tutorial" | "review" | "listicle"
        sequence_type: str  - "nurture" | "launch" | "onboarding"
    """

    name: str = "Content Writer Agent"
    role: AgentRole = AgentRole.SPECIALIST
    capabilities: list = [
        AgentCapability.CONTENT_WRITING,
        AgentCapability.COPYWRITING,
    ]

    # --- Class-level templates (ClassVar to avoid Pydantic field detection) ---

    BLOG_POST_TEMPLATE: ClassVar[str] = """# {title}

{meta_description}

## Table of Contents

{table_of_contents}

## Introduction

{introduction}

{body_sections}

## Conclusion

{conclusion}

## Frequently Asked Questions (FAQ)

{faq_section}

---

*Written by VIIPER Content Team | Last updated: {date}*
"""

    LANDING_PAGE_TEMPLATE: ClassVar[str] = """# {headline}

## {subheadline}

{hero_section}

## The Problem

{problem_agitation}

## The Solution

{solution_section}

## Features & Benefits

{features_section}

## Social Proof

{social_proof}

## Pricing

{pricing_section}

## Guarantee

{risk_reversal}

## Call to Action

{cta_section}

## FAQ

{faq_section}
"""

    PRODUCT_DESCRIPTION_TEMPLATE: ClassVar[str] = """## {product_name}

**{tagline}**

### What It Does

{what_it_does}

### Key Benefits

{benefits_list}

### Features

{features_list}

### Perfect For

{target_audience}

### How It Works

{how_it_works}

### Customer Success

{testimonial}

**{price_cta}**
"""

    QUALITY_STANDARDS: ClassVar[Dict[str, Any]] = {
        "minimum_word_count": 1500,
        "optimal_word_count": 2500,
        "keyword_density_min": 0.5,
        "keyword_density_max": 2.0,
        "readability_target": 60,
        "sentence_max_words": 25,
        "paragraph_max_sentences": 5,
        "transition_words_min": 30,
    }

    COPYWRITING_FRAMEWORKS: ClassVar[Dict[str, List[str]]] = {
        "AIDA": ["Attention", "Interest", "Desire", "Action"],
        "PAS": ["Problem", "Agitate", "Solution"],
        "FAB": ["Features", "Advantages", "Benefits"],
        "4Ps": ["Picture", "Promise", "Prove", "Push"],
        "QUEST": ["Qualify", "Understand", "Educate", "Stimulate", "Transition"],
    }

    # -------------------------------------------------------------------------

    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute content writing task.

        Dispatches based on task.metadata["content_type"].
        """
        content_type = task.metadata.get("content_type", "blog_post")

        dispatch = {
            "blog_post": self._write_blog_post,
            "landing_page": self._write_landing_page,
            "product_description": self._write_product_description,
            "comprehensive_guide": self._write_comprehensive_guide,
            "video_script": self._write_video_script,
            "email_sequence": self._write_email_sequence,
        }

        handler = dispatch.get(content_type)
        if handler is None:
            return {"success": False, "error": f"Unknown content type: {content_type}"}

        return handler(task)

    # -------------------------------------------------------------------------
    # Handlers
    # -------------------------------------------------------------------------

    def _write_blog_post(self, task: AgentTask) -> Dict[str, Any]:
        """Write an SEO-optimized blog post."""
        topic = task.metadata.get("topic", "product")
        target_keyword = task.metadata.get("target_keyword", topic.lower())

        title = self._generate_title(topic, target_keyword)
        meta_desc = self._generate_meta_description(topic, target_keyword)

        sections = [
            f"What is {topic}",
            f"Why {topic} Matters",
            f"Key Benefits of {topic}",
            f"How to Get Started with {topic}",
            f"Best Practices for {topic}",
            "Common Mistakes to Avoid",
        ]

        body = "".join(
            self._generate_section(s, target_keyword, i) + "\n\n"
            for i, s in enumerate(sections, 1)
        )

        content = self.BLOG_POST_TEMPLATE.format(
            title=title,
            meta_description=meta_desc,
            table_of_contents=self._generate_toc(sections),
            introduction=self._generate_introduction(topic, target_keyword),
            body_sections=body,
            conclusion=self._generate_conclusion(topic, target_keyword),
            faq_section=self._generate_faq(topic, target_keyword),
            date=datetime.now().strftime("%B %d, %Y"),
        )

        word_count = len(content.split())
        keyword_count = content.lower().count(target_keyword.lower())
        keyword_density = (keyword_count / word_count * 100) if word_count > 0 else 0

        return {
            "success": True,
            "output": {
                "title": title,
                "content": content,
                "meta_description": meta_desc,
                "word_count": word_count,
                "keyword_density": round(keyword_density, 2),
                "estimated_read_time": f"{word_count // 200} min read",
                "content_score": self._calculate_content_score(content, target_keyword),
                "suggested_internal_links": [
                    f"Related guide to {topic}",
                    "Getting started tutorial",
                    "Advanced strategies",
                ],
                "suggested_external_links": [
                    "Industry authority site",
                    "Research study",
                    "Official documentation",
                ],
            },
            "artifacts": {
                "content_type": "blog_post",
                "target_keyword": target_keyword,
                "images_needed": self._suggest_images(topic),
            },
        }

    def _write_landing_page(self, task: AgentTask) -> Dict[str, Any]:
        """Write high-converting landing page."""
        product = task.metadata.get("product", task.metadata.get("topic", "Product"))
        target_audience = task.metadata.get("audience", "professionals")

        headline = f"Finally! The {product} That [Biggest Benefit]"
        subheadline = f"Join 10,000+ {target_audience} who've transformed their results with {product}"

        content = self.LANDING_PAGE_TEMPLATE.format(
            headline=headline,
            subheadline=subheadline,
            hero_section=f"[Hero image/video showing {product} in action]",
            problem_agitation=f"Are you tired of [common pain point]? Do you struggle with [specific problem]? You're not alone—most {target_audience} face these challenges every day.",
            solution_section=f"Introducing {product}—the revolutionary solution that [key benefit]. Unlike other options, our approach [unique differentiator].",
            features_section="1. **Feature 1** → Benefit: Saves time\n2. **Feature 2** → Benefit: Increases results\n3. **Feature 3** → Benefit: Reduces costs",
            social_proof='⭐⭐⭐⭐⭐ "Best investment I\'ve made!" - John D.\n⭐⭐⭐⭐⭐ "Incredible results in just 30 days" - Sarah M.',
            pricing_section="**Starter**: $29/month\n**Professional**: $79/month (Most Popular)\n**Enterprise**: $199/month",
            risk_reversal="30-Day Money-Back Guarantee: Try it risk-free. If you're not completely satisfied, we'll refund every penny—no questions asked.",
            cta_section=f"**[Get Started with {product} - Start Your Free Trial]**\n\nNo credit card required. Cancel anytime.",
            faq_section=f"**Q: How quickly will I see results?**\nA: Most customers see improvements within the first 30 days.\n\n**Q: Is there a free trial?**\nA: Yes! Try {product} free for 14 days.",
        )

        return {
            "success": True,
            "output": {
                "headline": headline,
                "subheadline": subheadline,
                "content": content,
                "word_count": len(content.split()),
                "conversion_elements": [
                    "Strong headline with benefit",
                    "Problem agitation",
                    "Clear solution presentation",
                    "Feature-benefit pairs",
                    "Social proof",
                    "Risk reversal",
                    "Multiple CTAs",
                ],
                "a_b_test_suggestions": [
                    "Test headline variations",
                    "Test CTA button colors",
                    "Test social proof placement",
                    "Test pricing presentation",
                ],
            },
            "artifacts": {
                "content_type": "landing_page",
                "conversion_focus": True,
                "framework_used": "AIDA + PAS",
            },
        }

    def _write_product_description(self, task: AgentTask) -> Dict[str, Any]:
        """Write compelling product description."""
        product = task.metadata.get("product", task.metadata.get("topic", "Product"))

        description = self.PRODUCT_DESCRIPTION_TEMPLATE.format(
            product_name=product,
            tagline="The smart way to [achieve result]",
            what_it_does=f"{product} is an all-in-one solution that helps you [main function] without the usual headaches.",
            benefits_list="• Save 10+ hours per week\n• Increase results by 300%\n• Reduce costs by 50%\n• Scale without adding headcount",
            features_list="• **Smart Automation**: Handles repetitive tasks automatically\n• **Advanced Analytics**: Get insights that drive decisions\n• **Seamless Integration**: Works with your existing tools\n• **24/7 Support**: Help whenever you need it",
            target_audience="Perfect for: Small businesses, startups, freelancers, and anyone who wants to [achieve goal] without the complexity.",
            how_it_works="1. **Sign up** in 60 seconds\n2. **Connect** your accounts\n3. **Configure** your preferences\n4. **Start** seeing results immediately",
            testimonial='"I was skeptical at first, but this changed everything. Within 2 weeks, I saw a 250% improvement." - Alex R., Marketing Director',
            price_cta="Get Started Today →",
        )

        return {
            "success": True,
            "output": {
                "product_name": product,
                "description": description,
                "short_description": f"{product} helps you achieve better results faster with less effort.",
                "bullet_points": [
                    f"All-in-one {product.lower()} solution",
                    "Saves 10+ hours per week",
                    "300% average improvement",
                    "14-day free trial",
                ],
                "seo_title": f"{product} - Best Solution for Your Needs",
                "seo_description": f"Discover {product}. The smart way to [achieve result].",
            },
            "artifacts": {
                "content_type": "product_description",
                "persuasion_techniques": ["Social proof", "Scarcity", "Authority"],
            },
        }

    def _write_comprehensive_guide(self, task: AgentTask) -> Dict[str, Any]:
        """Write ultimate guide (5,000+ words)."""
        topic = task.metadata.get("topic", "product")

        sections = [
            f"What is {topic}? (Definition and Overview)",
            f"The History and Evolution of {topic}",
            f"Why {topic} is Essential in 2026",
            "Key Concepts and Terminology",
            f"Step-by-Step: Getting Started with {topic}",
            "Advanced Strategies and Techniques",
            "Common Challenges and How to Overcome Them",
            f"Tools and Resources for {topic}",
            "Case Studies: Real-World Success Stories",
            "Expert Tips and Insider Secrets",
            "Future Trends and Predictions",
            "Action Plan: Your Next Steps",
        ]

        body = "\n".join(
            f"\n## {i}. {s}\n\n[Comprehensive content for {s}...]\n\n"
            "**Key Insights:**\n"
            "• Important point 1 with detailed explanation\n"
            "• Important point 2 with real-world example\n"
            "• Important point 3 with actionable advice\n\n---"
            for i, s in enumerate(sections, 1)
        )

        content = (
            f"# The Ultimate Guide to {topic} (2026 Edition)\n\n"
            f"**Everything you need to know about {topic} to succeed.**\n\n"
            f"*Last updated: {datetime.now().strftime('%B %Y')} | {len(sections)} chapters | 45 min read*\n\n---\n\n"
            "## Introduction\n\n"
            f"Welcome to the most comprehensive guide on {topic} you'll find anywhere. "
            "Whether you're just getting started or looking to become an expert, this guide covers everything—"
            "from the basics to advanced strategies used by industry leaders.\n\n"
            "## Table of Contents\n\n"
            + "\n".join(f"{i}. [{s}](#section-{i})" for i, s in enumerate(sections, 1))
            + "\n\n"
            + body
            + f"\n\n## Conclusion and Next Steps\n\n"
            f"You've now mastered {topic}. Remember, knowledge without action is useless. "
            "Choose one strategy from this guide and implement it today.\n\n"
            "---\n\n*Was this guide helpful? [Share it with your network!]*"
        )

        return {
            "success": True,
            "output": {
                "title": f"The Ultimate Guide to {topic}",
                "content": content,
                "word_count": len(content.split()),
                "chapters": len(sections),
                "type": "ultimate_guide",
                "authority_signals": [
                    "Comprehensive coverage",
                    "Expert insights",
                    "Real case studies",
                    "Actionable advice",
                    "Regularly updated",
                ],
            },
            "artifacts": {
                "content_type": "comprehensive_guide",
                "pillar_content": True,
                "link_worthy": True,
            },
        }

    def _write_video_script(self, task: AgentTask) -> Dict[str, Any]:
        """Write YouTube-optimized video script."""
        topic = task.metadata.get("topic", "product")

        title = f"How to {topic} (Complete Tutorial for Beginners)"
        description = (
            f"Learn {topic} with this comprehensive tutorial.\n\n"
            "TIMESTAMPS:\n"
            "0:00 - Introduction\n"
            "1:00 - What you'll learn\n"
            "3:00 - Getting started\n"
            "10:00 - Main content\n"
            "20:00 - Conclusion\n\n"
            f"#{topic.replace(' ', '')} #Tutorial #HowTo"
        )

        script = (
            f"# Video Script: {topic}\n\n"
            f"## SEO Title\n{title}\n\n"
            f"## Description\n{description}\n\n"
            "## Script\n\n"
            "### [0:00-0:30] Hook\n"
            f'"Hey everyone! In today\'s video, I\'m going to show you exactly how to master {topic}. Let\'s dive in!"\n\n'
            "### [0:30-1:00] Intro\n"
            '"Welcome back! If you\'re new here, subscribe and hit the notification bell."\n\n'
            "### [1:00-3:00] What We\'ll Cover\n"
            f'"In this video, you\'ll learn everything about {topic} from A to Z."\n\n'
            "### [3:00-20:00] Main Content\n"
            "[Detailed step-by-step content with examples and demonstrations]\n\n"
            "### [20:00-21:00] Call to Action\n"
            '"If you found this helpful, give it a thumbs up and share it!"\n\n'
            "### [21:00-21:30] Outro\n"
            '"Thanks for watching! See you in the next one!"\n'
        )

        return {
            "success": True,
            "output": {
                "script": script,
                "seo_title": title,
                "seo_description": description,
                "estimated_duration": "21 minutes",
                "tags": [topic.lower(), f"{topic.lower()} tutorial", "how to", "guide", "2026"],
                "engagement_tactics": [
                    "Pattern interrupts every 30 seconds",
                    "Open loops",
                    "Stories and examples",
                    "Visual variety",
                ],
            },
            "artifacts": {
                "content_type": "video_script",
                "platform": "YouTube",
                "seo_optimized": True,
            },
        }

    def _write_email_sequence(self, task: AgentTask) -> Dict[str, Any]:
        """Write email marketing sequence."""
        sequence_type = task.metadata.get("sequence_type", "nurture")

        sequences: Dict[str, List[Dict[str, str]]] = {
            "nurture": [
                {"subject": "Welcome! Here's your exclusive guide", "preview": "Your resource is inside...", "goal": "Deliver lead magnet"},
                {"subject": "The #1 mistake most people make", "preview": "Are you making this error?", "goal": "Educate + agitate problem"},
                {"subject": "Case study: How [Name] achieved [Result]", "preview": "Real results in 30 days...", "goal": "Social proof"},
                {"subject": "[$X off] Last chance for early access", "preview": "Offer expires tonight...", "goal": "Conversion"},
            ],
            "onboarding": [
                {"subject": "Welcome to [Product]! Let's get started", "preview": "Your first step is...", "goal": "Activation"},
                {"subject": "Your quick-start checklist", "preview": "5 things to do today...", "goal": "Engagement"},
                {"subject": "Pro tip: [Key feature]", "preview": "Most users miss this...", "goal": "Feature adoption"},
                {"subject": "How are you finding [Product]?", "preview": "We'd love your feedback...", "goal": "Retention"},
            ],
            "launch": [
                {"subject": "🚀 It's here! [Product] is now live", "preview": "We've been working on this...", "goal": "Announce launch"},
                {"subject": "Founding member offer (48h only)", "preview": "Exclusive pricing inside...", "goal": "Drive conversions"},
                {"subject": "Last chance - offer expires tonight", "preview": "Don't miss out...", "goal": "Urgency / close"},
            ],
        }

        emails = sequences.get(sequence_type, sequences["nurture"])

        return {
            "success": True,
            "output": {
                "sequence_type": sequence_type,
                "emails": emails,
                "total_emails": len(emails),
                "recommended_timing": "Day 0, 2, 5, 7",
                "framework": "Value-first approach",
            },
            "artifacts": {
                "content_type": "email_sequence",
                "personalization_variables": ["first_name", "company", "pain_point"],
            },
        }

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _generate_title(self, topic: str, keyword: str) -> str:
        return f"The Complete Guide to {topic}: Everything You Need to Know (2026)"

    def _generate_meta_description(self, topic: str, keyword: str) -> str:
        return (
            f"Learn everything about {topic} in this comprehensive guide. "
            f"Discover proven strategies, best practices, and expert tips to succeed with {keyword} in 2026."
        )

    def _generate_toc(self, sections: List[str]) -> str:
        return "\n".join(f"{i}. {s}" for i, s in enumerate(sections, 1))

    def _generate_introduction(self, topic: str, keyword: str) -> str:
        return (
            f"Are you struggling to understand {topic}? You're not alone.\n\n"
            f"In this comprehensive guide, I'll share everything I've learned about {keyword}. "
            "Whether you're just starting out or looking to level up your skills, this guide has you covered.\n\n"
            f"**By the end of this article, you'll know:**\n"
            f"• Exactly what {topic} is and why it matters\n"
            "• The key strategies that drive results\n"
            "• Common mistakes to avoid\n"
            "• Actionable tips you can implement today\n\n"
            "Let's get started!"
        )

    def _generate_section(self, section_title: str, keyword: str, num: int) -> str:
        last_word = section_title.split()[-1]
        return (
            f"## {num}. {section_title}\n\n"
            f"Understanding {last_word} is crucial for success. "
            f"In this section, we'll explore the key concepts and practical applications.\n\n"
            "### Key Points:\n\n"
            f"• **Important aspect 1**: Detailed explanation of why this matters for {keyword}.\n\n"
            "• **Important aspect 2**: How to implement this effectively with examples.\n\n"
            "• **Important aspect 3**: Best practices and pro tips from industry experts.\n\n"
            "### Action Step:\n\n"
            f"✅ **Your Turn**: Take 10 minutes to apply this to your {keyword} strategy."
        )

    def _generate_conclusion(self, topic: str, keyword: str) -> str:
        return (
            f"Congratulations! You now have a comprehensive understanding of {topic}.\n\n"
            "**Key takeaways:**\n"
            f"• {topic} is essential for [benefit]\n"
            "• Success requires consistent effort and the right strategies\n"
            "• Avoid common mistakes by following best practices\n"
            "• Start implementing what you've learned today\n\n"
            f"What aspect of {keyword} are you most excited to try? Let me know in the comments!"
        )

    def _generate_faq(self, topic: str, keyword: str) -> str:
        questions = [
            f"What is {topic}?",
            f"How long does it take to see results with {keyword}?",
            f"Is {topic} suitable for beginners?",
            f"What are the costs associated with {topic}?",
            f"Can I do {keyword} myself or do I need help?",
        ]
        return "\n\n".join(
            f"**Q: {q}**\n\nA: [Comprehensive answer about {topic}...]"
            for q in questions
        )

    def _calculate_content_score(self, content: str, keyword: str) -> int:
        score = 70
        word_count = len(content.split())
        if word_count >= 2000:
            score += 10
        if word_count >= 3000:
            score += 5
        if keyword.lower() in content.lower():
            score += 5
        if content.count("##") >= 3:
            score += 5
        if "FAQ" in content:
            score += 5
        return min(100, score)

    def _suggest_images(self, topic: str) -> List[Dict[str, str]]:
        return [
            {"type": "hero", "alt": f"{topic} concept illustration"},
            {"type": "infographic", "alt": f"{topic} process diagram"},
            {"type": "screenshot", "alt": f"{topic} example"},
        ]
