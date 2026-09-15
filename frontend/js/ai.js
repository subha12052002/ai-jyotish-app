/**
 * AI Jyotish — AI Assistant Module
 * --------------------------------
 * Handles the AI astrology question interface.
 *
 * The backend remains responsible for the actual AI response.
 */

(function () {
    "use strict";

    const MODULE_NAME = "AIJyotishAI";

    let activeRequest = false;

    function escapeHtml(value) {
        if (value === null || value === undefined) {
            return "";
        }

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function getElement(id) {
        return document.getElementById(id);
    }

    function setLoading(button, loading) {
        if (!button) return;

        if (loading) {
            if (!button.dataset.originalText) {
                button.dataset.originalText =
                    button.textContent;
            }

            button.disabled = true;
            button.classList.add("is-loading");
            button.innerHTML = `
                <span class="ai-button-spinner"></span>
                <span>Thinking...</span>
            `;
        } else {
            button.disabled = false;
            button.classList.remove("is-loading");

            button.textContent =
                button.dataset.originalText ||
                "Ask AI";
        }
    }

    function getAnswerElement() {
        return (
            getElement("answer") ||
            document.querySelector(
                ".ai-answer"
            )
        );
    }

    function setAnswer(message, type = "normal") {
        const answer =
            getAnswerElement();

        if (!answer) return;

        answer.classList.remove(
            "is-loading",
            "is-error",
            "is-success"
        );

        if (type === "error") {
            answer.classList.add("is-error");
        }

        if (type === "success") {
            answer.classList.add("is-success");
        }

        answer.innerHTML =
            formatResponse(message);
    }

    function formatResponse(text) {
        if (
            text === null ||
            text === undefined
        ) {
            return "";
        }

        let content = String(text);

        /*
         * Escape first so AI output cannot inject HTML.
         */
        content = escapeHtml(content);

        /*
         * Basic readable formatting.
         * This deliberately does not use innerHTML
         * from the raw AI response.
         */

        content = content
            .replace(
                /\*\*(.*?)\*\*/g,
                "<strong>$1</strong>"
            )
            .replace(
                /\*(.*?)\*/g,
                "<em>$1</em>"
            )
            .replace(
                /^###\s?(.*?)$/gm,
                "<h4>$1</h4>"
            )
            .replace(
                /^##\s?(.*?)$/gm,
                "<h4>$1</h4>"
            )
            .replace(
                /^#\s?(.*?)$/gm,
                "<h4>$1</h4>"
            );

        const lines =
            content.split("\n");

        let html = "";
        let listOpen = false;

        lines.forEach(line => {
            const trimmed =
                line.trim();

            if (!trimmed) {
                if (listOpen) {
                    html += "</ul>";
                    listOpen = false;
                }

                html += "<div class=\"ai-space\"></div>";
                return;
            }

            if (
                trimmed.startsWith("- ") ||
                trimmed.startsWith("• ")
            ) {
                if (!listOpen) {
                    html += "<ul>";
                    listOpen = true;
                }

                html += `
                    <li>
                        ${trimmed.substring(2)}
                    </li>
                `;

                return;
            }

            if (listOpen) {
                html += "</ul>";
                listOpen = false;
            }

            if (
                trimmed.startsWith("<h4>")
            ) {
                html += trimmed;
            } else {
                html += `
                    <p>${trimmed}</p>
                `;
            }
        });

        if (listOpen) {
            html += "</ul>";
        }

        return html;
    }

    function getQuestion() {
        const input =
            getElement("question");

        return input
            ? input.value.trim()
            : "";
    }

    function validateQuestion(question) {
        if (!question) {
            return "Please enter a question.";
        }

        if (question.length < 3) {
            return "Please enter a more detailed question.";
        }

        if (question.length > 2000) {
            return "Please keep your question under 2000 characters.";
        }

        return null;
    }

    function getChartFromStorage() {
        try {
            const cached =
                sessionStorage.getItem(
                    "aiJyotishLatestChart"
                );

            if (!cached) {
                return null;
            }

            return JSON.parse(cached);
        } catch {
            return null;
        }
    }

    async function ask(question, chart = null) {
        const validation =
            validateQuestion(question);

        if (validation) {
            throw new Error(validation);
        }

        if (activeRequest) {
            throw new Error(
                "Please wait for the current response."
            );
        }

        activeRequest = true;

        try {
            const payload = {
                question
            };

            /*
             * The backend can use its own latest Kundli
             * context. We only send chart context when
             * available and already present on the client.
             */
            if (chart) {
                payload.chart = chart;
            }

            const response =
                await fetch(
                    "/api/ai/ask",
                    {
                        method: "POST",
                        credentials: "include",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body:
                            JSON.stringify(
                                payload
                            )
                    }
                );

            let data = {};

            try {
                data =
                    await response.json();
            } catch {
                data = {};
            }

            if (!response.ok) {
                throw new Error(
                    data.error ||
                    data.message ||
                    "Unable to get an AI response."
                );
            }

            return {
                answer:
                    data.answer ||
                    data.response ||
                    data.message ||
                    data.result ||
                    "No answer was returned.",
                raw: data
            };
        } finally {
            activeRequest = false;
        }
    }

    async function submit() {
        const form =
            getElement("aiForm");

        const input =
            getElement("question");

        const button =
            form?.querySelector(
                'button[type="submit"]'
            );

        const question =
            getQuestion();

        const validation =
            validateQuestion(question);

        if (validation) {
            setAnswer(
                validation,
                "error"
            );
            return;
        }

        if (activeRequest) {
            return;
        }

        const chart =
            getChartFromStorage();

        setLoading(
            button,
            true
        );

        const answer =
            getAnswerElement();

        if (answer) {
            answer.classList.add(
                "is-loading"
            );

            answer.innerHTML = `
                <div class="ai-thinking">
                    <div class="ai-thinking-orbit">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>

                    <div>
                        <strong>
                            Reading your chart...
                        </strong>

                        <p>
                            AI Jyotish is preparing
                            your interpretation.
                        </p>
                    </div>
                </div>
            `;
        }

        try {
            const result =
                await ask(
                    question,
                    chart
                );

            setAnswer(
                result.answer,
                "success"
            );
        } catch (error) {
            setAnswer(
                error.message ||
                    "Something went wrong while asking AI Jyotish.",
                "error"
            );
        } finally {
            setLoading(
                button,
                false
            );
        }
    }

    function addSuggestion(text) {
        const container =
            document.querySelector(
                ".ai-suggestions"
            );

        if (!container) return;

        const button =
            document.createElement(
                "button"
            );

        button.type = "button";
        button.className =
            "ai-suggestion";

        button.textContent = text;

        button.addEventListener(
            "click",
            () => {
                const input =
                    getElement("question");

                if (!input) return;

                input.value = text;
                input.focus();
            }
        );

        container.appendChild(
            button
        );
    }

    function initSuggestions() {
        const container =
            document.querySelector(
                ".ai-suggestions"
            );

        if (!container) return;

        /*
         * Do not add duplicates if suggestions
         * are already present in the HTML.
         */
        if (
            container.children.length > 0
        ) {
            container
                .querySelectorAll(
                    "button, .ai-suggestion"
                )
                .forEach(button => {
                    button.addEventListener(
                        "click",
                        () => {
                            const input =
                                getElement(
                                    "question"
                                );

                            if (!input) {
                                return;
                            }

                            input.value =
                                button.textContent.trim();

                            input.focus();
                        }
                    );
                });

            return;
        }

        [
            "What are my strongest planets?",
            "What does my Moon sign indicate?",
            "Tell me about my career potential.",
            "What does my current Dasha mean?"
        ].forEach(addSuggestion);
    }

    function init() {
        const form =
            getElement("aiForm");

        if (!form) return;

        /*
         * Prevent duplicate listeners if this module
         * is initialized more than once.
         */
        if (
            form.dataset.aiInitialized ===
            "true"
        ) {
            return;
        }

        form.dataset.aiInitialized =
            "true";

        form.addEventListener(
            "submit",
            event => {
                event.preventDefault();
                submit();
            }
        );

        initSuggestions();

        const input =
            getElement("question");

        if (input) {
            input.addEventListener(
                "keydown",
                event => {
                    if (
                        event.key === "Enter" &&
                        !event.shiftKey
                    ) {
                        event.preventDefault();
                        submit();
                    }
                }
            );
        }
    }

    window[MODULE_NAME] = {
        init,
        ask,
        submit,
        setAnswer,
        formatResponse,
        getChartFromStorage
    };

    if (
        document.readyState ===
        "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            init
        );
    } else {
        init();
    }
})();