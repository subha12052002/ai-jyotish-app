(function () {
    "use strict";

    const API = window.AIJyotishAPI || window.API;

    function $(id) {
        return document.getElementById(id);
    }

    function escapeHTML(value) {
        return String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function showMessage(element, message, type = "error") {
        if (!element) return;

        element.textContent = message || "";
        element.className = "auth-message";

        if (type) {
            element.classList.add(`auth-message-${type}`);
        }

        element.hidden = !message;
    }

    function setLoading(form, loading, label) {
        if (!form) return;

        form.classList.toggle("is-loading", loading);

        const buttons = form.querySelectorAll(
            'button[type="submit"], input[type="submit"]'
        );

        buttons.forEach((button) => {
            if (loading) {
                button.disabled = true;

                if (!button.dataset.originalText) {
                    button.dataset.originalText =
                        button.textContent || label || "Continue";
                }

                button.innerHTML = `
                    <span class="auth-spinner"></span>
                    <span>${escapeHTML(label || "Please wait…")}</span>
                `;
            } else {
                button.disabled = false;

                if (button.dataset.originalText) {
                    button.textContent =
                        button.dataset.originalText;
                }
            }
        });
    }

    function getMessage(data, fallback) {
        if (!data) return fallback;

        return (
            data.error ||
            data.message ||
            data.detail ||
            fallback
        );
    }

    function redirectAfterAuth(data, fallback) {
        const redirect =
            data?.redirect ||
            data?.next ||
            sessionStorage.getItem("aiJyotishAfterAuth") ||
            fallback;

        sessionStorage.removeItem("aiJyotishAfterAuth");

        window.location.href = redirect;
    }

    function setupPasswordToggle() {
        const toggles = document.querySelectorAll(
            "[data-password-toggle]"
        );

        toggles.forEach((toggle) => {
            const targetId =
                toggle.getAttribute("data-password-toggle");

            const input =
                targetId
                    ? $(targetId)
                    : toggle.parentElement?.querySelector(
                        'input[type="password"], input[type="text"]'
                    );

            if (!input) return;

            toggle.addEventListener("click", () => {
                const hidden =
                    input.type === "password";

                input.type = hidden
                    ? "text"
                    : "password";

                toggle.classList.toggle(
                    "is-visible",
                    hidden
                );

                toggle.setAttribute(
                    "aria-label",
                    hidden
                        ? "Hide password"
                        : "Show password"
                );
            });
        });
    }

    function setupPasswordStrength() {
        const password = $("password");

        if (!password) return;

        const indicator =
            document.querySelector(".password-strength");

        if (!indicator) return;

        const fill =
            indicator.querySelector(".password-strength-fill");

        const text =
            indicator.querySelector(".password-strength-text");

        function calculate(value) {
            if (!value) {
                return {
                    level: 0,
                    label: ""
                };
            }

            let score = 0;

            if (value.length >= 8) score++;
            if (value.length >= 12) score++;
            if (/[a-z]/.test(value)) score++;
            if (/[A-Z]/.test(value)) score++;
            if (/[0-9]/.test(value)) score++;
            if (/[^A-Za-z0-9]/.test(value)) score++;

            if (score <= 2) {
                return {
                    level: 1,
                    label: "Weak"
                };
            }

            if (score <= 4) {
                return {
                    level: 2,
                    label: "Moderate"
                };
            }

            return {
                level: 3,
                label: "Strong"
            };
        }

        password.addEventListener("input", () => {
            const result =
                calculate(password.value);

            indicator.dataset.level =
                result.level;

            if (fill) {
                fill.style.width =
                    `${(result.level / 3) * 100}%`;
            }

            if (text) {
                text.textContent =
                    result.label;
            }
        });
    }

    function validateEmail(value) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
            value
        );
    }

    function validateLogin(email, password) {
        if (!email) {
            return "Please enter your email address.";
        }

        if (!validateEmail(email)) {
            return "Please enter a valid email address.";
        }

        if (!password) {
            return "Please enter your password.";
        }

        return null;
    }

    function validateRegister(
        name,
        email,
        password,
        confirm
    ) {
        if (!name) {
            return "Please enter your name.";
        }

        if (name.length < 2) {
            return "Your name must contain at least 2 characters.";
        }

        if (!email) {
            return "Please enter your email address.";
        }

        if (!validateEmail(email)) {
            return "Please enter a valid email address.";
        }

        if (!password) {
            return "Please create a password.";
        }

        if (password.length < 6) {
            return "Password must contain at least 6 characters.";
        }

        if (password !== confirm) {
            return "Passwords do not match.";
        }

        return null;
    }

    async function handleLogin(event) {
        event.preventDefault();

        const form = event.currentTarget;

        const email =
            $("email")?.value.trim() || "";

        const password =
            $("password")?.value || "";

        const message =
            $("loginMessage") ||
            form.querySelector(".auth-message");

        const validationError =
            validateLogin(
                email,
                password
            );

        if (validationError) {
            showMessage(
                message,
                validationError,
                "error"
            );
            return;
        }

        if (!API) {
            showMessage(
                message,
                "API service is unavailable.",
                "error"
            );
            return;
        }

        setLoading(
            form,
            true,
            "Signing in…"
        );

        try {
            const result =
                await API.login({
                    email,
                    password
                });

            showMessage(
                message,
                "Welcome back. Opening your Jyotish dashboard…",
                "success"
            );

            setTimeout(() => {
                redirectAfterAuth(
                    result,
                    "dashboard.html"
                );
            }, 350);
        } catch (error) {
            console.error(
                "Login error:",
                error
            );

            showMessage(
                message,
                error.message ||
                "Login failed. Please check your details and try again.",
                "error"
            );

            setLoading(
                form,
                false,
                "Sign in"
            );
        }
    }

    async function handleRegister(event) {
        event.preventDefault();

        const form = event.currentTarget;

        const name =
            $("name")?.value.trim() || "";

        const email =
            $("email")?.value.trim() || "";

        const password =
            $("password")?.value || "";

        const confirm =
            $("confirm")?.value || "";

        const message =
            $("registerMessage") ||
            form.querySelector(".auth-message");

        const validationError =
            validateRegister(
                name,
                email,
                password,
                confirm
            );

        if (validationError) {
            showMessage(
                message,
                validationError,
                "error"
            );
            return;
        }

        if (!API) {
            showMessage(
                message,
                "API service is unavailable.",
                "error"
            );
            return;
        }

        setLoading(
            form,
            true,
            "Creating account…"
        );

        try {
            const result =
                await API.register({
                    name,
                    email,
                    password,
                    confirm
                });

            showMessage(
                message,
                "Account created successfully. Welcome to AI Jyotish.",
                "success"
            );

            setTimeout(() => {
                redirectAfterAuth(
                    result,
                    "dashboard.html"
                );
            }, 450);
        } catch (error) {
            console.error(
                "Registration error:",
                error
            );

            showMessage(
                message,
                error.message ||
                "Registration failed. Please try again.",
                "error"
            );

            setLoading(
                form,
                false,
                "Create account"
            );
        }
    }

    async function handleLogout() {
        if (!API) {
            window.location.href =
                "login.html";
            return;
        }

        try {
            await API.logout();
        } catch (error) {
            console.warn(
                "Logout request failed:",
                error
            );
        } finally {
            window.location.href =
                "login.html";
        }
    }

    function setupLogout() {
        const buttons =
            document.querySelectorAll(
                "#logoutBtn, [data-action='logout']"
            );

        buttons.forEach((button) => {
            button.addEventListener(
                "click",
                (event) => {
                    event.preventDefault();
                    handleLogout();
                }
            );
        });
    }

    function setupLogin() {
        const form = $("loginForm");

        if (!form) return;

        form.addEventListener(
            "submit",
            handleLogin
        );
    }

    function setupRegister() {
        const form =
            $("registerForm");

        if (!form) return;

        form.addEventListener(
            "submit",
            handleRegister
        );
    }

    function setupAuthLinks() {
        /*
         * Preserve the destination when a protected page
         * sends the user to login.
         */
        const loginLinks =
            document.querySelectorAll(
                'a[href="login.html"]'
            );

        loginLinks.forEach((link) => {
            link.addEventListener(
                "click",
                () => {
                    const current =
                        window.location.pathname
                            .split("/")
                            .pop();

                    if (
                        current &&
                        current !== "login.html"
                    ) {
                        sessionStorage.setItem(
                            "aiJyotishAfterAuth",
                            current
                        );
                    }
                }
            );
        });
    }

    async function checkSession() {
        if (!API) return null;

        try {
            const result =
                await API.me();

            return result;
        } catch (_) {
            return null;
        }
    }

    function initialize() {
        setupLogin();
        setupRegister();
        setupLogout();

        setupPasswordToggle();
        setupPasswordStrength();
        setupAuthLinks();
    }

    window.AIJyotishAuth = {
        login: handleLogin,
        register: handleRegister,
        logout: handleLogout,
        checkSession,
        initialize
    };

    if (
        document.readyState === "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            initialize,
            { once: true }
        );
    } else {
        initialize();
    }
})();
