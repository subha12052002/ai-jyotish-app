// frontend/js/api.js

const API_BASE = "/api";

/**
 * Generic API request helper
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;

    const config = {
        method: options.method || "GET",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    };

    if (options.body !== undefined) {
        config.body =
            typeof options.body === "string"
                ? options.body
                : JSON.stringify(options.body);
    }

    try {
        const response = await fetch(url, config);

        let data = null;

        const contentType = response.headers.get("content-type") || "";

        if (contentType.includes("application/json")) {
            data = await response.json();
        } else {
            const text = await response.text();
            data = text ? { message: text } : null;
        }

        if (!response.ok) {
            const message =
                data?.message ||
                data?.error ||
                `Request failed with status ${response.status}`;

            const error = new Error(message);
            error.status = response.status;
            error.data = data;

            throw error;
        }

        return data;
    } catch (error) {
        console.error(`API request failed: ${options.method || "GET"} ${url}`, error);
        throw error;
    }
}


/* =========================
   AUTH
========================= */

async function getCurrentUser() {
    return apiRequest("/me");
}

async function loginUser(email, password) {
    return apiRequest("/login", {
        method: "POST",
        body: {
            email,
            password
        }
    });
}

async function registerUser(name, email, password) {
    return apiRequest("/register", {
        method: "POST",
        body: {
            name,
            email,
            password
        }
    });
}

async function logoutUser() {
    return apiRequest("/logout", {
        method: "POST"
    });
}


/* =========================
   KUNDLI
========================= */

async function generateKundli(birthData) {
    return apiRequest("/kundli", {
        method: "POST",
        body: birthData
    });
}

async function getLatestKundli() {
    return apiRequest("/kundli/latest");
}


/* =========================
   AI
========================= */

async function askAI(question, chart = null) {
    const body = {
        question
    };

    if (chart) {
        body.chart = chart;
    }

    return apiRequest("/ai/ask", {
        method: "POST",
        body
    });
}


/* =========================
   HEALTH
========================= */

async function getAPIHealth() {
    return apiRequest("/health");
}


/* =========================
   GLOBAL EXPORT
========================= */

window.AIJyotishAPI = {
    request: apiRequest,

    getCurrentUser,
    loginUser,
    registerUser,
    logoutUser,

    generateKundli,
    getLatestKundli,

    askAI,
    getAPIHealth
};